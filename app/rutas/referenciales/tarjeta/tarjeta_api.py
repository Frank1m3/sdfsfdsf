from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.tarjeta.TarjetaDao import TarjetaDao

tarapi = Blueprint('tarapi', __name__)

# Trae todos las tarjetas
@tarapi.route('/tarjetas', methods=['GET'])
def getTarjetas():
    tardao = TarjetaDao()

    try:
        tarjetas = tardao.getTarjetas()

        return jsonify({
            'success': True,
            'data': tarjetas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las tarjetas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@tarapi.route('/tarjetas/<int:tarjeta_id>', methods=['GET'])
def getTarjeta(tarjeta_id):
    tardao = TarjetaDao()

    try:
        tarjeta = tardao.getTarjetaById(tarjeta_id)

        if tarjeta:
            return jsonify({
                'success': True,
                'data': tarjeta,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la tarjeta con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener tarjeta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva tarjeta
@tarapi.route('/tarjetas', methods=['POST'])
def addTarjeta():
    data = request.get_json()
    tardao = TarjetaDao()

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
        tarjeta_id = tardao.guardarTarjeta(descripcion)
        if tarjeta_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': tarjeta_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la tarjeta. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar la tarjeta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@tarapi.route('/tarjetas/<int:tarjeta_id>', methods=['PUT'])
def updateTarjeta(tarjeta_id):
    data = request.get_json()
    tardao = TarjetaDao()

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
        if tardao.updateTarjeta(tarjeta_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': tarjeta_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la tarjeta con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar tarjeta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@tarapi.route('/tarjetas/<int:tarjeta_id>', methods=['DELETE'])
def deleteTarjeta(tarjeta_id):
    tardao = TarjetaDao()

    try:
        # Usar el retorno de eliminar tarjeta para determinar el éxito
        if tardao.deleteTarjeta(tarjeta_id):
            return jsonify({
                'success': True,
                'mensaje': f'Tarjeta con ID {tarjeta_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la tarjeta con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar tarjeta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
    