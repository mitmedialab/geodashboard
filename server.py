from flask import Flask, render_template
import json
import ast

app = Flask(__name__)

@app.route('/')
def home():
	json_obj = []
	with open('static/data/results.json') as f:
		for line in f:
			json_obj.append(json.loads(line))
	#json_obj = json.loads("../GeoDashboard/static/js/results.json")
	json_obj = json_obj[0]
	json_obj = ast.literal_eval(json_obj)
	return render_template('home.html', data=json_obj)  

if __name__ == '__main__':
    app.debug = True
    app.run()
