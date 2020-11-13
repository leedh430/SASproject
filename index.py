#!C:\Python3.8\python.exe
print("content-type: text/html; charset=euc-kr\n")
import cgi
import cgitb
import pymysql
import json 

#db connect
conn = pymysql.connect(host='localhost', user='root', password='root1234', database='test_db')
curs = conn.cursor() 
sql_det ="SELECT DEMO_NO, DET_NO, DET_NAME FROM DEMO_DET WHERE DISPLAY_F='Y'"
curs.execute(sql_det)
det_data = curs.fetchall() 

#demo 시나리오
sql_demo_name = "SELECT DEMO_NO, DEMO_NAME FROM demo_master"
curs.execute(sql_demo_name)
demoname_data = curs.fetchall() 

print('''<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-type" content="text/html; charset=UTF-8">
	<link rel="stylesheet" type="text/css" href="main.css">
 </head>
<body>
<div class="background">
		<nav id="mySidenav" class="sidenav">
            <ul>
				<li class="topMenuLi"><a href=".." class="menu">HOME</a></li>
''')
for demodata in demoname_data:  #demodata: [demo_no, demo_name]
	print('<li class="topMenuLi"><a href="#" class="menu">'+demodata[1]+'</a>')
	print('<ul class="subnav">')
	for det in det_data: #det: [demo_no, det_no, det_name]
		if(demodata[0] == det[0]):
			print('<li><a href="scenario.py?demo_no={demo_no}&det_no={det_no}" class="menu">&nbsp;&nbsp;&nbsp;&nbsp;{det_name}</a></li>'.format(
		demo_no=det[0], det_no=det[1], det_name=det[2]))
	print('</ul></li>')

print('''	</ul>  
        </nav> 
	<div class="container">
		<div class="header">
			<p><h1>Real-Time Intelligent Decisioning</p>
		</div>
		<div class="input">
			<iframe name="inframe" src="input.py" width=100% height=500px frameborder=0></iframe>
		</div>
		<div class="output">
			<iframe name="outframe" width=100% height=500px frameborder=0></iframe>
		</div>
	</div>
</div>
</body>
</html>
''')