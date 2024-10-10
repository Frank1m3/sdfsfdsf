from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.materia.MateriaDao import MateriaDao

matapi = Blueprint('matapi', __name__)

# Trae todas las materias
@matapi.route('/materias', methods=['GET'])
def getMaterias():
    matdao = MateriaDao()

    try:
        materias = matdao.getMaterias()

        return jsonify({
            'success': True,
            'data': materias,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las materias: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@matapi.route('/materias/<int:materia_id>', methods=['GET'])
def getMateria(materia_id):
    matdao = MateriaDao()

    try:
        materia = matdao.getMateriaById(materia_id)

        if materia:
            return jsonify({
                'success': True,
                'data': materia,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la materia con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener materia: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva materia
@matapi.route('/materias', methods=['POST'])
def addMateria():
    data = request.get_json()
    matdao = MateriaDao()

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
        materia_id = matdao.guardarMateria(descripcion)
        if materia_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': materia_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la materia. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar la materia: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@matapi.route('/materias/<int:materia_id>', methods=['PUT'])
def updateMateria(materia_id):
    data = request.get_json()
    matdao = MateriaDao()

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
        if matdao.updateMateria(materia_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': materia_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la materia con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar materia: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@matapi.route('/materias/<int:materia_id>', methods=['DELETE'])
def deleteMateria(materia_id):
    matdao = MateriaDao()

    try:
        # Usar el retorno de eliminar materia para determinar el éxito
        if matdao.deleteMateria(materia_id):
            return jsonify({
                'success': True,
                'mensaje': f'Materia con ID {materia_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la materia con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar materia: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
