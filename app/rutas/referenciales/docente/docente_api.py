from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.docente.DocenteDao import DocenteDao

docapi = Blueprint('docapi', __name__)


@docapi.route('/docentes', methods=['GET'])
def getDocentes():
    docdao = DocenteDao()

    try:
        docentes = docdao.getDocentes()

        return jsonify({
            'success': True,
            'data': docentes,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los docentes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@docapi.route('/docentes/<int:docente_id>', methods=['GET'])
def getDocente(docente_id):
    docdao = DocenteDao()

    try:
        docente = docdao.getAlumnoById(docente_id)

        if docente:
            return jsonify({
                'success': True,
                'data': docente,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el docente con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener docente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo docente
@docapi.route('/docentes', methods=['POST'])
def addDocente():
    data = request.get_json()
    docdao = DocenteDao()

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
        docente_id = docdao.guardarDocente(descripcion)
        if docente_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': docente_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el docente. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar el docente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@docapi.route('/docentes/<int:docente_id>', methods=['PUT'])
def updateDocente(docente_id):
    data = request.get_json()
    docdao = DocenteDao()

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
        if docdao.updateDocente(docente_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': docente_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el docente con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar docente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@docapi.route('/docentes/<int:docente_id>', methods=['DELETE'])
def deleteDocente(docente_id):
    docdao = DocenteDao()

    try:
        # Usar el retorno de eliminar docente para determinar el éxito
        if docdao.deleteDocente(docente_id):
            return jsonify({
                'success': True,
                'mensaje': f'docente con ID {docente_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el docente con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar docente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
    