from flask import Flask, render_template
from json2html import *
import json
import main_functions

app = Flask(__name__, template_folder='.')

@app.route("/")
def index():
    with open('data.json') as json_file:
        data = json.load(json_file)
    html=json2html.convert(json=data)
    writer=open('index.html','w')
    writer.write('<html>\n<body>\n')
    writer.write(html)
    writer.write('\n</body>\n</html>')
    writer.close()
    return render_template('index.html')

@app.route("/data.json")
def data():
    return render_template('data.json')

if __name__ == '__main__':
    app.run(debug=True)