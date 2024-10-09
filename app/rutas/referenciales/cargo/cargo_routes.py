from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.cargo.CargoDao import CargoDao

carmod = Blueprint('cargo', __name__, template_folder='templates')

@carmod.route('/cargo-index')
def cargoIndex():
    cardao = CargoDao()
    return render_template('cargo-index.html', lista_cargos=cardao.getCargos())