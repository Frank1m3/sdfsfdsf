from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.proveedor.ProveedorDao import ProveedorDao

promod = Blueprint('proveedor', __name__, template_folder='templates')

@promod.route('/proveedor-index')
def proveedorIndex():
    prodao = ProveedorDao()
    return render_template('proveedor-index.html', lista_proveedores=prodao.getProveedores())