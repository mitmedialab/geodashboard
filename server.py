import json, ast, os, logging

from flask import Flask, render_template

base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

log_file_path = os.path.join(base_dir,'logs','geodashboard.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting up!")

@app.route('/')
def home():
	logging.debug("home")
	file_path = os.path.join(base_dir,'static','data','media_sentence_counts.json')
	logging.debug("loaded file")
	data = []
	with open(file_path,'r') as data_file:
		data = json.load(data_file)
	logging.debug("loaded data")
	return render_template('home.html', media_list=data['mediaInfo'], 
		highlighted_tag=data['highlightedTag'], totals=data['total'])  

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
