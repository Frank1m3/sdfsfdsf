from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.vehiculo.VehiculoDao import VehiculoDao

vehiapi = Blueprint('vehiapi', __name__)

# Trae todos los vehículos
@vehiapi.route('/vehiculos', methods=['GET'])
def getVehiculos():
    vehiDao = VehiculoDao()
    try:
        vehiculos = vehiDao.getVehiculos()
        return jsonify({
            'success': True,
            'data': vehiculos,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los vehículos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@vehiapi.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def getVehiculo(vehiculo_id):
    vehiDao = VehiculoDao()
    try:
        vehiculo = vehiDao.getVehiculoById(vehiculo_id)
        if vehiculo:
            return jsonify({
                'success': True,
                'data': vehiculo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el vehículo con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener vehículo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo vehículo
@vehiapi.route('/vehiculos', methods=['POST'])
def addVehiculo():
    data = request.get_json()
    vehiDao = VehiculoDao()
    
    campos_requeridos = ['descripcion']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        descripcion = data['descripcion'].upper()
        vehiculo_id = vehiDao.guardarVehiculo(descripcion)
        if vehiculo_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': vehiculo_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el vehículo. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar el vehículo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@vehiapi.route('/vehiculos/<int:vehiculo_id>', methods=['PUT'])
def updateVehiculo(vehiculo_id):
    data = request.get_json()
    vehiDao = VehiculoDao()

    campos_requeridos = ['descripcion']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    descripcion = data['descripcion']
    
    try:
        if vehiDao.updateVehiculo(vehiculo_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': vehiculo_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el vehículo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar vehículo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@vehiapi.route('/vehiculos/<int:vehiculo_id>', methods=['DELETE'])
def deleteVehiculo(vehiculo_id):
    vehiDao = VehiculoDao()
    try:
        if vehiDao.deleteVehiculo(vehiculo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Vehículo con ID {vehiculo_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el vehículo con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar vehículo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
