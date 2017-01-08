#!/usr/bin/python

import xlrd
import sys
import getopt
import MySQLdb
from passlib.hash import bcrypt_sha256

reload(sys)
sys.setdefaultencoding('utf8')

def usage():
	print "Usage:./auto.py -s test -t database"
	sys.exit(0)

def checkdb(dbuser,dbpasswd,dbname):
	try:
		conn=MySQLdb.connect("localhost",dbuser,dbpasswd,dbname,charset="utf8")	
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0],e.args[1])

def checktable(dbuser,dbpasswd,dbname):
	try:
		conn=MySQLdb.connect("localhost",dbuser,dbpasswd,dbname,charset="utf8")

		sql = "select table_name from information_schema.TABLES WHERE table_name = 'teams' and table_schema=" + "'" + dbname + "';" 
		cursor = conn.cursor()
		cursor.execute(sql)
		data = cursor.fetchone()
		if data == None :
			print "Database " + dbname + " is not initialized!!"
			conn.close()
			sys.exit(0)
		else:
			conn.close()
			pass
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0],e.args[1])
		conn.close()

# Read the excel table and insert all tasks into table task
def insert_data(dbuser,dbpasswd,dbname,excel):
	try:
		conn=MySQLdb.connect("localhost",dbuser,dbpasswd,dbname,charset="utf8")
		cursor = conn.cursor()
		data = xlrd.open_workbook(excel)
		# insert task
		table1 = data.sheets()[0]
		#print table.nrows
		for i in range (0,table1.nrows):
			j = str(i+1)
			#print table.row_values(i)[0]
			sql = "insert into task(task_id,task_name,task_count) values (" + j + "," + "'" + table1.row_values(i)[0].replace(' ', '') + "'," + "0" + ")"
			#print sql
			cursor.execute(sql)
		conn.commit()
		# insert student
		password="123456"
		std_password=bcrypt_sha256.encrypt(password)
		#print password

		table2 = data.sheets()[1]
		#print table2.row_values(1)[0].rstrip()
		for k in range (0,table2.nrows):
			m = str(k+1)
			sql = "insert into student(student_id,student_name,student_password,student_is_task,student_progress,student_score,admin) values ('" + table2.row_values(k)[0].rstrip() + "'," + "'" + table2.row_values(k)[1].rstrip() + "'," + "'" + std_password + "'," + "0" + ","+ "0" + "," + "0" + "," + "1" + ")"
			cursor.execute(sql)
		conn.commit()
		print "Succeed!!"
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0],e.args[1])
		conn.close()

def main():
	dbuser = "root"
	dbpasswd = "cloudstack"
	dbname = ""
	excel = ""
	if not len(sys.argv[1:]):
		usage()
	try:
		opts,args=getopt.getopt(sys.argv[1:],"s:t:")
	except getopt.GetoptError as err:
		print str(err)
		usage()
	for o,arg in opts:
		if o == "-s":
			excel = arg + ".xlsx"
		elif o == "-t":
			dbname = arg
		else:
			usage()
	checkdb(dbuser,dbpasswd,dbname)
	checktable(dbuser,dbpasswd,dbname)
	insert_data(dbuser,dbpasswd,dbname,excel)

main()