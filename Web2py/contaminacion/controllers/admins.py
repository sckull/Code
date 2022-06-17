@auth.requires_login()
def index():
    return dict()

####################################################################
#                               PAIS                               #
####################################################################
@auth.requires_login()
def pais():
    paises = db(db.pais.id > 0).select(db.pais.ALL)
    return dict(paises = paises)

@auth.requires_login()
def editar_pais():
    pais = request.vars.pais
    nombre = db(db.pais.id == pais).select(db.pais.nombre).first()
    form = SQLFORM(db.pais, 
                    record=pais,
                   _class='form-horizontal', 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('pais'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(pais=pais, 
                nombre=nombre, 
                form=form)

@auth.requires_login()
def eliminar_pais():
    db(db.pais.id == request.vars.pais).delete()
    session.flash = T('Eliminado')
    redirect(URL('pais'))

####################################################################
#                          CONTENIDO                               #
####################################################################
@auth.requires_membership('admin')
def contenido():
    contenidos = db((db.contenido.tipo_contenido_id==db.tipo_contenido.id)).select()
    return dict(contenidos = contenidos)

@auth.requires_membership('admin')
def editar_contenido():
    contenido = request.vars.contenido_id
    titulo = db(db.contenido.id == contenido).select(db.contenido.titulo).first()
    form = SQLFORM(db.contenido, 
                    record=contenido,
                   _class='form-horizontal', 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('contenido'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(contenido=contenido, 
                titulo=titulo, 
                form=form)

@auth.requires_membership('admin')
def eliminar_contenido():
    db(db.contenido.id == request.vars.contenido_id).delete()
    session.flash = T('Eliminado')
    redirect(URL('contenido'))

####################################################################
#                          TIPO CONTENIDO                          #
####################################################################
@auth.requires_login()
def tipo_contenido():
    contenidos = db(db.tipo_contenido).select()
    return dict(contenidos = contenidos)

@auth.requires_login()
def editar_tipo_contenido():
    contenido = request.vars.tipo_contenido
    titulo = db(db.tipo_contenido.id == contenido).select(db.tipo_contenido.nombre).first()
    form = SQLFORM(db.tipo_contenido, 
                    record=contenido,
                   _class='form-horizontal', 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('tipo_contenido'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(contenido=contenido, 
                titulo=titulo, 
                form=form)

@auth.requires_login()
def eliminar_tipo_contenido():
    db(db.contenido.id == request.vars.contenido).delete()
    session.flash = T('Eliminado')
    redirect(URL('contenido'))

####################################################################
#                        CALIDAD DEL AIRE                          #
####################################################################
@auth.requires_login()
def calidad_pais():
    paises_calidad = db(db.calidadAire.pais_id == db.pais.id).select(db.calidadAire.id, 
                                                                     db.calidadAire.activo,
                                                                     db.pais.nombre)
    return dict(paises_calidad = paises_calidad)

@auth.requires_login()
def editar_calidad_pais():
    pais_calidad = request.vars.pais_calidad
    titulo = db(db.pais.id == pais_calidad).select(db.pais.nombre).first()

    form = SQLFORM(db.calidadAire, 
                    record=pais_calidad,
                   _class='form-horizontal', 
                   showid=False)

    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('calidad_pais'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(pais_calidad=pais_calidad, 
                titulo=titulo, 
                form=form)

@auth.requires_login()
def eliminar_calidad_pais():
    db(db.calidadAire.id == request.vars.pais_calidad).delete()
    session.flash = T('Eliminado')
    redirect(URL('calidad_pais'))

####################################################################
#                    ALERTA - CALIDAD DEL AIRE                     #
####################################################################
@auth.requires_login()
def alerta():
    alertas = db(db.alerta).select()
    return dict(alertas = alertas)

@auth.requires_login()
def editar_alerta():
    alerta = request.vars.alerta
    nombre = db(db.alerta.id == alerta).select(db.alerta.nombre).first()
    
    form = SQLFORM(db.alerta, 
                    record=alerta,
                   _class='form-horizontal', 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('alerta'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(alerta=alerta, 
                nombre=nombre, 
                form=form)

@auth.requires_login()
def eliminar_alerta():
    db(db.alerta.id == request.vars.alerta).delete()
    session.flash = T('Eliminado')
    redirect(URL('contenido'))

####################################################################
#                       TIPO CONTAMINACION                         #
####################################################################
@auth.requires_login()
def tipo_contaminacion():
    datos = db(db.tipo_contaminacion).select()
    return dict(datos = datos)

@auth.requires_login()
def editar_tipo_contaminacion():
    tipo_id = request.vars.tipo_id
    titulo = db(db.tipo_contaminacion.id == tipo_id).select(db.tipo_contaminacion.nombre).first()

    form = SQLFORM(db.tipo_contaminacion, 
                    record=tipo_id,
                   _class='form-horizontal', 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('tipo_contaminacion'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(tipo_id=tipo_id, 
                titulo=titulo, 
                form=form)

@auth.requires_login()
def eliminar_tipo_contaminacion():
    db(db.contaminacion.id == request.vars.tipo_id).delete()
    session.flash = T('Eliminado')
    redirect(URL('tipo_contaminacion'))

####################################################################
#                          CONTAMINACION                           #
####################################################################
@auth.requires_membership('admin')
def contaminacion():
    contaminacion = db((db.contaminacion.tipo_contaminacion_id==db.tipo_contaminacion.id)&
                       (db.contaminacion.pais_id == db.pais.id)).select(db.pais.nombre, 
                                                                        db.contaminacion.ALL, 
                                                                        db.tipo_contaminacion.descripcion)    
    return dict(contaminacion = contaminacion)

@auth.requires_membership('admin')
def editar_contaminacion():
    contaminacion = request.vars.contaminacion_id
    titulo = db(db.contaminacion.id == contaminacion).select(db.contaminacion.fecha).first()
    form = SQLFORM(db.contaminacion, 
                    record=contaminacion,
                   _class='form-horizontal', 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('contaminacion'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(contaminacion=contaminacion, 
                titulo=titulo, 
                form=form)

@auth.requires_membership('admin')
def eliminar_contaminacion():
    db(db.contaminacion.id == request.vars.contaminacion_id).delete()
    session.flash = T('Eliminado')
    redirect(URL('contaminacion'))

####################################################################
#                     TIPO CAMBIO CLIMATICO                        #
####################################################################
@auth.requires_login()
def tipo_cambio_climatico():
    datos = db(db.tipo_cambio_climatico).select()
    return dict(datos = datos)

@auth.requires_login()
def editar_tipo_cambio_climatico():
    cambio_id = request.vars.cambio_id
    titulo = db(db.tipo_cambio_climatico.id == cambio_id).select(db.tipo_cambio_climatico.nombre).first()

    form = SQLFORM(db.tipo_cambio_climatico, 
                    record=cambio_id,
                   _class='form-horizontal', 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('tipo_cambio_climatico'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(cambio_id=cambio_id, 
                titulo=titulo, 
                form=form)

@auth.requires_login()
def eliminar_tipo_cambio_climatico():
    db(db.tipo_cambio_climatico.id == request.vars.cambio_id).delete()
    session.flash = T('Eliminado')
    redirect(URL('tipo_cambio_climatico'))

####################################################################
#                        CAMBIO CLIMATICO                          #
####################################################################
@auth.requires_membership('admin')
def cambioclimatico():
    datos = db((db.cambio_climatico.tipo_cambio_id==db.tipo_cambio_climatico.id)&
                       (db.cambio_climatico.pais_id == db.pais.id)).select( db.pais.nombre, 
                                                                            db.cambio_climatico.ALL, 
                                                                            db.tipo_cambio_climatico.descripcion)
    return dict(datos = datos)

@auth.requires_membership('admin')
def editar_cambioclimatico():
    cambio_id = request.vars.cambio_id
    titulo = db(db.cambio_climatico.id == cambio_id).select(db.cambio_climatico.fecha).first()

    form = SQLFORM(db.cambio_climatico, 
                    record=cambio_id,
                   _class='form-horizontal', 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('cambioclimatico'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(cambio_id=cambio_id, 
                titulo=titulo, 
                form=form)

@auth.requires_membership('admin')
def eliminar_cambioclimatico():
    db(db.contenido.id == request.vars.cambio_id).delete()
    session.flash = T('Eliminado')
    redirect(URL('cambioclimatico'))

####################################################################
#                          CONCEPTOS                               #
####################################################################
@auth.requires_login()
def concepto():
    conceptos = db(db.concepto).select()
    return dict(conceptos = conceptos)

@auth.requires_login()
def editar_concepto():
    concepto = request.vars.concepto_id
    nombre = db(db.concepto.id == concepto).select(db.concepto.nombre).first()    
    form = SQLFORM(db.concepto, 
                    record=concepto,
                   _class='form-horizontal', 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('concepto'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(concepto=concepto, 
                nombre=nombre, 
                form=form)

@auth.requires_login()
def eliminar_concepto():
    db(db.concepto.id == request.vars.concepto_id).delete()
    session.flash = T('Eliminado')
    redirect(URL('concepto'))

####################################################################
#                        USUARIOS - ROLES                          #
####################################################################

@auth.requires_login()
def usuarios():
    grid = SQLFORM.grid(db.auth_membership, exportclasses = dict(xml=False, 
                                                            html=False, 
                                                            csv=False, 
                                                            csv_with_hidden_cols=False, 
                                                            json=False, 
                                                            tsv_with_hidden_cols=False, 
                                                            tsv=False))
    return locals()

@auth.requires_login()
def usuarios_roles():
    grid = SQLFORM.grid(db.auth_group, exportclasses = dict(xml=False, 
                                                            html=False, 
                                                            csv=False, 
                                                            csv_with_hidden_cols=False, 
                                                            json=False, 
                                                            tsv_with_hidden_cols=False, 
                                                            tsv=False))    
    return locals()

####################################################################
#                    TIPO IMAGENES CONTAMINACION                   #
####################################################################
#tipo_contaminacion_imagen
@auth.requires_login()
def tipo_imagen_contaminacion():
    data = db(db.tipo_contaminacion_imagen).select()
    return dict(data = data)

@auth.requires_login()
def editar_tipo_contaminacion_imagen():
    tipo_id = request.vars.tipo_id
    nombre = db(db.tipo_contaminacion_imagen.id == tipo_id).select(db.tipo_contaminacion_imagen.nombre).first() 

    form = SQLFORM(db.tipo_contaminacion_imagen, 
                    record=tipo_id,
                   _class='form-horizontal', 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('tipo_contaminacion_imagen'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(tipo_id=tipo_id, 
                nombre=nombre, 
                form=form)

@auth.requires_login()
def eliminar_tipo_contaminacion_imagen():
    db(db.tipo_contaminacion_imagen.id == request.vars.tipo_id).delete()
    session.flash = T('Eliminado')
    redirect(URL('tipo_contaminacion_imagen'))

####################################################################
#                        IMAGENES CONTAMINACION                    #
####################################################################
@auth.requires_login()
def download():
        return response.download(request, db)

@auth.requires_login()
def contaminacion_imagen():
    data = db(db.image_contaminacion.tipo_cambio_imagen_id == db.tipo_contaminacion_imagen.id).select(db.tipo_contaminacion_imagen.nombre,
                                                                                                      db.tipo_contaminacion_imagen.descripcion,
                                                                                                      db.image_contaminacion.id,
                                                                                                      db.image_contaminacion.fecha)
    return dict(data = data)

@auth.requires_login()
def editar_imagen_contaminacion():    
    img_id = request.vars.img_id
    nombre = db(db.image_contaminacion.id == img_id).select(db.image_contaminacion.fecha).first() 

    form = SQLFORM(db.image_contaminacion, 
                    record=img_id,
                   _class='form-horizontal',
                   upload=URL('download'), 
                   showid=False)
    if form.process().accepted:
        session.flash = T('Guardado')
        redirect(URL('contaminacion_imagen'))
    elif form.errors:
        response.flash = T('Verifica tus datos')
    return dict(img_id=img_id, 
                nombre=nombre, 
                form=form)

@auth.requires_login()
def eliminar_imagen_contaminacion():
    db(db.image_contaminacion.id == request.vars.img_id).delete()
    session.flash = T('Eliminado')
    redirect(URL('editar_imagen_contaminacion'))

def insertar_imagen():
    import glob, datetime

    path = '/home/sckull/Desktop/COPERNICUS/COLUMNA_DIOXIDO_NITROGENO/'
    files = glob.glob(path+'*')
    tipo = 3    

    for i in files:
        fecha = i.replace('/home/sckull/Desktop/COPERNICUS/COLUMNA_DIOXIDO_NITROGENO/mapa-', '').replace('-centroamerica.png', '')
        fecha = datetime.datetime.strptime(fecha+'-01', '%Y-%m-%d')

        #Insertar Imagen - https://bit.ly/38wyNjp
        stream = open(i, 'rb')
        #db.image_contaminacion.update_or_insert(tipo_cambio_imagen_id=tipo, imagen=db.image_contaminacion.imagen.store(stream, i), fecha=fecha)
        #db.commit()
    