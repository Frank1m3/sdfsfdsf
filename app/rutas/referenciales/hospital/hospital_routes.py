from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.hospital.HospitalDao import HospitalDao

hosmod = Blueprint('hospital', __name__, template_folder='templates')

@hosmod.route('/hospital-index')
def hospitalIndex():
    hosdao = HospitalDao()
    return render_template('hospital-index.html', lista_hospitales=hosdao.getHospitales())