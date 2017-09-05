from kami import load_table, find_next, lookup
from flask import Flask, request, redirect, url_for
import bleach

app = Flask(__name__)

data = load_table('data/out.txt', columns=['m', 'n', 'alpha'])

HTML_WRAP = '''\
<!DOCTYPE html>
<html>
	<head>
		<title>Tính lún bằng phương pháp cộng lớp</title>
		<style>
			h1, form {{ text-align: center; }}
			input {{ border: 1px solid #999; }}
			div.result {{ border: 1px solid #999;
						  padding: 10px 10px;
						  margin: 10px 20%; }}
		</style>
	</head>
	<body>
		<h1>Tính Độ Lún</h1>
		<form method=post>
			Giá trị m:</br>
			<input type="text" id="m" name="m" value="{}"></input></br>
			Giá trị n:</br>
			<input type="text" id="n" name="n" value="{}"></input></br>
			<input id="go" type="submit" value="Tra hệ số alpha"></button>
		</form>
		<div class=result>
			{}
		</div>
	</body>
</html>
'''

@app.route('/', methods=['GET'])
def main():
	return HTML_WRAP.format('', '', 'Vui lòng nhập tham số m, n')

@app.route('/', methods=['POST'])
def settle():
	try:
		m = float(bleach.clean(request.form['m'].replace(',', '.')))
		n = float(bleach.clean(request.form['n'].replace(',', '.')))
	except Exception as e:
		result = HTML_WRAP.format('Giá trị không hợp lệ, vui lòng thử lại')
		return result
	cols = list(find_next(m, data.iloc[:, 0]))
	rows = list(find_next(n, data.iloc[:, 1]))
	result = [v[2] for v in lookup(m, n, data)]
	result = '''\
	Giá trị alpha tương ứng với các giá trị m, n gần nhất
	<table>
	  	<tr>
	  		<th></th>
	    	<th>{n[0]}</th> 
	    	<th>{n[1]}</th>
	  	</tr>
	  	<tr>
	   		<th>{m[0]}</th>
	    	<td>{d[0]}</td>
	    	<td>{d[1]}</td>
	  	</tr>
	  	<tr>
	    	<th>{m[1]}</th>
	    	<td>{d[2]}</td>
	    	<td>{d[3]}</td>
	  	</tr>
	</table>
	'''.format(m=cols, n=rows, d=result)
	result = HTML_WRAP.format(request.form['m'], request.form['n'], result)
	return result

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080)