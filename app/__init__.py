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




# registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
app.register_blueprint(marmod, url_prefix=f'{modulo0}/marca')
app.register_blueprint(nacmod, url_prefix=f'{modulo0}/nacionalidad')
app.register_blueprint(carmod, url_prefix=f'{modulo0}/cargo')
app.register_blueprint(tarmod, url_prefix=f'{modulo0}/tarjeta')
app.register_blueprint(banmod, url_prefix=f'{modulo0}/banco')
app.register_blueprint(supmod, url_prefix=f'{modulo0}/supermercado')





from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.marca.marca_api import marapi
from app.rutas.referenciales.nacionalidad.nacionalidad_api import nacapi
from app.rutas.referenciales.cargo.cargo_api import carapi
from app.rutas.referenciales.tarjeta.tarjeta_api import tarapi
from app.rutas.referenciales.banco.banco_api import banapi
from app.rutas.referenciales.supermercado.supermercado_api import supapi



# APIS v1
version1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=version1)

app.register_blueprint(marapi, url_prefix=version1)

app.register_blueprint(nacapi, url_prefix=version1)

app.register_blueprint(carapi, url_prefix=version1)

app.register_blueprint(tarapi, url_prefix=version1)

app.register_blueprint(banapi, url_prefix=version1)
app.register_blueprint(supapi, url_prefix=version1)
