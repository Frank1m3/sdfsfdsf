from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.banco.BancoDao import BancoDao

banmod = Blueprint('banco', __name__, template_folder='templates')

@banmod.route('/banco-index')
def bancoIndex():
    bandao = BancoDao()
    return render_template('banco-index.html', lista_bancos=bandao.getBancos())