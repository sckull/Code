#-*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
#mail.settings.server = 'smtp.gmail.com:465' if request.is_local else configuration.get('smtp.server')
mail.settings.server = 'loggin' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)




####################################################################
#                               PAIS                               #
####################################################################
#3 letter ISO 3166-1 alpha-3 code
#2 letter ISO 3166-1 alpha-2 code

db.define_table('pais',
    Field('nombre',         'string',     label=T('Nombre')),
    Field('codigo',         'string',     label=T('Codigo de Pais (ISO 3166-1 - alpha-2)')),
    Field('codigo_alt',     'string',     label=T('Codigo de Pais (ISO 3166-1 - alpha-3)')),
    Field('longitud',       'string',     label=T('Longitud')),
    Field('latitud',        'string',     label=T('Latitud')),
    format = '%(nombre)s'
)
db.pais.nombre.requires = IS_NOT_EMPTY()

####################################################################
#                        Calidad del Aire                          #
####################################################################
db.define_table('calidadAire',
    Field('pais_id', 'reference pais',          label=T('Pais')),    
    Field('activo', 'boolean',                  label=T('Informacion Disponible')),
)

db.calidadAire.pais_id.requires   = IS_IN_DB(db, 'pais.id', '%(nombre)s', zero=T('choose one'))


####################################################################
#                ALERTA - Calidad del Aire                         #
####################################################################

db.define_table('alerta',
    Field('nombre',         'string',     label=T('Nombre')),
    Field('descripcion',    'text',     label=T('Descripcion')),
    Field('rango_menor',    'string',     label=T('Rango de Alerta Min')),
    Field('rango_mayor',    'string',     label=T('Rango de Alerta Max')),
    format = '%(nombre)s'
)
db.alerta.nombre.requires = IS_NOT_EMPTY()
db.alerta.rango_menor.requires = IS_NOT_EMPTY()
db.alerta.rango_mayor.requires = IS_NOT_EMPTY()

####################################################################
#                     TIPO DE CONTAMINACION                        #
####################################################################
db.define_table('tipo_contaminacion',
    Field('nombre',                'string',     label=T('Nombre')),
    Field('identificador',         'string',     label=T('Identificador')),
    Field('descripcion',           'string',     label=T('Descripcion')),
    format = '%(nombre)s'
)
db.tipo_contaminacion.nombre.requires = IS_NOT_EMPTY()
db.tipo_contaminacion.identificador.requires = IS_NOT_EMPTY()
db.tipo_contaminacion.descripcion.requires = IS_NOT_EMPTY()

####################################################################
#                         Contaminacion                            #
####################################################################
db.define_table('contaminacion',
    Field('pais_id',                    'reference pais',                   label=T('Pais')),
    Field('tipo_contaminacion_id',      'reference tipo_contaminacion',     label=T('Tipo Contaminacion')),    
    Field('cantidad',                                                       label=T('Cantidad')),
    Field('fecha',                      'datetime',                         label=T('Fecha')),
)

db.contaminacion.pais_id.requires                = IS_IN_DB(db, 'pais.id', '%(nombre)s', zero=T('choose one'))
db.contaminacion.tipo_contaminacion_id.requires  = IS_IN_DB(db, 'tipo_contaminacion.id', '%(nombre)s', zero=T('choose one'))
db.contaminacion.cantidad.requires               = IS_NOT_EMPTY()
db.contaminacion.fecha.requires                  = IS_DATETIME(format=T('%Y-%m-%d'), error_message='must be YYYY-MM-DD!')

####################################################################
#                        TIPO DE CONTENIDO                         #
####################################################################
db.define_table('tipo_contenido',
    Field('nombre',         'string',     label=T('Nombre')),
    format = '%(nombre)s'
)
db.tipo_contenido.nombre.requires = IS_NOT_EMPTY()

####################################################################
#                           CONTENIDO                              #
####################################################################
db.define_table('contenido',
    Field('tipo_contenido_id', 'reference tipo_contenido',   label=T('Tipo de contenido')),    
    Field('titulo',            'string',                     label=T('Titulo')),    
    Field('contenido',         'text',                       label=T('Contenido')),
    Field('imagen_con',        'string',                     label=T('Imagen')),
    format = '%(titulo)s'    
)

db.contenido.tipo_contenido_id.requires = IS_IN_DB(db, 'tipo_contenido.id', '%(nombre)s', zero=T('choose one'))
db.contenido.titulo.requires            = IS_NOT_EMPTY()
db.contenido.contenido.requires         = IS_NOT_EMPTY()
db.contenido.imagen_con.requires        = IS_EMPTY_OR(IS_URL())

####################################################################
#                    TIPO DE CAMBIO CLIMATICO                      #
####################################################################
db.define_table('tipo_cambio_climatico',
    Field('nombre',        'string',     label=T('Nombre')),
    Field('identificador', 'string',     label=T('Identificador')),
    Field('descripcion',   'string',     label=T('Descripcion')),
    Field('medicion',   'string',     label=T('Descripcion')),
    format = '%(nombre)s'
)

db.tipo_cambio_climatico.nombre.requires = IS_NOT_EMPTY()
db.tipo_cambio_climatico.identificador.requires = IS_NOT_EMPTY()
db.tipo_cambio_climatico.identificador.medicion = IS_NOT_EMPTY()


####################################################################
#                         CAMBIO CLIMATICO                         #
####################################################################

db.define_table('cambio_climatico',
    Field('tipo_cambio_id',             'reference tipo_cambio_climatico',   label=T('Tipo de Cambio Climatico')),
    Field('pais_id',                    'reference pais',                    label=T('Pais')),
    Field('cantidad',                                                        label=T('Cantidad')),
    Field('fecha',                      'datetime',                          label=T('Fecha')),
)

db.cambio_climatico.tipo_cambio_id.requires = IS_IN_DB(db, 'tipo_cambio_climatico.id', '%(nombre)s', zero=T('choose one'))
db.cambio_climatico.pais_id.requires        = IS_IN_DB(db, 'pais.id', '%(nombre)s', zero=T('choose one'))
db.cambio_climatico.cantidad.requires       = IS_NOT_EMPTY()
db.cambio_climatico.fecha.requires          = IS_DATETIME(format=T('%Y-%m-%d'), error_message='must be YYYY-MM-DD!')

####################################################################
#                           CONCEPTOS                              #
####################################################################
db.define_table('concepto',
    Field('nombre',        'string',     label=T('Nombre')),
    Field('titulo',        'string',     label=T('Titulo')),
    Field('descripcion',   'text',       label=T('Descripcion')),
    format = '%(nombre)s'
)

db.concepto.nombre.requires = IS_NOT_EMPTY()
db.concepto.titulo.requires = IS_NOT_EMPTY()
db.concepto.descripcion.requires = IS_NOT_EMPTY()


####################################################################
#                 TIPO DE CONTAMINACION IMAGENES                   #
####################################################################
db.define_table('tipo_contaminacion_imagen',
    Field('nombre',        'string',     label=T('Nombre')),
    Field('identificador', 'string',     label=T('Identificador')),
    Field('descripcion',   'string',     label=T('Descripcion')),
    format = '%(nombre)s'
)

db.tipo_contaminacion_imagen.nombre.requires = IS_NOT_EMPTY()
db.tipo_contaminacion_imagen.identificador.requires = IS_NOT_EMPTY()

####################################################################
#                      CONTAMINACION IMAGENES                      #
####################################################################

db.define_table('image_contaminacion',
    Field('tipo_cambio_imagen_id',  'reference tipo_contaminacion_imagen',   label=T('Tipo de Contaminacion Imagen')),
    Field('fecha',                      'datetime',                          label=T('Fecha')),
    Field('imagen',   'upload'),
    format = '%(title)s'
)

db.image_contaminacion.tipo_cambio_imagen_id.requires = IS_IN_DB(db, 'tipo_contaminacion_imagen.id', '%(nombre)s', zero=T('Elige uno'))
db.image_contaminacion.fecha.requires                 = IS_DATETIME(format=T('%Y-%m-%d %H:%M:%S'), error_message='Debe de ser ano-mes-dia HH:MM:SS!!')
db.image_contaminacion.imagen.requires                = IS_NOT_EMPTY() and IS_IMAGE(extensions=('png','jpg')) 