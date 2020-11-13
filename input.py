#!C:\Python3.8\python.exe
print("content-type: text/html; charset=euc-kr\n")
import cgi
import cgitb
import pymysql
import json 

#choice from case.py +)전송된 시나리오 및 고객 정보
demo_no=''  #호출한 case가 없을 시 빈 화면 출력을 위한 선언
det_no=''
case_no=''
form = cgi.FieldStorage()
if 'demo' in form:    #호출이 있을시에만
    demo_no = form["demo"].value
    det_no = form["det"].value
    case_no = form["case"].value

    #db connect
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root1234', database='test_db')
    curs = conn.cursor()
    sql = "SELECT input_name, input_id, input_value FROM demo_det_data WHERE DEMO_NO="+demo_no+" and DET_NO="+det_no+" and CASE_NO=" + case_no
    curs.execute(sql)
    case_data = curs.fetchall()

test_function = '''
    function test(){
        var f = document.inputform;
        f.target="outframe";
        f.action="output.py";
        f.submit();
        }
        '''  #input iframe내 입력을 output iframe으로 전달하기 위한 자바스크립트 함수

print('''<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-type" content="text/html; charset=UTF-8">
	<link rel="stylesheet" type="text/css" href="main.css">
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>
<body class="blue_background">
    <script type="text/javascript">
    {test_function}
    </script>
<div>
	<div>
		<div>
			<form name="inputform" accept-charset="utf-8">
                <input type="hidden" name="demo" value={demo_no}>
                <input type="hidden" name="det" value={det_no}>
				<div class="content-input">
					<div class="form-group">
					<label class="col-md-12 control-label" for="prependedtext"></label>
                    '''.format(test_function=test_function, demo_no=demo_no, det_no=det_no))
for i in range(len(case_data)):   #선택된 고객의 db내부 정보 input form으로 호출
    print('''
    <div class="col-md-12">
        <div class="input-group">
        <input id="prependedtext" class="form-control" placeholder="{description}" type="text">
        <input type="hidden" name="inputid" value={key}>
        <input id="prependedtext" name="inputvalue" class="form-control" type="text" value={value}>
        </div>
    </div>'''.format(description=case_data[i][0], key=case_data[i][1], value=case_data[i][2]))
print('''
					</div>
				</div>
			</form>
            <button onclick="test()">호출</button>
		</div>
	</div>
</div>

</body>
</html>
''')