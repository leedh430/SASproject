#!C:\Python3.8\python.exe
print("content-type: text/html; charset=euc-kr\n")
import cgi
import cgitb
import json
import pymysql 

#form from index.py   +)cgi모듈 활용, 전달받은 호출인자 추출
form = cgi.FieldStorage()
demo_no = form["demo_no"].value
det_no = form["det_no"].value

#db connect
conn = pymysql.connect(host='localhost', user='root', password='root1234', database='test_db')
curs = conn.cursor()

#현재 시나리오 이름 db로부터 호출
sql_scenario_name = 'SELECT DET_NAME FROM demo_det WHERE DEMO_NO = '+demo_no+' and DET_NO='+det_no
curs.execute(sql_scenario_name)
data = curs.fetchall()
sce_name = data[0][0]

#case +)상세 시나리오별 고객 정보 db 호출
sql_case = "SELECT case_no, MAX(case_desc) FROM demo_det_data WHERE DEMO_NO="+demo_no+"  and DET_NO="+det_no+" GROUP BY CASE_NO"
curs.execute(sql_case)
case_data = curs.fetchall()  

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
				<li class="topMenuLi"><a href=".." class="menu">Home</a></li>
				<li class="menu">{scenario_name}</li>
'''.format(scenario_name=sce_name))
for i in range(len(case_data)):	
	print('<li class="caseMenuLi"><a href="input.py?demo={demo_no}&det={det_no}&case={case_no}" class="menu" target="inframe">&nbsp;&nbsp;&nbsp;&nbsp;Case #{case_no}</a>'.format(
		demo_no=demo_no, det_no=det_no, case_no=case_data[i][0]))  #호출할 고객 정보 input.py 전송
	print('''<ul class="subnav">
				<li class="menu" style="color:black;">
					&nbsp;&nbsp;&nbsp;&nbsp;{case_desc}
				</li>
			</ul>
		</li>'''.format(case_desc=case_data[i][1]))

print('''
            </ul>  
        </nav> 
	<div class="container">
		<div class="header">
			<p><h1>{scenario_name}</p>
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
'''.format(scenario_name=sce_name, demo_no=demo_no, det_no=det_no))