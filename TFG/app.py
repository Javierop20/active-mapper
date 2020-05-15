from flask import Flask, render_template
from json2html import *
import json
import main_functions
app = Flask(__name__)
print("Servidor con tu informe creado!")
@app.route("/")
def index():
    # Abrimos primero el archivo de la CMDB
    with open('templates/data.json') as json_file:
        data = json.load(json_file)
    # Usando la libreria JSON2HTML, convertimos la CMDB en una tabla. Despues agregamos la funcion de busqueda.
    html=json2html.convert(json=data,table_attributes="id=\"myTable\" class=\"header\"")
    writer=open('templates/indextabla.html', 'w')
    writer.write('<html>\n<head>\n')
    writer.write('<meta name="viewport" content="width=device-width, initial-scale=1"><style>* {box-sizing: border-box;}#myInput {background-position: 10px 10px;background-repeat: no-repeat;width: 100%;font-size: 16px;padding: 12px 20px 12px 40px;border: 1px solid #ddd;margin-bottom: 12px;}#myTable {border-collapse: collapse;width: 100%;border: 1px solid #ddd;font-size: 18px;}#myTable th, #myTable td {text-align: left;padding: 12px;}#myTable tr {border-bottom: 1px solid #ddd;}#myTable tr.header, #myTable tr:hover {background-color: #f1f1f1;}</style>')
    writer.write('</head>')
    writer.write('<body>')
    writer.write('<input type="text" id="myInput" onkeyup="myFunction()" placeholder="Busca una IP:" title="Busca una IP">')
    writer.write(html)
    writer.write('<script>function myFunction() {var input, filter, table, tr, td, i, txtValue;input = document.getElementById("myInput");filter = input.value.toUpperCase();table = document.getElementById("myTable");tr = table.getElementsByTagName("tr");for (i = 0; i < tr.length; i++) {td = tr[i].getElementsByTagName("td")[0];if (td) {txtValue = td.textContent || td.innerText;if (txtValue.toUpperCase().indexOf(filter) > -1) {tr[i].style.display = "";} else {tr[i].style.display = "none";}}}}</script>')
    writer.write('\n</body>\n</html>')
    writer.close()
    # Cargamos como template el informe HTML generado
    return render_template('indextabla.html')

@app.route("/data.json")
def data():
    # Cargamos la CMDB por si se quiere integrar con otro sistema
    return render_template('data.json')

if __name__ == '__main__':
    app.run(debug=False)