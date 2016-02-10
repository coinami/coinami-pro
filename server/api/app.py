from flask import Flask, jsonify, stream_with_context, Response, request
from flask.ext.cache import Cache

from werkzeug.utils import secure_filename
from zipfile import ZipFile as zf
from subprocess import call

import time
import psycopg2
import os
import json
import ConfigParser

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
conf = ConfigParser.ConfigParser()
conf.read(['server.conf'])
conn = psycopg2.connect('postgresql://' + conf.get('database', 'username') + ':' + \
                        conf.get('database', 'password') + '@' + conf.get('database', 'address') + '/' + \
                        conf.get('database', 'name'))


@app.route('/coinami.key')
@cache.cached(timeout=900)
def public_key():
    return open(conf.get('files', 'key')).read()


@app.route('/info.json')
def authorities():
    return json.dumps(json.loads(open(conf.get('files', 'info.json')).read()))


@app.route('/job_request/<public_key>')
def job_request(public_key):
    cur = conn.cursor()
    cur.execute("SELECT job_id from job where completed = false and expiration < %s;", (int(time.time()),))
    job = cur.fetchone()
    if not job:
        return "-1"
    job_id = job[0]
    cur.execute("UPDATE job SET assigned_to = %s, expiration = %s WHERE job_id = %s;",
                (public_key, int(time.time()) + 86400, job_id))
    conn.commit()
    cur.close()
    return str(job_id)


@app.route("/job/<job_id>")
def job_download(job_id):
    cur = conn.cursor()
    cur.execute("SELECT job_file from job where job_id = %s;", (job_id,))
    job = cur.fetchone()
    if not job:
        return ""
    result_file = job[0]
    try:
        print str(os.path.join(conf.get("folders", "job"), result_file))
        file_object = open(os.path.join(conf.get("folders", "job"), result_file))
    except:
        return "File not found"

    def generator(file_object):
        while True:
            data = file_object.readline()
            if not data:
                break
            yield data

    return Response(stream_with_context(generator(file_object)), mimetype="application/zip")


@app.route("/job_upload", methods=["POST"])
def job_upload():
    result = request.files["result_file"]
    if not result:
        return "No file uploaded"
    job_id = request.form["job_id"]
    if not job_id:
        return "No job_id specified"
    path = os.path.join(conf.get("folders", "result"), str(job_id))
    if not os.path.exists(path):
        os.makedirs(path)
    filename = secure_filename(result.filename)
    fullpath = os.path.join(path, filename)
    result.save(fullpath)
    try:
        p = zf(fullpath)
        p.extractall(path)
        print "Unzipped the file"
        bam_file = os.path.join(path, "result.bam")
        cur = conn.cursor()
        cur.execute("update job set result_file = %s where job_id = %s", (bam_file, job_id))
        conn.commit()
        call([conf.get("executables", "demux"), job_id, conf.get("files", "muxkey"), conf.get("folders", "groups")])
        print "finished demux, checking completed groups"
        cur.execute(
            "select group_id from fastq_file_group where (select count(*) from job where job.group_id = fastq_file_group.group_id and completed = false) = 0 and merged = false;")
        group = cur.fetchone()
        if group != None:
            group_id = group[0]
            print "found group ", group_id
            cur.execute("select file_id from fastq_file where group_id = %s;", (group_id,))
            while True:
                file = cur.fetchone()
                if file == None:
                    break
                file_id = file[0]
                print "merging FASTQ" + str(file_id)
                group_path = os.path.join(conf.get("folders", "groups"), "FASTQ" + str(file_id))
                output = os.path.join(group_path, "result.bam")
                files = os.path.join(group_path, "*")
                print group_path
                print output
                print files
                call("samtools merge " + output + " " + files, shell=True)
                call("samtools index " + output, shell=True)
            cur.execute("update fastq_file_group set merged = true where group_id = %s", (group_id,))
            conn.commit()
            cur.close()
            print "merged group", group_id
        print "no groups to merge"
    except:
        return "Error"
    return "Done"


@app.route("/stats.json")
def stats_json():
    result = {}
    cur = conn.cursor()
    cur.execute("SELECT job_id from job WHERE completed = false and expiration < %s", (int(time.time()),))
    result["unAssigned"] = cur.rowcount
    cur.execute("SELECT job_id from job WHERE completed = false and expiration > %s", (int(time.time()),))
    result["assigned"] = cur.rowcount
    cur.execute("SELECT job_id from job WHERE completed = true", (int(time.time()),))
    result["completed"] = cur.rowcount
    return jsonify(result)


@app.route("/statistics")
def statistics():
    return open("view/statistics.html").read()


@app.route("/upload_form")
def upload_form():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="job_upload" method=post enctype=multipart/form-data>
      <p><input type=file name=result_file />
	<input type=text name=job_id placeholder="Job ID" />
         <input type=submit value=Upload />
    </form>
    '''


@app.route("/jobs_assigned/<public_key>")
def jobs_assigned(public_key):
    cur = conn.cursor()
    cur.execute("SELECT job_id,expiration from job where completed = false and expiration > %s and assigned_to = %s;",
                (int(time.time()), public_key))
    jobs = cur.fetchall()
    result = {}
    result["jobs"] = []
    for job in jobs:
        result["jobs"].append({'job_id': job[0], 'expiration': job[1]})

    cur.close()
    return jsonify(result)


@app.route('/')
def hello():
    return jsonify({'message': 'Hello miner!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7500, debug=True)
