@request.restful()
def api():
    response.view = 'generic.'+request.extension
    def GET(*args,**vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)

    return dict(GET=GET)

"""@request.restful()
def mapa():
    response.view = 'generic.'+request.extension
    def GET(tablename, year):
        if not tablename == 'contaminacion_ch4':
            raise HTTP(400)
        
        c = db((db.contaminacion.pais_id == db.pais.id)
                &(db.pais.id == db.contaminacion.pais_id)                
                &(db.contaminacion.cantidad !=0)
                &(db.contaminacion.fecha == year)
                &(db.contaminacion.tipo_contaminacion == 'CH4')).select(db.contaminacion.cantidad,
                                                               db.pais.nombre,
                                                               db.pais.codigo_alt)
        #print(c)
        return dict(contaminacion = c)
    return locals()"""

@request.restful()
def contaminacion():
    response.view = 'generic.'+request.extension

    def GET(tablename, year, codigo, tipo):        
        if not tablename == 'contaminacion':
            raise HTTP(400)
        
        paises = db(db.pais).select(db.pais.id,
                                    db.pais.codigo, 
                                    db.pais.nombre)
        if str(year) != 'all':
            if len(str(year)) != 4:
                return '{"Error": "Ano incorrecto."}'

            tipos = db(db.tipo_contaminacion).select(db.tipo_contaminacion.id, db.tipo_contaminacion.nombre)

            for i in tipos:
                if str(tipo) == str(i.nombre):
                    tipo = i.id
                    break
                else:
                    return '{"Error": "Contaminacion no encontrada"}'
            
            year = year + "-01-01 00:00:00"
            response = {}

            for i in paises:
                if str(i.codigo) == str(codigo):
                    data = db((db.contaminacion.tipo_contaminacion_id == tipo)&
                            (db.contaminacion.pais_id == i.id)&
                            (db.contaminacion.fecha == year)&
                            (db.contaminacion.cantidad != 0)&
                            (db.pais.id == i.id)).select(db.contaminacion.cantidad, db.pais.nombre)
                    
                    cantidad_data = data[0]['contaminacion']['cantidad']
                    pais_data = data[0]['pais']['nombre']

                    response['cantidad'] = cantidad_data
                    response['pais'] = pais_data
                    break
            
            return dict(contaminacion = response)
        else:
            def to_list(results):
                return [str(result.contaminacion.cantidad) for result in results] if results else []

            tipos = db(db.tipo_contaminacion).select(db.tipo_contaminacion.id, db.tipo_contaminacion.nombre)

            for i in tipos:
                if str(tipo) == str(i.nombre):
                    tipo = i.id
                    break
                else:
                    return '{"Error": "Contaminacion no encontrada"}'
            
            response = {}

            for i in paises:
                if str(i.codigo) == str(codigo):
                    data = db((db.contaminacion.tipo_contaminacion_id == tipo)&
                            (db.contaminacion.pais_id == i.id)&
                            (db.contaminacion.cantidad != 0)&
                            (db.pais.id == i.id)).select(db.contaminacion.cantidad, 
                                                         db.contaminacion.fecha, 
                                                         db.pais.nombre)
                    break

            return dict(contaminacion = data)
    return locals()

@request.restful()
def cambio_climatico():
    response.view = 'generic.'+request.extension

    def GET(tablename, year, codigo, tipo):      
        if not tablename == 'cambio_climatico':
            raise HTTP(400)
        codigo_pais = codigo
        paises = db(db.pais).select(db.pais.id,
                                    db.pais.codigo, 
                                    db.pais.nombre)
        if str(year) != 'all':
            if len(str(year)) != 4:
                return '{"Error": "Ano incorrecto."}'

            tipos = db(db.tipo_cambio_climatico).select(db.tipo_cambio_climatico.id, db.tipo_cambio_climatico.identificador)

            for i in tipos:
                if str(tipo) == str(i.identificador):
                    tipo = i.id
                    break
                else:
                    return '{"Error": "Cambio no encontrado"}'
            
            year = year + "-01-01 00:00:00"
            response = {}

            for i in paises:
                if str(i.codigo) == str(codigo_pais):
                    data = db((db.cambio_climatico.tipo_cambio_id == tipo)&
                            (db.cambio_climatico.pais_id == i.id)&
                            (db.cambio_climatico.fecha == year)&
                            (db.cambio_climatico.cantidad != 0)&
                            (db.pais.id == i.id)).select(db.cambio_climatico.cantidad, db.cambio_climatico.fecha, db.pais.nombre).as_list()
                    response['cantidad'] = data[0]['cambio_climatico']['cantidad']
                    response['pais'] = data[0]['pais']['nombre']
                    break                    
            
            return dict(cambio = response)
        else:
            tipos = db(db.tipo_cambio_climatico).select(db.tipo_cambio_climatico.id, db.tipo_cambio_climatico.identificador)

            for i in tipos:
                if str(tipo) == str(i.identificador):
                    tipo = i.id
                    break
                else:
                    return '{"Error": "Cambio no encontrado"}'
            
            response = {}

            for i in paises:
                if str(i.codigo) == str(codigo):
                    data = db((db.cambio_climatico.tipo_cambio_id == tipo)&
                            (db.cambio_climatico.pais_id == i.id)&
                            (db.cambio_climatico.cantidad != 0)&
                            (db.pais.id == i.id)).select(db.cambio_climatico.cantidad, 
                                                         db.cambio_climatico.fecha, 
                                                         db.pais.nombre)
                    break

            return dict(cambio = data)

    return locals()


@request.restful()
def imagen_contaminacion():
    response.view = 'generic.' + request.extension

    def GET(tablename, tipo, fecha):
        tipo_img = ''

        if not tablename == 'imagen_contaminacion':
            raise HTTP(400)
        
        #TIPO
        tipos = db((db.tipo_contaminacion_imagen.id)
                &(db.tipo_contaminacion_imagen.identificador == str(tipo))).select(db.tipo_contaminacion_imagen.id, 
                                                                                   db.tipo_contaminacion_imagen.identificador).first()

        if tipos == None:
            return '{"Error": "Tipo de contaminacion incorrecto."}'
        else:
            tipo_img = tipos.id
        
        if tipo_img == '' or tipo_img == 0:
            return '{"Error": "Tipo de contaminacion incorrecto."}'

        
        if int(fecha[:4]) < 2009 or int(fecha[:4]) > 2018:
            return '{"Error": "Fecha incorrecta."}'

        fecha = fecha + '-01 00:00:00'        

        datos = db((db.image_contaminacion.tipo_cambio_imagen_id == tipo_img)
                &(db.image_contaminacion.fecha == fecha)
                &(db.tipo_contaminacion_imagen.id == tipo_img)).select(db.image_contaminacion.fecha,
                                                                        db.image_contaminacion.imagen,
                                                                        db.tipo_contaminacion_imagen.nombre)
        
        return dict(contaminacion = datos)

    return locals()