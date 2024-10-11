from flask import Flask

app = Flask(__name__)

#Cada importar, registrar el from app. Apis v1 son los caminos para que funcione todo el entorno
# importar referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.marca.marca_routes import marmod
from app.rutas.referenciales.nacionalidad.nacionalidad_routes import nacmod
from app.rutas.referenciales.cargo.cargo_routes import carmod
from app.rutas.referenciales.tarjeta.tarjeta_routes import tarmod
from app.rutas.referenciales.banco.banco_routes import banmod
from app.rutas.referenciales.supermercado.supermercado_routes import supmod
from app.rutas.referenciales.hospital.hospital_routes import hosmod
from app.rutas.referenciales.alumno.alumno_routes import alumod
from app.rutas.referenciales.docente.docente_routes import docmod
from app.rutas.referenciales.carrera.carrera_routes import carrmod
from app.rutas.referenciales.entidad.entidad_routes import entmod
from app.rutas.referenciales.materia.materia_routes import matmod
from app.rutas.referenciales.vehiculo.vehiculo_routes import vehimod
from app.rutas.referenciales.proveedor.proveedor_routes import promod




# registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
app.register_blueprint(marmod, url_prefix=f'{modulo0}/marca')
app.register_blueprint(nacmod, url_prefix=f'{modulo0}/nacionalidad')
app.register_blueprint(carmod, url_prefix=f'{modulo0}/cargo')
app.register_blueprint(tarmod, url_prefix=f'{modulo0}/tarjeta')
app.register_blueprint(banmod, url_prefix=f'{modulo0}/banco')
app.register_blueprint(supmod, url_prefix=f'{modulo0}/supermercado')
app.register_blueprint(hosmod, url_prefix=f'{modulo0}/hospital')
app.register_blueprint(alumod, url_prefix=f'{modulo0}/alumno')
app.register_blueprint(docmod, url_prefix=f'{modulo0}/docente')
app.register_blueprint(carrmod, url_prefix=f'{modulo0}/carrera')
app.register_blueprint(entmod, url_prefix=f'{modulo0}/entidad')
app.register_blueprint(matmod, url_prefix=f'{modulo0}/materia')
app.register_blueprint(vehimod, url_prefix=f'{modulo0}/vehiculo')
app.register_blueprint(promod, url_prefix=f'{modulo0}/proveedor')






from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.marca.marca_api import marapi
from app.rutas.referenciales.nacionalidad.nacionalidad_api import nacapi
from app.rutas.referenciales.cargo.cargo_api import carapi
from app.rutas.referenciales.tarjeta.tarjeta_api import tarapi
from app.rutas.referenciales.banco.banco_api import banapi
from app.rutas.referenciales.supermercado.supermercado_api import supapi
from app.rutas.referenciales.hospital.hospital_api import hosapi
from app.rutas.referenciales.alumno.alumno_api import aluapi
from app.rutas.referenciales.docente.docente_api import docapi
from app.rutas.referenciales.carrera.carrera_api import carrapi
from app.rutas.referenciales.entidad.entidad_api import entapi
from app.rutas.referenciales.materia.materia_api import matapi
from app.rutas.referenciales.vehiculo.vehiculo_api import vehiapi
from app.rutas.referenciales.proveedor.proveedor_api import proapi



# APIS v1
version1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=version1)

app.register_blueprint(marapi, url_prefix=version1)

app.register_blueprint(nacapi, url_prefix=version1)

app.register_blueprint(carapi, url_prefix=version1)

app.register_blueprint(tarapi, url_prefix=version1)

app.register_blueprint(banapi, url_prefix=version1)

app.register_blueprint(supapi, url_prefix=version1)

app.register_blueprint(hosapi, url_prefix=version1)

app.register_blueprint(aluapi, url_prefix=version1)

app.register_blueprint(docapi, url_prefix=version1)

app.register_blueprint(carrapi, url_prefix=version1)

app.register_blueprint(entapi, url_prefix=version1)

app.register_blueprint(matapi, url_prefix=version1)

app.register_blueprint(vehiapi, url_prefix=version1)

app.register_blueprint(proapi, url_prefix=version1)