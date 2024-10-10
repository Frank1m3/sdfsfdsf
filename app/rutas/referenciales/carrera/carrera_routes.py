from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.carrera.CarreraDao import CarreraDao

carrmod = Blueprint('carrera', __name__, template_folder='templates')

@carrmod.route('/carrera-index')
def carreraIndex():
    carrdao = CarreraDao()
    return render_template('carrera-index.html', lista_alumnos=carrdao.getCarreras())