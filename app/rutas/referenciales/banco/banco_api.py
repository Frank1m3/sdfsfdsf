from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.banco.BancoDao import BancoDao

banapi = Blueprint('banapi', __name__)

# Trae todos los bancos
@banapi.route('/bancos', methods=['GET'])
def getBancos():
    bandao = BancoDao()

    try:
        bancos = bandao.getBancos()

        return jsonify({
            'success': True,
            'data': bancos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas los bancos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@banapi.route('/bancos/<int:banco_id>', methods=['GET'])
def getBanco(banco_id):
    bandao = BancoDao()

    try:
        banco = bandao.getBancoById(banco_id)

        if banco:
            return jsonify({
                'success': True,
                'data': banco,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el banco con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener banco: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo banco
@banapi.route('/bancos', methods=['POST'])
def addBanco():
    data = request.get_json()
    bandao = BancoDao()

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
        banco_id = bandao.guardarBanco(descripcion)
        if banco_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': banco_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el banco. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar el banco: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@banapi.route('/bancos/<int:banco_id>', methods=['PUT'])
def updateBanco(banco_id):
    data = request.get_json()
    bandao = BancoDao()

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
        if bandao.updateBanco(banco_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': banco_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la tarjeta con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar banco: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@banapi.route('/bancos/<int:banco_id>', methods=['DELETE'])
def deleteBanco(banco_id):
    bandao = BancoDao()

    try:
        # Usar el retorno de eliminar banco para determinar el éxito
        if bandao.deleteBanco(banco_id):
            return jsonify({
                'success': True,
                'mensaje': f'Banco con ID {banco_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el banco con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar banco: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
    