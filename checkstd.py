#!/usr/bin/python

import sys
import getopt
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')

def usage():
	print "Usage:./auto.py -t database"
	sys.exit(0)

def checkstudent(dbuser,dbpasswd,dbname):
	try:
		conn=MySQLdb.connect("localhost",dbuser,dbpasswd,dbname,charset="utf8")
		sql = "select student_id,student_name from student WHERE student_is_task = 0"
		cursor = conn.cursor()
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			print "number: %s, name: %s" % (row[0],row[1])
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0],e.args[1])
		conn.close()

def main():
	dbuser = "root"
	dbpasswd = "cloudstack"
	dbname = ""
	if not len(sys.argv[1:]):
		usage()
	try:
		opts,args=getopt.getopt(sys.argv[1:],"t:")
	except getopt.GetoptError as err:
		print str(err)
		usage()
	for o,arg in opts:
		if o == "-t":
			dbname = arg
		else:
			usage()
	checkstudent(dbuser,dbpasswd,dbname)

main()