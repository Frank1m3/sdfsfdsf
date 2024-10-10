from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.vehiculo.VehiculoDao import VehiculoDao

vehimod = Blueprint('vehiculo', __name__, template_folder='templates')

@vehimod.route('/vehiculo-index')
def vehiculoIndex():
    vehidao = VehiculoDao()
    return render_template('vehiculo-index.html', lista_vehiculos=vehidao.getVehiculos())