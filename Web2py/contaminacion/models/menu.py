# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# MENU - USER
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Contaminacion'), False, URL('contaminacion','index')),
    (T('Calidad del Aire'), False, URL('air', 'index')),
    (T('Cambio Climatico'), False, URL('cambioclimatico', 'index')),
    (T('Datos'), False, URL('data','index')),
    #(T('Ingresar / Registrarse'), False, URL('admin', 'default', 'site')),
]

response.title_user = "Ambiente"
response.title = "Ambiente"
# ----------------------------------------------------------------------------------------------------------------------
# MENU - ADMIN
# ----------------------------------------------------------------------------------------------------------------------

response.menu_admin = [
    (T('Contenido'), False, None, [
        (T('Contenido'), False, URL('admins', 'contenido')),
        (T('Tipo Contenido'), False, URL('admins', 'tipo_contenido')),
        (T('Conceptos'), False, URL('admins', 'concepto')),
    ]),  
    (T('Calidad del Aire'), False, None, [
        (T('Alertas'), False, URL('admins', 'alerta')),
        (T('Calidad del Aire - Paises'), False, URL('admins', 'calidad_pais')),
    ]),    
    (T('Contaminacion'), False, None, [
        (T('Datos'), False, URL('admins','contaminacion')),
        (T('Tipo'), False, URL('admins', 'tipo_contaminacion')),
        (T('Tipo Imagen'), False, URL('admins', 'tipo_imagen_contaminacion')),
        (T('Imagen'), False, URL('admins', 'contaminacion_imagen')),
    ]),
    (T('Cambio Climatico'), False, None, [
        (T('Datos'), False, URL('admins','cambioclimatico')),
        (T('Tipo'), False, URL('admins', 'tipo_cambio_climatico')),
    ]),
    (T('Paises'), False, URL('admins', 'pais')),    
    (T('Usuarios'), False, None, [
        (T('Usuarios'), False, URL('admins', 'usuarios')),
        (T('Roles'), False, URL('admins', 'usuarios_roles')),
    ]),
]

response.title_admin = "Administracion"

response.google_analytics_id = "250218557"

# ----------------------------------------------------------------------------------------------------------------------
# MENU - DATA
# ----------------------------------------------------------------------------------------------------------------------
response.menu_data = [
    (T('API'), False, URL('data','doc')),
]

response.title_data = "API"

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        #(T('My Sites'), False, URL('admin', 'default', 'site')),

    ]

