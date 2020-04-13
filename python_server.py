from flask import Flask, render_template, jsonify, request
import json
from flask_cors import CORS, cross_origin
import subprocess 
import operator

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
	return "Welcome"

@app.route('/compile', methods=['GET','POST'])
@cross_origin()
def compile():
	clicked=None
	data = {}
	if request.method == "POST":
		matches = json.loads(request.data.decode("utf-8"))
		text_file = open("sourcecode.jvs", "w")
		text_file.write(str(matches['source_code']))
		text_file.close()
		xval = (str(matches['stdin']).split("=")[1].rstrip().replace("Y","").replace('\r', '').replace('\n', ''))
		yval = (str(matches['stdin']).split("=")[2].rstrip().replace('\r', '').replace('\n', ''))
		proc = subprocess.Popen(['python3', 'python_main.py', xval, yval], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		ans = proc.communicate()[0]
		answer = str(ans)
		if operator.contains(answer, "Traceback"):
			print("Syntax Error"+answer)
			data['output'] = "Syntax Error - Not matches grammar, Or \nSometimes Give spaces between token If possible \nFor example x space * space 2 (x * 2)"
			json_data = json.dumps(data)
			return json_data 
		answer = answer.replace("b","")
		answer = answer.replace("'","")
		answer = answer.replace("\\","")
		answer = answer.replace("n","")
		data['output'] = str(answer)
		json_data = json.dumps(data)
	return json_data

if __name__ == "__main__":
	app.run(debug=True)
