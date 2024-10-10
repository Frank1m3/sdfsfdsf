from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.alumno.AlumnoDao import AlumnoDao

aluapi = Blueprint('aluapi', __name__)

# Trae todos los alumnos
@aluapi.route('/alumnos', methods=['GET'])
def getAlumnos():
    aludao = AlumnoDao()

    try:
        alumnos = aludao.getAlumnos()

        return jsonify({
            'success': True,
            'data': alumnos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los alumnos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@aluapi.route('/alumnos/<int:alumno_id>', methods=['GET'])
def getAlumno(alumno_id):
    aludao = AlumnoDao()

    try:
        alumno = aludao.getAlumnoById(alumno_id)

        if alumno:
            return jsonify({
                'success': True,
                'data': alumno,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el alumno con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener alumno: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo alumno
@aluapi.route('/alumnos', methods=['POST'])
def addAlumno():
    data = request.get_json()
    aludao = AlumnoDao()

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
        alumno_id = aludao.guardarAlumno(descripcion)
        if alumno_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': alumno_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el alumno. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar el alumno: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@aluapi.route('/alumnos/<int:alumno_id>', methods=['PUT'])
def updateAlumno(alumno_id):
    data = request.get_json()
    aludao = AlumnoDao()

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
        if aludao.updateAlumno(alumno_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': alumno_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el alumno con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar alumno: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@aluapi.route('/alumnos/<int:alumno_id>', methods=['DELETE'])
def deleteAlumno(alumno_id):
    aludao = AlumnoDao()

    try:
        # Usar el retorno de eliminar alumno para determinar el éxito
        if aludao.deleteAlumno(alumno_id):
            return jsonify({
                'success': True,
                'mensaje': f'alumno con ID {alumno_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el alumno con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar alumno: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
    