from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.materia.MateriaDao import MateriaDao

matmod = Blueprint('materia', __name__, template_folder='templates')

@matmod.route('/materia-index')
def materiaIndex():
    matdao = MateriaDao()
    return render_template('materia-index.html', lista_alumnos=matdao.getMaterias())