#!C:\Python3.8\python.exe
print("content-type: text/html; charset=euc-kr\n")
import cgi
import cgitb
import pymysql
import json 
import requests

#form POST from input.py
form = cgi.FieldStorage()
demo = form["demo"].value
det = form["det"].value 
input_name = list()
input_value = list()

#db connect
conn = pymysql.connect(host='localhost', port=3306, user='root', password='root1234', database='test_db')
curs = conn.cursor()
sql = "SELECT URI FROM demo_det WHERE demo_no="+demo+" AND det_no="+det
curs.execute(sql)
data = curs.fetchall()
uri = data[0][0]

def isFloat(candi):  #문자인지 실수인지 판별용 함수
	try:
		tmp = float(candi)
		return True
	except ValueError:
		return False 

for i in range(len(form["inputid"])):  #입력된 고객 정보 배열 선언하는 반복문
	input_name.append(form["inputid"][i].value) 
	if isFloat(form["inputvalue"][i].value):   #값이 숫자(실수)일 경우
		if form["inputvalue"][i].value.isdecimal() :   #값이 정수일 경우
			form["inputvalue"][i].value = int(form["inputvalue"][i].value) #입력값은 '정수' 형식으로 오기 때문, 정수형으로 변환하여 재선언
		else:
			form["inputvalue"][i].value=float(form["inputvalue"][i].value)
	input_value.append(form["inputvalue"][i].value) 

#SAS 서버 접근 권한(token)을 위한 POST REST 호출
#SAS 서버 정보에 관한 내용은 공백 처리하였습니다. 2020.11.13. 조아라 인턴십 지원	
headers={'Content-Type':'application/x-www-form-urlencoded',
         "Authorization":" "}

response = requests.post('http:// ', headers=headers,
                        data='grant_type= ')

token = response.json()["access_token"]
headers = {"Content-Type":"application/json",
            "Authorization":" "+token,
            "If-Unmodified-Since":" "}

#json 형식의 데이터를 위해 고객 정보 dictionary화
inputs = list()
for i in range (len(input_name)):
    dic = dict()
    dic["name"] = input_name[i]
    dic["value"] = input_value[i]
    inputs.append(dic)


data = {
    "inputs" : inputs, 
    "version" : 1
}

#SAS 서버에 해당 고객 정보 request 및 response
response = requests.post(uri, headers=headers,
                        data=json.dumps(data))
outputlist = response.json()["outputs"]

print('''<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-type" content="text/html; charset=UTF-8">
	<link rel="stylesheet" type="text/css" href="main.css">
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>
<body class="navy_background">
<div>
	<div>
		<div class="output_frame">
			<div class="form-group">
				<label class="col-md-12 control-label" for="prependedtext">출력 데이터</label>
				''')
for i in range(len(outputlist)):  #SAS 서버 내 고객 정보 출력
	output = outputlist[i]	
	print('''				
			<div class="col-md-12">
				<div class="input-group">
				<input class="form-control" placeholder="{output_name}" type="text">
				<input class="form-control" placeholder="{output_value}" type="text">
				</div>
			</div>
		'''.format(output_name=output["name"], output_value=output["value"]))
					
print('''
			</div>
		</div>
	</div>
</div>
</body>
</html>
''')