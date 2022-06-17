def index():
    contenido = db(db.contenido.tipo_contenido_id ==3).select()
    paises = db(db.pais).select(db.pais.id, db.pais.nombre)
    return dict(contenido = contenido, paises = paises)

def country():
    if request.vars:
        pais = request.vars.pais

        #Cambio climatico
        nombre = db(db.pais.id == pais).select(db.pais.nombre).first()
        data = db(db.cambio_climatico.pais_id == pais).select(db.cambio_climatico.tipo_cambio_id,
                                                              groupby=db.cambio_climatico.tipo_cambio_id)
        cambio = {}
        
        for d in data:
            tmp = db((db.cambio_climatico.pais_id == pais)&
                (db.cambio_climatico.tipo_cambio_id == d.tipo_cambio_id)).select(db.cambio_climatico.cantidad,
                                                                                    db.cambio_climatico.fecha,
                                                                                    orderby=db.cambio_climatico.fecha).as_list()
                                                   
            fecha = []
            valor = []
            for i in tmp:
                if i['cantidad'] != 0:
                    f = i['fecha'].strftime('%Y-%m')
                    fecha.append(f)
                    valor.append(i['cantidad'])
            
            descr = db(db.tipo_cambio_climatico.id == d.tipo_cambio_id).select(db.tipo_cambio_climatico.nombre).first()

            descripcion = db(db.tipo_cambio_climatico.id == d.tipo_cambio_id).select(db.tipo_cambio_climatico.descripcion).first()

            cambio[descr['nombre']] = {'fecha':fecha, 'valor':valor, 'descripcion':descripcion['descripcion']}
        
        conceptos = db(db.concepto).select()
        
        #Reporte
        #fechas = db((db.cambio_climatico.pais_id == pais)
        #            &(db.cambio_climatico.cantidad != None)).select(db.cambio_climatico.fecha, orderby=~db.cambio_climatico.fecha)
        #tipos = db(db.tipo_cambio_climatico).select(db.tipo_cambio_climatico.id, db.tipo_cambio_climatico.nombre)

        #fechas = sorted(set(to_list(fechas)))
        #fechas = sorted([x[:7] for x in fechas])
        #fechas.reverse()
        #return dict(paises = paises, fechas = fechas)

        return dict(nombre = nombre, cambio = cambio, conceptos = conceptos, pais = pais)
    else:
        session.flash = T('Informacion no encontrada')
        redirect(URL('cambioclimatico'))
    
#Utils
def insertar_datos_h():
    import glob
    #Historico - Lluvia
    path = '/home/sckull/tmp/contaminacion/cambioclimatico/lluvia_h/'
    paises = db(db.pais).select(db.pais.id, db.pais.nombre, db.pais.codigo_alt)
    #tipo = id -- 2
    tipo = 2
        
    #Historico - Temperatura
    #path = '/home/sckull/tmp/contaminacion/cambioclimatico/temp_h/'
    #paises = ['GTM', 'SLV', 'HND', 'BLZ', 'PAN', 'NIC', 'CRI']
    fechas = {'Jan Average':'01', 'Feb Average':'02', 'Mar Average':'03', 'Apr Average':'04', 
              'May Average':'05', 'Jun Average':'06', 'Jul Average':'07', 'Aug Average':'08', 
              'Sep Average':'09', 'Oct Average':'10', 'Nov Average':'11', 'Dec Average':'12'}
    
    paises = {
        'Guatemala':'1',
        'El+Salvador': '2',
        'Honduras':'3',
        'Belice':'4',
        'Panama':'5',
        'Nicaragua':'6',
        'Costa+Rica':'7',        
    }

    files = glob.glob(path+'*')

    for file in files:
        #A Lineas
        with open(file) as f:
            content = f.readlines()        
        content = [x.strip().split(', ') for x in content]
        content = content[1:]
        
        #Lineas en content
        for x in content:
            if x[2] in fechas:
                fecha = x[1] +'/'+ fechas.get(x[2])+'/' + '01'
                cantidad = x[0]
                pais = paises.get(x[3])
                db.cambio_climatico.update_or_insert(tipo_cambio_id=tipo, pais_id=pais, cantidad=cantidad, fecha=fecha)
                db.commit()
            else:
                print(":/")
        print(file)

#Utils
def api_cambio_climatico():
    import wbpy
    from pprint import pprint
    import datetime

    c_api = wbpy.ClimateAPI()
    c_api.ARG_DEFINITIONS["instrumental_types"]
    c_api.ARG_DEFINITIONS["instrumental_intervals"]

    #['year', 'month', 'decade']
    iso_and_basin_codes = ['GTM', 'SLV', 'HND', 'BLZ', 'PAN', 'NIC', 'CRI']

    #Definir pr o tas
    #dataset = c_api.get_instrumental(data_type="pr", interval="year", locations=iso_and_basin_codes)
    data = dataset.as_dict()

    paises = {
        'GT':'1',
        'SV': '2',
        'HN':'3',
        'BZ':'4',
        'PA':'5',
        'NI':'6',
        'CR':'7',        
    }
    #tipo 2 = Precipitacion (pr)
    #tipo 1 = Temperatura  (tas)
    tipo = 2
    
    for d in data:
        pais = paises.get(d)
        g = data[d]
        for i in g:
            if i != 1901:            
                fecha = datetime.datetime(int(i), 1, 1)
                cantidad = g[i]
                #db.cambio_climatico.update_or_insert(tipo_cambio_id=tipo, pais_id=pais, cantidad=cantidad, fecha=fecha)
                #db.commit() 
        print(pais)      


#Utils      
def api_cambio_climatico_futuro():
    import wbpy
    from pprint import pprint
    import datetime

    c_api = wbpy.ClimateAPI()
    c_api.ARG_DEFINITIONS["modelled_types"]
    c_api.ARG_DEFINITIONS["modelled_intervals"]

    #['year', 'month', 'decade']
    location = ['GTM', 'SLV', 'HND', 'BLZ', 'PAN', 'NIC', 'CRI']
    #loc = ['GTM']

    #Definir pr o tas
    modelled_dataset = c_api.get_modelled("pr", "mavg", location)
    data = modelled_dataset.as_dict(sres="b1")['cccma_cgcm3_1']
    #cccma_cgcm3_1

    paises = {
        'GT':'1',
        'SV': '2',
        'HN':'3',
        'BZ':'4',
        'PA':'5',
        'NI':'6',
        'CR':'7',        
    }

    #tipo = 3 #Futuro temperatura
    tipo = 4 #Futuro lluvia

    for i in data:
        pais = paises.get(i)
        g = data[i]
        for e in g:
            if e != 1901:
                if len(g[e]) == 12:
                    ano = e
                    for h in range(0,12):
                        fecha = datetime.datetime(int(ano), int(h+1), 1)
                        cantidad = g[e][h]
                        #print(str(fecha)+ ' : ' + str(cantidad))
                        #db.cambio_climatico.update_or_insert(tipo_cambio_id=tipo, pais_id=pais, cantidad=cantidad, fecha=fecha)
                        #db.commit()
        print(pais)
   
#utils    
def report():
    import datetime
    if request.vars:
        pais_id = request.vars.pais
        pais_nombre = db(db.pais.id == pais_id).select(db.pais.nombre).first()
        
        info = db(db.tipo_cambio_climatico).select(db.tipo_cambio_climatico.id,db.tipo_cambio_climatico.nombre, db.tipo_cambio_climatico.descripcion)

        registros = []
        for i in info:
            tmp = ''
            tmp = db((db.cambio_climatico.tipo_cambio_id == i.id)
                    &(db.tipo_cambio_climatico.id==i.id)
                    &(db.cambio_climatico.pais_id == pais_id)
                    &(db.cambio_climatico.cantidad != None)).select(db.cambio_climatico.cantidad,
                                                                db.cambio_climatico.fecha,
                                                                db.tipo_cambio_climatico.nombre,
                                                                orderby=~db.cambio_climatico.fecha,
                                                                limitby=(0,10))
            registros.append(tmp)

        #DATOS para charts
        tipos = db(db.tipo_cambio_climatico).select(db.tipo_cambio_climatico.id)
        charts = []

        for i in tipos:
            tmp = ''
            tmp = db((db.cambio_climatico.tipo_cambio_id == i.id)
                    &(db.tipo_cambio_climatico.id==i.id)
                    &(db.cambio_climatico.pais_id == pais_id)
                    &(db.cambio_climatico.cantidad != None)).select(db.cambio_climatico.cantidad,
                                                                db.cambio_climatico.fecha,
                                                                db.tipo_cambio_climatico.nombre,
                                                                db.tipo_cambio_climatico.medicion,
                                                                orderby=~db.cambio_climatico.fecha,
                                                                limitby=(0,12)).as_list()
            charts.append(tmp)
        
        #STRING con HTML de charts
        lista_charts = []

        for chart in charts:
            fecha = []
            datos = []
            medicion = ''
            nombre = ''
            for c in chart:
                medicion = c['tipo_cambio_climatico']['medicion']
                nombre = c['tipo_cambio_climatico']['nombre']
                datos.append(c['cambio_climatico']['cantidad'])
                fecha.append(c['cambio_climatico']['fecha'].strftime('%Y-%m'))

            #Agrega los charts generados por la funcion generar_chart
            lista_charts.append(figuras_gen(fecha, datos, nombre, medicion))
            
        pais = "Cambio Climatico " + str(pais_nombre.nombre)
            
        #TABLA DE DEFINICIONES
        rows_def = [THEAD(TR(TH("Cambio",_width="40%"), 
                        TH("Descripcion",_width="60%"),
                        _bgcolor="#41b54a"
                        )
                    )
                ]
        
        for r in info:
            rows_def.append(TR(
                        TD(r.nombre,_align="center"),
                        TD(r.descripcion,_align="center"),
                        ))

        table_def = TABLE(*rows_def, _border="0", _align="left", _width="100%",_style="font-size:15px;")
        #print(table_def)
        
        #TABLA DE INFORMACION
        rows = [THEAD(TR(TH("Cambio",_width="40%"),
                        TH('Cantidad', _width="30%"),
                        TH('Fecha', _width="30%"),
                        _bgcolor="#41b54a"
                        )
                    )
                ]

        for registro in registros:
            for r in registro:
                rows.append(TR(TD(r.tipo_cambio_climatico.nombre,_align="center"),
                                TD(r.cambio_climatico.cantidad,_align="center"),
                                TD(r.cambio_climatico.fecha.strftime('%Y-%m'),_align="center"),
                            ))
        
        table = TABLE(*rows, _border="0", _align="center", _width="100%", _style="font-size:18px;")

        #Estilos
        style = '<link rel="stylesheet" href="https://bootswatch.com/4/minty/bootstrap.css"> \
                <link rel="stylesheet" href="https://bootswatch.com/4/minty/bootstrap.min.css"> \
                <style>thead{color:white; text-align:center;}img{width:80%;}</style> \
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script> \
                <meta charset="utf-8" />'
        #HEAD
        titulo = 'Ambiente'
        titulo_tabla = '<h6 style="font-color:black; font-size:10px;"><em>Informacion: Banco Mundial</em></h6><br>'

        #Salto de linea
        br = '<br/>'

        #Configurar GRID con CHARTS-PLOTS
        linear = ''
        for i in lista_charts:
            linear = linear + '<div class="col">' + str(i) +'</div>'

        #BODY HTML
        body = BODY(XML( str(XML( CENTER(H2(titulo) + H5(pais) + HR()) )) +  #Titulo y Subtitulo
                        str(XML( table_def )) + #Tabla definiciones
                        str(br*5) + #Saltos de Linea
                        str(XML( table )) + #Tabla de informacion
                        str(XML( titulo_tabla )) + #Label Tabla de informacion
                        str(XML( CENTER(H5('Cambio Climatico')) )) +  #Titulo y Subtitulo
                        str( '<div class="container"><div class="row row-cols-1 text-center">' ) + #GRID
                        str( XML(linear) ) + #CHARTS
                        str( '</div></div>') +#GRID END
                        str(XML( titulo_tabla ))  #Label Tabla de informacion
                    ))
        #HTML FINAL
        html = str('</html>') + str(HEAD(XML(style))) + str(body) + str('</html>')    

        #Generar PDF    
        import pdfkit, os

        options = {
                    'page-size':'A4', 
                    'dpi':300,
                    'encoding':'utf-8', 
                    'margin-top':'1cm',
                    'margin-bottom':'1cm',
                    'margin-left':'1cm',
                    'margin-right':'1cm'
                }

        #nombre PDF
        reporte = 'reporte-'+ str(pais.replace(' ', '')) +'.pdf'
        #print(reporte)

        #Generar PDF
        pdf = pdfkit.from_string(html, False, options=options)

        #Headers para retornar el PDF
        response.headers["Content-disposition"] = "attachment; filename=" + reporte
        response.headers['Content-Type'] ='application/pdf'
        
        return pdf
    else:
        return 'Parametros no encontrados'

#Utils
#Funcion para dibujar figuras - plots
def figuras_gen(fechas, datos, nombre, medicion):
    import matplotlib.pyplot as plt
    import io, base64
    import matplotlib.style as style
    
    x = fechas
    y = datos
    y = [round(float(i), 2) for i in y]
    x.reverse()
    y.reverse()

    style.use('ggplot')

    img = io.BytesIO()

    plt.figure(figsize=(18,8))
    plt.plot(x, y,'g')
    plt.plot(x, y, 'go')
    plt.title(nombre, fontdict={'fontsize': '18','verticalalignment': 'baseline'})
    plt.ylabel(medicion, fontdict={'fontsize': '12','verticalalignment': 'baseline'})
    plt.xlabel('Fecha')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.1)
    plt.savefig(img, format='png')
    plt.close()

    plot_url = str(base64.b64encode(img.getvalue())).replace('\'','')[1:]
    base_fig = f'<img src="data:image/png;base64, {plot_url}"/>'
    nombre = ''

    return base_fig

#Utils
def to_list(results):
        return [str(result.fecha) for result in results] if results else []