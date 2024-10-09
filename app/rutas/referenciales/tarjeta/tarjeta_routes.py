from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.tarjeta.TarjetaDao import TarjetaDao

tarmod = Blueprint('tarjeta', __name__, template_folder='templates')

@tarmod.route('/tarjeta-index')
def tarjetaIndex():
    tardao = TarjetaDao()
    return render_template('tarjeta-index.html', lista_tarjetas=tardao.getTarjetas())