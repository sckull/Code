####################################################################
#                           Contaminacion                          #
####################################################################
def index():
    contenido = db(db.contenido.tipo_contenido_id == 1).select(db.contenido.titulo, 
                                                            db.contenido.contenido,
                                                            db.contenido.imagen_con)
    paises = db(db.pais).select()
    #indicadores = ['EN.ATM.CO2E.PC','EN.ATM.NOXE.ZG','EN.ATM.METH.EG.KT.CE','EN.ATM.GHGO.KT.CE']
    #efe = [1, 2, 3, 4]
    #for i in efe:
    #    api_contaminacion(indicadores[i-1],i)
    
    return dict(contenido = contenido, paises = paises)

def country():
    pais        = request.vars.pais
    nombre_pais = db(db.pais.id == pais).select(db.pais.nombre).first()    
    contaminante  = db(db.contaminacion.pais_id == pais).select(db.contaminacion.tipo_contaminacion_id, 
                                                                groupby=db.contaminacion.tipo_contaminacion_id)
    contaminacion = {}
    for c in contaminante:
        tmp = db((db.contaminacion.pais_id == pais)&
                 (db.contaminacion.tipo_contaminacion_id == c.tipo_contaminacion_id)).select(db.contaminacion.cantidad,
                                                                                       db.contaminacion.fecha,
                                                                                       orderby=db.contaminacion.fecha).as_list()
        fecha = []
        valor = []
        for i in tmp:
            if i['cantidad'] != None:
                f = i['fecha'].strftime('%Y')
                fecha.append(f)            
                valor.append(i['cantidad'])        
        descr = db(db.tipo_contaminacion.id == c.tipo_contaminacion_id).select(db.tipo_contaminacion.nombre).first()
        
        descripcion = db(db.tipo_contaminacion.id == c.tipo_contaminacion_id).select(db.tipo_contaminacion.descripcion).first()
        
        contaminacion[descr['nombre']] = {'fecha':fecha, 'valor':valor, 'descripcion':descripcion['descripcion']}
    
    conceptos = db(db.concepto).select()

    return dict(contaminacion = contaminacion, nombre_pais = nombre_pais.nombre, conceptos = conceptos)

def centroamerica():
    tipos = db(db.tipo_contaminacion_imagen).select()
    conceptos = db(db.concepto).select()
    
    imagen = []
    for i in tipos:
        tmp = db(db.image_contaminacion.tipo_cambio_imagen_id == i.id).select(db.image_contaminacion.imagen, 
                                                                              orderby=db.image_contaminacion.fecha).first()
        imagen.append(tmp)    
    return dict(tipos = tipos, imagen = imagen, conceptos = conceptos)
       
def download():
        return response.download(request, db)

def contaminante_ca():
    contaminante = request.vars.tipo
    imagenes = db(db.image_contaminacion.tipo_cambio_imagen_id == contaminante).select(orderby=db.image_contaminacion.fecha)
    
    fechas = db(db.image_contaminacion.tipo_cambio_imagen_id == contaminante).select(db.image_contaminacion.fecha, orderby=~db.image_contaminacion.fecha)
    fechas = sorted(set(to_list(fechas)))
    fechas = sorted([x[:4] for x in fechas])
    fechas.reverse()

    return dict(imagenes = imagenes, fechas = set(fechas), contaminante = contaminante)


def to_list(results):
        return [str(result.fecha) for result in results] if results else []

#LOAD FILES
def ca_atmosferica():
    fechas = db((db.contaminacion.tipo_contaminacion.id == db.tipo_contaminacion.id) &(db.tipo_contaminacion== 'CH4')&(db.contaminacion.cantidad != 0)).select(db.contaminacion.fecha, orderby=db.contaminacion.fecha)
    fechas = list(set(to_list(fechas)))
    fechas.sort()
    #print(fechas)
    return dict(fechas = fechas)

#worldBankAPI(p.codigo,'EN.ATM.CO2E.PC','CO2')
#worldBankAPI(p.codigo,'EN.ATM.NOXE.ZG','NO')
#worldBankAPI(p.codigo,'EN.ATM.METH.EG.KT.CE','CH4')
#worldBankAPI(p.codigo,'EN.ATM.GHGO.KT.CE','GEI')

#indicadores = ['EN.ATM.CO2E.PC','EN.ATM.NOXE.ZG','EN.ATM.METH.EG.KT.CE','EN.ATM.GHGO.KT.CE']

def api_contaminacion(indicador, tipo_id=0):
    import wbpy, datetime
    from pprint import pprint

    api = wbpy.IndicatorAPI()

    iso_country_codes = ['GTM', 'SLV', 'HND', 'BLZ', 'PAN', 'NIC', 'CRI']    

    dataset = api.get_dataset(indicador, iso_country_codes, date="1960:2020")
    data = dataset.as_dict()

    paises = {
        'GT':'1',
        'SV':'2',
        'HN':'3',
        'BZ':'4',
        'PA':'5',
        'NI':'6',
        'CR':'7',        
    }
    tipo = tipo_id    
    for d in data:
        pais = paises.get(d)
        g = data[d]
        for i in g:
            if i != 1901:
                fecha = datetime.datetime(int(i), 1, 1)
                cantidad = g[i]
                #print(str(fecha) +' : '+ str(cantidad)+' : '+str(tipo))
                #db.contaminacion.update_or_insert(tipo_contaminacion_id=tipo, pais_id=pais, cantidad=cantidad, fecha=fecha)
                #db.commit() 
        print(pais)

def report():
    import datetime
    if request.vars:
        pais_id = request.vars.pais_id
        ano = request.vars.ano
        #1986-01-01 00:00:00
        date_str = str(ano) +'-01-01 00:00:00'
    
        registros = db((db.contaminacion.pais_id == pais_id)
                    &(db.contaminacion.fecha == date_str)
                    &(db.pais.id == pais_id)
                    &(db.contaminacion.tipo_contaminacion_id == db.tipo_contaminacion.id)).select(db.pais.nombre,
                                                                                                    db.contaminacion.cantidad,
                                                                                                    db.contaminacion.fecha,
                                                                                                    db.tipo_contaminacion.nombre,
                                                                                                    db.tipo_contaminacion.descripcion)

        #DATOS para charts
        tipos = db(db.tipo_contaminacion).select(db.tipo_contaminacion.id)
        charts = []

        for i in tipos:
            tmp = ''
            tmp = db((db.contaminacion.tipo_contaminacion_id == i.id)
                    &(db.tipo_contaminacion.id==i.id)
                    &(db.contaminacion.pais_id == pais_id)
                    &(db.contaminacion.cantidad != None)).select(db.contaminacion.cantidad,
                                                                db.contaminacion.fecha,
                                                                db.tipo_contaminacion.nombre,
                                                                orderby=~db.contaminacion.fecha,
                                                                limitby=(0,10)).as_list()
            charts.append(tmp)
        
        #STRING con HTML de charts
        #lista_charts = ''
        lista_charts = []

        for chart in charts:
            fecha = []
            datos = []
            nombre = ''
            for c in chart:            
                nombre = c['tipo_contaminacion']['nombre']
                datos.append(c['contaminacion']['cantidad'])
                fecha.append(c['contaminacion']['fecha'].strftime('%Y'))

            #Agrega los charts generados por la funcion generar_chart
            lista_charts.append(figuras_gen(fecha, datos, nombre))
            
        pais = "Contaminacion " + str(db(db.pais.id == pais_id).select(db.pais.nombre).first().nombre)
            
        #TABLA DE DEFINICIONES
        rows_def = [THEAD(TR(TH("Contaminante",_width="40%"), 
                        TH("Descripcion",_width="60%"),
                        _bgcolor="#41b54a"
                        )
                    )
                ]
        
        for r in registros:
            rows_def.append(TR(
                        TD(r.tipo_contaminacion.nombre,_align="center"),
                        TD(r.tipo_contaminacion.descripcion,_align="center"),
                        )
                        )
        table_def = TABLE(*rows_def, _border="0", _align="left", _width="100%",_style="font-size:15px;")
        #print(table_def)
        
        #TABLA DE INFORMACION
        rows = [THEAD(TR(TH("Contaminante",_width="33%"),
                        TH('Cantidad', _width="33%"),
                        TH('Fecha', _width="33%"),
                        _bgcolor="#41b54a"
                        )
                    )
                ]

        for registro in registros:
            if registro.contaminacion.cantidad != None:
                rows.append(TR(
                                TD(registro.tipo_contaminacion.nombre,_align="center"),
                                TD(registro.contaminacion.cantidad,_align="center"),
                                TD(registro.contaminacion.fecha.strftime('%Y'),_align="center"),
                            ))
            else:
                rows.append(TR(
                                TD('No existe Registro',_align="center"),
                                TD('No existe Registro',_align="center"),
                                TD(registro.contaminacion.fecha.strftime('%Y'),_align="center"),
                            ))
        table = TABLE(*rows, _border="0", _align="center", _width="100%", _style="font-size:18px;")

        #Estilos
        style = '<link rel="stylesheet" href="https://bootswatch.com/4/minty/bootstrap.css"> \
                <link rel="stylesheet" href="https://bootswatch.com/4/minty/bootstrap.min.css"> \
                <style>thead{color:white; text-align:center;}img{width:100%;}table{text-align:center;}</style> \
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

        #print(linear)

        #BODY HTML
        body = BODY(XML( str(XML( CENTER(H2(titulo) + H5(pais) + HR()) )) +  #Titulo y Subtitulo
                        str(XML( table_def )) + #Tabla definiciones
                        str(br*10) + #Saltos de Linea
                        str(XML( table )) + #Tabla de informacion
                        str(XML( titulo_tabla )) + #Label Tabla de informacion
                        str(XML( CENTER(H5('Contaminacion en los ultimos Años')) )) +  #Titulo y Subtitulo
                        str( '<div class="container"><div class="row row-cols-2">' ) + #GRID
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
                    'dpi':200,
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

#Funcion para dibujar figuras - plots
def figuras_gen(fechas, datos, nombre):
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

    plt.figure()
    plt.plot(x, y,'g')
    plt.plot(x, y, 'go')
    plt.title(nombre, fontdict={'fontsize': '18','verticalalignment': 'baseline'})
    plt.ylabel('Tons', fontdict={'fontsize': '12','verticalalignment': 'baseline'})
    plt.xlabel('Años')
    plt.grid(True, alpha=0.1)
    plt.savefig(img, format='png')
    #plt.show()
    plt.close()

    plot_url = str(base64.b64encode(img.getvalue())).replace('\'','')[1:]
    base_fig = f'<img src="data:image/png;base64, {plot_url}"/>'

    return base_fig
    
def generar_reporte():
    paises = db(db.pais).select(db.pais.id, db.pais.nombre)

    fechas = db(db.contaminacion.tipo_contaminacion_id == db.tipo_contaminacion.id).select(db.contaminacion.fecha, 
                                                                                           orderby=~db.contaminacion.fecha)
    fechas = sorted(set(to_list(fechas)))
    fechas = sorted([x[:4] for x in fechas])
    fechas.reverse()
    return dict(paises = paises, fechas = fechas)

def reporte_ca():
    if request.vars:
        contaminante = request.vars.contaminante
        fecha = request.vars.ano        
        #1986-01-01 00:00:00
        #date_str = str(ano) +'-01-01 00:00:00'
  
        
        #DEFINICIONES
        registros = db(db.tipo_contaminacion_imagen.id == contaminante).select(db.tipo_contaminacion_imagen.nombre, 
                                                                                db.tipo_contaminacion_imagen.descripcion)
        
        tipo_con = db(db.tipo_contaminacion_imagen.id == contaminante).select(db.tipo_contaminacion_imagen.nombre).first()
        pais = "Contaminacion " + str(tipo_con.nombre)
        print(pais)
            
        #TABLA DE DEFINICIONES
        rows_def = [THEAD(TR(TH("Contaminante",_width="40%"), 
                        TH("Descripcion",_width="60%"),
                        _bgcolor="#41b54a"
                        )
                    )
                ]
        
        for r in registros:
            rows_def.append(TR(
                        TD(r.nombre,_align="center"),
                        TD(r.descripcion,_align="center"),
                        ))

        table_def = TABLE(*rows_def, _border="0", _align="left", _width="100%",_style="font-size:15px;")
        

        #IMAGENES
        imagenes = db((db.image_contaminacion.tipo_cambio_imagen_id == contaminante)
                    &(db.tipo_contaminacion_imagen.id == contaminante)).select(db.image_contaminacion.fecha,
                                                                                db.image_contaminacion.imagen,
                                                                                db.tipo_contaminacion_imagen.nombre,
                                                                                db.tipo_contaminacion_imagen.descripcion,
                                                                                orderby=db.image_contaminacion.fecha)
                

        #Estilos
        style = '<link rel="stylesheet" href="https://bootswatch.com/4/minty/bootstrap.css"> \
                <link rel="stylesheet" href="https://bootswatch.com/4/minty/bootstrap.min.css"> \
                <style>thead{color:white; text-align:center;}img{width:100%;}table{text-align:center;}</style> \
                <meta charset="utf-8" />'
        #HEAD
        titulo = 'Ambiente'
        titulo_tabla = '<h6 style="font-color:black; font-size:10px;"><em>Informacion: Banco Mundial</em></h6><br>'

        #Salto de linea
        br = '<br/>'

        #Configurar GRID con IMAGENES
        import os, io, base64
        linear = ''
        for i in imagenes:
            tmp = ''
            tmp = (i.image_contaminacion.fecha).strftime('%Y')
            if str(fecha) in tmp:
                direccion = URL('contaminacion', 'download', args=i.image_contaminacion.imagen)                

                #Directorio de imagenes
                dir_path = os.path.dirname(os.path.realpath(__file__))
                stream = open(dir_path[:-11]+'uploads/'+str(i.image_contaminacion.imagen), 'rb')

                #Crear imagen en Base64
                base = str(base64.b64encode(stream.read())).replace('\'','')[1:]
                base_fig = f'<img src="data:image/png;base64, {base}"/>'
                
                #Agregar imagen a columna
                linear = linear + '<div class="col">' + str(base_fig) + '</div>'

        contaminacion_titulo = CENTER(H5( 'Contaminacion - ' + str(fecha) ))
        #BODY HTML
        body = BODY(XML( str(XML( CENTER(H2(titulo) + H5(pais) + HR()) )) +  #Titulo y Subtitulo
                        str(XML( table_def )) + #Tabla definiciones
                        str(HR()) + #Saltos de Linea                        
                        str(XML( contaminacion_titulo )) +  #Titulo y Subtitulo
                        str( '<div class="container"><div class="row row-cols-2">' ) + #GRID
                        str( XML(linear) ) + #CHARTS
                        str( '</div></div>') #GRID END
                    ))
        #HTML FINAL
        html = str('</html>') + str(HEAD(XML(style))) + str(body) + str('</html>')    

        #Generar PDF    
        import pdfkit, os

        options = {
                    'page-size':'A4', 
                    'dpi':200,
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