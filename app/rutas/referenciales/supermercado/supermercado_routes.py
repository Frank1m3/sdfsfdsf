from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.supermercado.SupermercadoDao import SupermercadoDao

supmod = Blueprint('supermercado', __name__, template_folder='templates')

@supmod.route('/supermercado-index')
def supermercadoIndex():
    supdao = SupermercadoDao()
    return render_template('supermercado-index.html', lista_supermercados=supdao.getSupermercados())