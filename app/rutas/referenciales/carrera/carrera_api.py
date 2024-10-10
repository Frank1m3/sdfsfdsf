from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.carrera.CarreraDao import CarreraDao

carrapi = Blueprint('carrapi', __name__)

# Trae todas las carreras
@carrapi.route('/carreras', methods=['GET'])
def getCarreras():
    carrdao = CarreraDao()

    try:
        carreras = carrdao.getCarreras()

        return jsonify({
            'success': True,
            'data': carreras,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las carreras: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@carrapi.route('/carreras/<int:carrera_id>', methods=['GET'])
def getCarrera(carrera_id):
    carrdao = CarreraDao()

    try:
        carrera = carrdao.getCarreraById(carrera_id)

        if carrera:
            return jsonify({
                'success': True,
                'data': carrera,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la carrera con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener carrera: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva carrera
@carrapi.route('/carreras', methods=['POST'])
def addCarrera():
    data = request.get_json()
    carrdao = CarreraDao()

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
        carrera_id = carrdao.guardarCarrera(descripcion)
        if carrera_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': carrera_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la carrera. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar la carrera: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@carrapi.route('/carreras/<int:carrera_id>', methods=['PUT'])
def updateCarrera(carrera_id):
    data = request.get_json()
    carrdao = CarreraDao()

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
        if carrdao.updateCarrera(carrera_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': carrera_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la carrera con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar carrera: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@carrapi.route('/carreras/<int:carrera_id>', methods=['DELETE'])
def deleteCarrera(carrera_id):
    carrdao = CarreraDao()

    try:
        # Usar el retorno de eliminar carrera para determinar el éxito
        if carrdao.deleteCarrera(carrera_id):
            return jsonify({
                'success': True,
                'mensaje': f'Carrera con ID {carrera_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la carrera con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar carrera: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
