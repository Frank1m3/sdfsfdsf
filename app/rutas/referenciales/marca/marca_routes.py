from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.marca.MarcaDao import MarcaDao

marmod = Blueprint('marca', __name__, template_folder='templates')

@marmod.route('/marca-index')
def marcaIndex():
    mardao = MarcaDao()
    return render_template('marca-index.html', lista_marcas=mardao.getMarcas())