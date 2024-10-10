from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.entidad.EntidadDao import EntidadDao

entapi = Blueprint('entapi', __name__)

# Trae todas las entidades
@entapi.route('/entidades', methods=['GET'])
def getEntidades():
    entdao = EntidadDao()

    try:
        entidades = entdao.getEntidades()

        return jsonify({
            'success': True,
            'data': entidades,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las entidades: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@entapi.route('/entidades/<int:entidad_id>', methods=['GET'])
def getEntidad(entidad_id):
    entdao = EntidadDao()

    try:
        entidad = entdao.getEntidadById(entidad_id)

        if entidad:
            return jsonify({
                'success': True,
                'data': entidad,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la entidad con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener entidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva entidad
@entapi.route('/entidades', methods=['POST'])
def addEntidad():
    data = request.get_json()
    entdao = EntidadDao()

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
        entidad_id = entdao.guardarEntidad(descripcion)
        if entidad_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': entidad_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la entidad. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar la entidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@entapi.route('/entidades/<int:entidad_id>', methods=['PUT'])
def updateEntidad(entidad_id):
    data = request.get_json()
    entdao = EntidadDao()

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
        if entdao.updateEntidad(entidad_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': entidad_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la entidad con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar entidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@entapi.route('/entidades/<int:entidad_id>', methods=['DELETE'])
def deleteEntidad(entidad_id):
    entdao = EntidadDao()

    try:
        # Usar el retorno de eliminar entidad para determinar el éxito
        if entdao.deleteEntidad(entidad_id):
            return jsonify({
                'success': True,
                'mensaje': f'Entidad con ID {entidad_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la entidad con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar entidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
