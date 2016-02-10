# usr/bin/env python
import json
import os
import sys
import time
import urllib
import urllib2

import requests

conf_dir = os.path.expanduser('~/.coinami')
conf_file = os.path.expanduser('~/.coinami/client.conf')

from subprocess import call
from zipfile import ZipFile as zf
from ConfigParser import ConfigParser

conf = ConfigParser()
conf.read([conf_file])

base_url = "http://localhost:7500"


def assignedJobs(public_key):
    conn = urllib.urlopen(base_url + "/jobs_assigned/" + public_key)
    try:
        content = conn.read()
        jContent = json.loads(content)
        jobs = jContent['jobs']
        fineJobs = []
        for job in jobs:
            if job['expiration'] > time.time():
                fineJobs.append(str(job['job_id']))
        return fineJobs
    except:
        return []


def request_job(public_key):
    conn = requests.get(base_url + "/job_request/" + public_key)
    if conn.status_code == 200:
        return conn.text
    else:
        return 0


def download_job(job_id):
    url = base_url + '/job/' + job_id

    try:
        if not os.path.isdir("job/"):
            os.mkdir("job")
        os.mkdir("job/" + job_id)
    except:
        updateStatus("There was a problem while creating job folder", 0)
        return False

    try:
        updateStatus("Downloading job", 10)
        file_name = "job/job_" + job_id + ".zip"
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        context = u.read()
        f.write(context)
        f.close()
    except:
        updateStatus("There was a problem while downloading the job.", 0)
        return False

    try:
        z = zf("job/job_" + job_id + ".zip")
        z.extractall("job/" + job_id)
        os.remove("job/job_" + job_id + ".zip")
    except:
        updateStatus("Downloaded file is broken", 20)
        return False

    return True


def run_bwa(job_id):
    try:
        updateStatus('Running BWA', 20)
        if conf.get("files", "ref") == "none":
            updateStatus('Reference Genome is not set', 20)
            return False
        call(["bwa", "mem", conf.get("files", "ref"), "job/" + job_id + "/job.1.fq", "job/" + job_id + "/job.2.fq"],
             stdout=open("output.sam", "w"))
        call(["samtools", "view", "-bS", "-o", "output.bam", "output.sam"])
        call(["samtools", "sort", "output.bam", "output.sorted"])
        call(["samtools", "rmdup", "output.sorted.bam", "result.bam"])
        call(["samtools", "index", "result.bam"])
        call(["rm", os.path.join("job", job_id), "-rf"])
        os.remove("output.sam")
        return True
    except:
        return False


def zip_results():
    try:
        updateStatus('Compressing results', 80)
        z = zf("result.zip", mode="w")
        z.write("result.bam")
        z.write("result.bam.bai")
        os.remove("result.bam")
        os.remove("result.bam.bai")
        return True
    except:
        return False


def upload_results(job_id):
    try:
        updateStatus('Uploading results', 90)
        files = {'result_file': open("result.zip")}
        data = {'job_id': job_id}
        r = requests.post(base_url + "/job_upload", files=files, data=data)
        if r.text == u"Done":
            return 0
        else:
            return 1
    except:
        return 2


def updateStatus(update, progress):
    print json.dumps({'status': update, 'progress': progress})
    sys.stdout.flush()


def main():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    try:
        args = sys.argv[1:]
        pubkey = args[0]
    except:
        updateStatus('You need to specify a pubkey', 0)
        return 1

    while True:

        job_id = -1

        jobs = assignedJobs(pubkey)
        if len(jobs) != 0:
            if os.path.isdir("job/"):
                subs = [x[0] for x in os.walk("job")]
                for i in range(1, len(subs)):
                    job_id_t = subs[i]
                    job_id_t = job_id_t.split(os.sep)
                    job_id_t = job_id_t[1]
                    if job_id_t in jobs:
                        job_id = job_id_t

        if job_id == -1:

            if len(jobs) != 0:
                job_id = jobs[0]
            else:
                updateStatus('Requesting Job', 0)
                job_id = request_job(pubkey)
                if job_id == 0:
                    updateStatus('Request is failed', 0)
                    return 2
                elif job_id < 0:
                    updateStatus('There is no job left', 0)
                    return 7

            job_file = download_job(job_id)
            if not job_file:
                return 3

        bwa = run_bwa(job_id)
        if not bwa:
            updateStatus('One of the bwa and samtools calls is failed', 20)
            return 4

        ziping = zip_results()
        if not ziping:
            updateStatus('Compressing of the results was failed', 80)
            return 5

        upload = upload_results(job_id)
        if upload == 1:
            updateStatus('Results were wrong', 90)
            return 6
        elif upload == 2:
            updateStatus('Upload failed', 90)
            return 8

        updateStatus('Work is completed', 100)


if __name__ == '__main__':
    main()
