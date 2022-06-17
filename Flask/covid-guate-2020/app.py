# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from covid_python import *
from datetime import date
import requests

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')


#Datos Generales
def datosGenerales():
    url = "https://api.covid19api.com/country/guatemala?from=2020-05-09T00:00:00Z&to=2020-05-09T00:00:00Z"
    covid_cases = requests.get(url).json()
    general = covid_cases[int(len(covid_cases))-1]
    #numCasos*100/18millones    
    casosTotal = int(general['Confirmed'])
    porcentaje = (casosTotal*100)/18047395
    porcentajeFinal = '{0:.3g}'.format(porcentaje)

    general['porcentajeFinal'] = porcentajeFinal
    return general

@app.route("/")
@app.route("/index")
def index():
    general = datosGenerales()
    return render_template("index.html", general = general)

@app.route("/get",  methods=['GET', 'POST'])
def covid_calculos():
    date = request.args.get('msg')
    confirmados = calcular_dias(date, 0)
    recuperados = calcular_dias(date, 1)
    muertos = calcular_dias(date, 2)
    datos_prediccion = {}
    
    #Infectados    
    datos_prediccion["confirmados"] = prediccion(str(nombresDump[0]),confirmados+3)
    
    #Recuperados
    datos_prediccion["recuperados"] = prediccion(str(nombresDump[1]),recuperados-1)

    #Muertos     
    datos_prediccion["muertos"] = prediccion(str(nombresDump[2]),int(muertos-18))
    
    porcentaje = (int(round(float(datos_prediccion["confirmados"][0])))*100)/18047395
    datos_prediccion["porcentaje"] = '{0:.3g}'.format(porcentaje)
    return datos_prediccion

@app.route("/ia",  methods=['GET', 'POST'])
@app.route("/ia")
def ia():
    grf = request.args.get('grf')
    entrenamiento = request.args.get('entrenamiento')

    if grf:
        get_csvData()
        return "complete"
    elif entrenamiento:
        entrenarModelos()
        return "complete"

    return render_template("ia.html")

@app.route("/informacion")
def informacion():
    return render_template("informacion.html")


if __name__ == "__main__":
    app.run(debug=True)


