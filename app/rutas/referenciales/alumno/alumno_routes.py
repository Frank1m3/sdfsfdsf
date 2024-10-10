from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.alumno.AlumnoDao import AlumnoDao

alumod = Blueprint('alumno', __name__, template_folder='templates')

@alumod.route('/alumno-index')
def alumnoIndex():
    aludao = AlumnoDao()
    return render_template('alumno-index.html', lista_alumnos=aludao.getAlumnos())