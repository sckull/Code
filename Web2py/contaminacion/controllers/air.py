####################################################################
#                        Calidad del Aire                          #
####################################################################

# ACQIN TOKEN - 116e65bebc8b18241e1c8363c4cddc853ae363e2
# API ACQIN
def airQualityAPI(country):
    import requests
    #pip install python-dateutil
    from dateutil import parser


    #Sensors
    sensor_data = ["co", "no2", "o3", "m10", "pm25", "pm10", "so2","uvi"]

    #API
    URL_BASE = "https://api.waqi.info/feed/"
    TOKEN    = "116e65bebc8b18241e1c8363c4cddc853ae363e2"

    response = requests.get(f"{URL_BASE}{country}/?token={TOKEN}")
    r = response.json()
    
    if response.status_code == 404 or len(r["data"]) == 0 or r["data"]=="Unknown station":
        return "Error"

    if response.status_code == 200:
        general = {}
        data = response.json()['data']
        general["actual"]    = data["aqi"]
        general["city"]      = data["city"]["name"]
        general["station"]   = data["attributions"][0]["name"]
        general["last_time"] = parser.parse(data["time"]["s"]).strftime("%A - %H:%M")
        

        #Forecast - Daily
        if 'daily' not in data["forecast"]:
            general["forecast"] = 'no'
        else:
            forecast_daily = {}
            for e in data["forecast"]["daily"]:
                if e in sensor_data:
                    forecast_daily[e] = data["forecast"]["daily"][e]
            
            general["forecast"] = forecast_daily
        
        #Actual Values - Sensor
        sensor_values = {}
        for i in data["iaqi"]:
            if i in sensor_data:
                sensor_values[i] = data["iaqi"][i]['v']
        
        general["sensor"] = sensor_values
        #print(general)
        return(general)    
    else:
        return "Error"

def index():
    redirect(URL('calidadAire'))

def calidadAire():
    paises = db(db.calidadAire.pais_id == db.pais.id).select(db.calidadAire.id, 
                                                            db.calidadAire.activo,
                                                            db.pais.nombre,
                                                            db.pais.id)

    contenido = db(db.contenido.tipo_contenido_id == 2).select(db.contenido.titulo, 
                                                            db.contenido.contenido,
                                                            db.contenido.imagen_con)  
    return dict(paises = paises, contenido = contenido)

def country():
    if request.vars:
        pais = request.vars.pais
        general = airQualityAPI(pais)
        conceptos = db(db.concepto).select()

        if general == "Error":
            session.flash = T('Informacion no encontrada')
            redirect(URL('calidadAire'))

        alertas = db(db.alerta).select()
        
        for a in alertas:
            a_min = int(a.rango_menor) -1
            a_max = int(a.rango_mayor) +1         
            if general['actual'] in range(a_min,a_max):
                alerta = a
                break
            else:
                alerta = {"nombre":"Alerta no Encontrada", "descripcion":"Alerta no encontrada"}
        return dict(general = general, alerta = alerta, conceptos = conceptos)
    else:
        redirect(URL('calidadAire'))
        

