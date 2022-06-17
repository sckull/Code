def index():
    return dict()

def doc():
    contenido = db(db.contenido.tipo_contenido_id == 4).select(db.contenido.titulo, db.contenido.contenido)
    return dict(contenido = contenido)
