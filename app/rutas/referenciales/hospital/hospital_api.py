from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.hospital.HospitalDao import HospitalDao

hosapi = Blueprint('hosapi', __name__)

# Trae todos los bancos
@hosapi.route('/hospitales', methods=['GET'])
def getHospitales():
    hosdao = HospitalDao()

    try:
        hospitales = hosdao.getHospitales()

        return jsonify({
            'success': True,
            'data': hospitales,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas los hospitales: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@hosapi.route('/hospitales/<int:hospital_id>', methods=['GET'])
def getHospital(hospital_id):
    hosdao = HospitalDao()

    try:
        hospital = hosdao.getHospitalById(hospital_id)

        if hospital:
            return jsonify({
                'success': True,
                'data': hospital,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el hospital con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener hospital: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


@hosapi.route('/hospitales', methods=['POST'])
def addHospital():
    data = request.get_json()
    hosdao = HospitalDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        hospital_id = hosdao.guardarHospital(descripcion)
        if hospital_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': hospital_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el hospital. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar el hospital: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@hosapi.route('/hospitales/<int:hospital_id>', methods=['PUT'])
def updateHospital(hospital_id):
    data = request.get_json()
    hosdao = HospitalDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if hosdao.updateHospital(hospital_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': hospital_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el hospital con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar hospital: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@hosapi.route('/hospitales/<int:hospital_id>', methods=['DELETE'])
def deleteHospital(hospital_id):
    hosdao = HospitalDao()

    try:
     
        if hosdao.deleteHospital(hospital_id):
            return jsonify({
                'success': True,
                'mensaje': f'hospital con ID {hospital_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el hospital con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar hospital: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
    banco