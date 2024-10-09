from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.supermercado.SupermercadoDao import SupermercadoDao

supapi = Blueprint('supapi', __name__)


@supapi.route('/supermercados', methods=['GET'])
def getSupermercados():
    supdao = SupermercadoDao()

    try:
        supermercados = supdao.getSupermercados()

        return jsonify({
            'success': True,
            'data': supermercados,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas los supermercados: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@supapi.route('/supermercados/<int:supermercado_id>', methods=['GET'])
def getSupermercado(supermercado_id):
    supdao = SupermercadoDao()

    try:
        supermercado = supdao.getSupermercadoById(supermercado_id)

        if supermercado:
            return jsonify({
                'success': True,
                'data': supermercado,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el supermercado con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener supermercado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo supermercado
@supapi.route('/supermercados', methods=['POST'])
def addSupermercado():
    data = request.get_json()
    supdao = SupermercadoDao()

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
        supermercado_id = supdao.guardarSupermercado(descripcion)
        if supermercado_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': supermercado_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el supermercado. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar el banco: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@supapi.route('/supermercados/<int:supermercado_id>', methods=['PUT'])
def updateSupermercado(supermercado_id):
    data = request.get_json()
    supdao = SupermercadoDao()

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
        if supdao.updateSupermercado(supermercado_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': supermercado_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el supermercado con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar supermercado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@supapi.route('/supermercados/<int:supermercado_id>', methods=['DELETE'])
def deleteSupermercado(supermercado_id):
    supdao = SupermercadoDao()

    try:
        # Usar el retorno de eliminar banco para determinar el éxito
        if supdao.deleteSupermercado(supermercado_id):
            return jsonify({
                'success': True,
                'mensaje': f'supermercado con ID {supermercado_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el supermercado con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar supermercado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
    