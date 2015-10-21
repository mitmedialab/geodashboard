import json, ast, os

from flask import Flask, render_template

base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

@app.route('/')
def home():
	file_path = os.path.join(base_dir,'static','data','media_sentence_counts.json')
	data = []
	with open(file_path,'r') as data_file:
		data = json.load(data_file)
	return render_template('home.html', media_list=data)  

@app.route('/places')
def places():
	json_obj = []
	with open('static/data/results.json') as f:
		for line in f:
			json_obj.append(json.loads(line))
	#json_obj = json.loads("../GeoDashboard/static/js/results.json")
	json_obj = json_obj[0]
	json_obj = ast.literal_eval(json_obj)
	return render_template('places.html', data=json_obj)  

if __name__ == '__main__':
    app.debug = True
    app.run()
