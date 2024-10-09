from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.nacionalidad.NacionalidadDao import NacionalidadDao

nacmod = Blueprint('nacionalidad', __name__, template_folder='templates')

@nacmod.route('/nacionalidad-index')
def nacionalidadIndex():
    nacdao = NacionalidadDao()
    return render_template('nacionalidad-index.html', lista_nacionalidades=nacdao.getNacionalidad())