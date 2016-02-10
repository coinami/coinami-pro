import ConfigParser
import psycopg2

conf = ConfigParser.ConfigParser()
conf.read(['server.conf'])
conn = psycopg2.connect('postgresql://' + conf.get('database','username') + ':' + \
	conf.get('database','password') + '@' + conf.get('database','address') + '/' + \
	conf.get('database','name'))

cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS job;")
cur.execute("DROP TABLE IF EXISTS fastq_file;")
cur.execute("DROP TABLE IF EXISTS fastq_file_group;")

cur.execute("CREATE TABLE fastq_file_group(group_id serial PRIMARY KEY, time integer, merged boolean default false, done boolean default false);")

cur.execute("CREATE TABLE fastq_file(group_id integer REFERENCES fastq_file_group (group_id), file_id serial PRIMARY KEY, read_file varchar(300), isDecoy varchar(10) );")

cur.execute("CREATE TABLE job(group_id integer REFERENCES fastq_file_group (group_id), job_id serial PRIMARY KEY, job_file varchar(300), result_file varchar(300), expiration integer, completed boolean default false, rewarded boolean default false, assigned_to varchar(300));")

conn.commit()
cur.close()