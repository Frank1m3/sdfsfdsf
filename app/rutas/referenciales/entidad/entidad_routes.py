from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.entidad.EntidadDao import EntidadDao

entmod = Blueprint('entidad', __name__, template_folder='templates')

@entmod.route('/entidad-index')
def entidadIndex():
    entdao = EntidadDao()
    return render_template('entidad-index.html', lista_alumnos=entdao.getEntidades())