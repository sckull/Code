# -*- coding: utf-8 -*-
import pandas as pd
import io, re, os
import requests
import numpy as np
from sklearn.neural_network import MLPRegressor
#from sklearn.externals import joblib
import sklearn.externals as extjoblib
import joblib


from datetime import date

#Confirmados = 0, Recuperdos = 1, Muertos = 2
APIS = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv']

#Confirmados = 0, Recuperdos = 1, Muertos = 2
casosUno = [55, 66, 75]

#Confirmados = 0, Recuperdos = 1, Muertos = 2
basesEntrenamiento = [0.99, 0.98, 0.97]

#Confirmados = 0, Recuperdos = 1, Muertos = 2
nombresDump = ['casosConfirmados',
               'casosRecuperados',
               'casosMuertos']

#Funcion para entrenamiento segun el API y el Caso
def entrenamientoDatos(API, casoUNO, nombreDump, baseEntrenamiento):
    url = API
    s = requests.get(url).content
    datos = ""
    datos = pd.read_csv(io.StringIO(s.decode('utf-8')))
    datos.shape

    #Pais
    cdatos = pd.DataFrame.copy(datos)
    cdatos = cdatos.set_index('Country/Region')
    cdatos.shape

    #Nombre de Pais
    nombrePaises = datos['Country/Region'].drop_duplicates(keep='first')
    nombrePaises.shape

    #Guatemala
    Pais = cdatos.loc[['Guatemala']]
    #Pais.head()

    #Casos
    #3/14/20
    casoUno = casoUNO
    casos = Pais.iloc[:,casoUno:]
    datosOrden = casos.melt(var_name="Fecha", value_name="Casos")
    #datosOrden.head()

    #Agregar "DIAS" columna
    num = len(datosOrden["Casos"])
    lista = list(range(0,num))
    datoFinal = datosOrden.assign(Dias = lista)

    #Valores en X y Y
    x = datoFinal["Dias"]
    y = datoFinal["Casos"]

    X=x[:,np.newaxis]
    X=X.reshape(-1,1)

    while True:
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        mlr = MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5,5), random_state=1)
        mlr.fit(X_train, y_train)
        if mlr.score(X_train, y_train) > baseEntrenamiento:
            break
    #Precision
    #print(mlr.score(X_train, y_train))  
    if nombreDump == "casosConfirmados":
        label_title = "Personas Confirmadas Infectados"
    elif nombreDump == "casosRecuperados":
        label_title = "Personas Confirmadas Recuperadas"
    elif nombreDump == "casosMuertos":
        label_title = "Personas Confirmadas Muertos"
    else:
        print("error")
        
    #Generar Figura
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker
    import matplotlib as mpl
    mpl.rcParams['figure.dpi']=150
    x = ""
    y = ""

    x = datoFinal["Dias"]
    y = datoFinal["Casos"]
    label = datoFinal[datoFinal.columns[0]]

    plt.rcParams.update({'font.size': 7})
    plt.plot(label,y, color="#84e69a")
    plt.ylabel('Numero de Casos', fontsize=7)
    plt.xlabel('Fecha - 7 dias',fontsize=7)
    plt.xticks(np.arange(min(label.index), max(label.index),7), rotation=90, fontsize=5 )
    plt.title(label_title,fontsize=12)
    plt.grid(alpha=0.1)
    plt.savefig(nombreDump+'.png')
    
    # Mover Imagenes
    import shutil
    shutil.move(nombreDump+'.png', 'static/graficas/'+nombreDump+'.png')
    
    #Generar modelo y guardarlo
    nombreDump = nombreDump + '.pkl'
    joblib.dump(mlr, nombreDump)
    
    # Mover Modelos
    shutil.move(nombreDump, 'modelos/'+nombreDump)

#Prediccion segun Archivo Dumpeado de Entrenamiento
def prediccion(nombreDump, dia):
    clf_from_joblib = joblib.load('modelos/'+nombreDump+'.pkl')
    pr = re.findall(r"\d+\.\d+", str(clf_from_joblib.predict([[dia]]))) 
    return pr

#Generar Figuras de DF
def generarFiguras(API, casoUNO, nombreDump, baseEntrenamiento):    
    url = API
    s = requests.get(url).content
    datos = ""
    datos = pd.read_csv(io.StringIO(s.decode('utf-8')))
    datos.shape

    #Pais
    cdatos=""
    cdatos = pd.DataFrame.copy(datos)
    cdatos = cdatos.set_index('Country/Region')
    cdatos.shape

    #Nombre de Pais
    nombrePaises = datos['Country/Region'].drop_duplicates(keep='first')
    nombrePaises.shape

    #Guatemala
    Pais = cdatos.loc[['Guatemala']]
    #Pais.head()

    #Casos
    #3/14/20
    casoUno = casoUNO
    casos = Pais.iloc[:,casoUno:]
    datosOrden=""
    datosOrden = casos.melt(var_name="Fecha", value_name="Casos")
    #datosOrden.head()

    #Agregar "DIAS" columna
    num = len(datosOrden["Casos"])
    lista = list(range(0,num))
    datoFinal=""
    datoFinal = datosOrden.assign(Dias = lista)

    #Valores en X y Y
    y =""
    x =""
    X =""
    x = datoFinal["Dias"]
    y = datoFinal["Casos"]

    X=x[:,np.newaxis]
    X=X.reshape(-1,1)
    if nombreDump == "casosConfirmados":
        label_title = "Personas Infectadas"
    elif nombreDump == "casosRecuperados":
        label_title = "Personas Recuperadas"
    elif nombreDump == "casosMuertos":
        label_title = "Personas Fallecidas"
    else:
        print("error")
        
    #Generar Figura
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker
    import matplotlib as mpl
    mpl.rcParams['figure.dpi']=150
    x = ""
    y = ""
    label = ""

    x = datoFinal["Dias"]
    y = datoFinal["Casos"]
    label = datoFinal[datoFinal.columns[0]]

    plt.rcParams.update({'font.size': 7})
    plt.plot(label,y, color="#84e69a")
    plt.ylabel('Numero de Casos', fontsize=7)
    plt.xlabel('Fecha - 7 dias',fontsize=7)
    plt.xticks(np.arange(min(label.index), max(label.index),7), rotation=90, fontsize=5 )
    plt.title(label_title,fontsize=12)
    plt.grid(alpha=0.1)
    plt.savefig(nombreDump+'.png')
    plt.close()
    
    # Mover Imagenes
    import shutil
    shutil.move(nombreDump+'.png', 'static/graficas/'+nombreDump+'.png')

#Calcular dias a partir de fecha dada
def calcular_dias(fecha, caso):
    #Confirmados = 0, Recuperdos = 1, Muertos = 2
    fechas = [date(2020, 3, 14),
            date(2020, 3, 25),
            date(2020, 3, 16)]

    formatear_date = fecha
    x = formatear_date.split("-")

    date_final = date(int(x[0]), int(x[1]), int(x[2]))
    delta = date_final - fechas[int(caso)]
    return int(delta.days)

def entrenarModelos():
    #Entrenamiento Confirmados
    entrenamientoDatos(APIS[0], casosUno[0], nombresDump[0], basesEntrenamiento[0])

    #Entrenamiento Recuperados
    entrenamientoDatos(APIS[1], casosUno[1], nombresDump[1], basesEntrenamiento[1])

    #Entrenamiento Muertos
    entrenamientoDatos(APIS[2], casosUno[2], nombresDump[2], basesEntrenamiento[2])
    print("Entrenado")

"""
#FIGURA Confirmados
generarFiguras(APIS[0], casosUno[0], nombresDump[0], basesEntrenamiento[0])

#FIGURA Recuperados
generarFiguras(APIS[1], casosUno[1], nombresDump[1], basesEntrenamiento[1])

#FIGURA Muertos
generarFiguras(APIS[2], casosUno[2], nombresDump[2], basesEntrenamiento[2])
"""


"""
#PREDICCION Confirmados 44
print("Confirmados")
print(prediccion(str(nombresDump[0]),44))
#PREDICCION Recuperados 33
print("Recuperados")
print(prediccion(str(nombresDump[1]),33))
#PREDICCION Muertos 42
print("Muertos")
print(prediccion(str(nombresDump[2]),42))
"""

def get_csvData():
    for i in range(0,3):
        print("CASOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO: "+ str(i))
        url = APIS[i]
        s = requests.get(url).content
        datos = ""
        datos = pd.read_csv(io.StringIO(s.decode('utf-8')))
        datos.shape

        #Pais
        cdatos = pd.DataFrame.copy(datos)
        cdatos = cdatos.set_index('Country/Region')
        cdatos.shape

        #Nombre de Pais
        nombrePaises = datos['Country/Region'].drop_duplicates(keep='first')
        nombrePaises.shape

        #Guatemala
        Pais = cdatos.loc[['Guatemala']]
        #Pais.head()

        #Casos
        #3/14/20
        casoUno = casosUno[i]
        casos = Pais.iloc[:,casoUno:]
        nombreDump = str(nombresDump[i]) + '.csv'
        path = os.path.abspath(os.getcwd())+'/static/datasets/'        
        print(path)
        casos.to_csv(path+nombreDump, encoding='utf-8')

