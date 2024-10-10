from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.docente.DocenteDao import DocenteDao

docmod = Blueprint('docente', __name__, template_folder='templates')

@docmod.route('/docente-index')
def docenteIndex():
    docdao = DocenteDao()
    return render_template('docente-index.html', lista_docentes=docdao.getDocentes())