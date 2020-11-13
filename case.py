#!C:\Python\Python38-32\python.exe
print("content-type: text/html; charset=euc-kr\n")
import cgi
import cgitb
import pymysql
import json 

#form from scenario.py
form = cgi.FieldStorage()
demo_no = form["demo_no"].value
det_no = form["det_no"].value

#db connect
conn = pymysql.connect(host='localhost', port=3306, user='root', password='root1234', database='test_db')
curs = conn.cursor()
sql = "SELECT CASE_NO FROM demo_det_data WHERE DEMO_NO="+demo_no+ " AND DET_NO="+det_no+" GROUP BY CASE_NO" 
curs.execute(sql)
case_no = curs.fetchall()

case_function = '''
    function ccase(demo_no, det_no, case_no){ 
        parent.inframe.location.href = "input.py?demo="+demo_no+"&det="+det_no+"&case="+case_no;
        }
        '''

print('''<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-type" content="text/html; charset=UTF-8">
	<link rel="stylesheet" type="text/css" href="main.css">
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>
<body>
    <script type="text/javascript">
      {case_function}
    </script>
'''.format(case_function=case_function))
for i in range(len(case_no)):
  print('''
      <button onclick="ccase({demo_no},{det_no},{case_no})";>케이스 {case_no}</button>
      '''.format(demo_no=demo_no, det_no=det_no, case_no=case_no[i][0]))

print('''
</body>
</html>
''')
