from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.proveedor.ProveedorDao import ProveedorDao

proapi = Blueprint('proapi', __name__)


@proapi.route('/proveedores', methods=['GET'])
def getProveedores():
    prodao = ProveedorDao()

    try:
        proveedores = prodao.getProveedores()

        return jsonify({
            'success': True,
            'data': proveedores,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los proveedores: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proapi.route('/proveedores/<int:proveedor_id>', methods=['GET'])
def getProveedor(proveedor_id):
    prodao = ProveedorDao()

    try:
        proveedor = prodao.getProveedorById(proveedor_id)

        if proveedor:
            return jsonify({
                'success': True,
                'data': proveedor,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el proveedor con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


@proapi.route('/proveedores', methods=['POST'])
def addProveedor():
    data = request.get_json()
    prodao = ProveedorDao()

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
        proveedor_id = prodao.guardarProveedor(descripcion)
        if proveedor_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': proveedor_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el proveedor. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar el proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proapi.route('/proveedores/<int:proveedor_id>', methods=['PUT'])
def updateProveedor(proveedor_id):
    data = request.get_json()
    prodao = ProveedorDao()

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
        if prodao.updateProveedor(proveedor_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': proveedor_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el proveedor con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proapi.route('/proveedores/<int:proveedor_id>', methods=['DELETE'])
def deleteProveedor(proveedor_id):
    prodao = ProveedorDao()

    try:
        # Usar el retorno de eliminarNacionalidad para determinar el éxito
        if prodao.deleteProveedor(proveedor_id):
            return jsonify({
                'success': True,
                'mensaje': f'Proveedor con ID {proveedor_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la proveedor con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500