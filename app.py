import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from catalogo import catalogo
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


# Create flask app
app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = ("HS256")
jwt = JWTManager(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=False)
    password = db.Column(db.String(120), unique=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


#class UsuarioSchema(ma.Schema):
    #class Meta:
        #fields = ('email', 'password')


#usuario_schema = Usuario()
#usuarios_schema = UsuarioSchema(many=True)


class Viaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(144))

    def __init__(self, title, content):
        self.title = title
        self.content = content


class Catalogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id):
        self.id = id
        


class Lugar(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id):
        self.id = id

#lugar_schema = Lugar()
#lugars_schema = LugarSchema(many=True)


db.create_all()


# TOKEN
@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    usuario = Usuario.query.filter_by(email=email, password=password).first()
    # if email != "test" or password != "test":
    if Usuario is None:
        return jsonify({"msg": "No acepta las credenciales"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# Protected


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_usuario_email = get_jwt_identity()
    usuario = Usuario.filter.get(current_usuario_email)

    return jsonify({"email": usuario.email, "password": usuario.password}), 200


# GET Data Routes
@app.route('/catalogo')
def getCatalogo():
    # return jsonify(products)
    return jsonify({'catalogo': catalogo})

# LUGAR

@app.route('/lugar/<id>', methods=["GET"])
def get_lugar(id):
    return jsonify({'id': id})


@app.route('/catalogo/<string:catalogo_nombre>')
def getCatalogos(catalogo_nombre):
    catalogosFound = [
        catalogo for catalogo in catalogo if catalogo['nombre'] == catalogo_nombre]
    if (len(catalogosFound) > 0):
        return jsonify({"catalogo": catalogosFound[0]})
    return jsonify({"message": "Destino no encontrado"})

# Create Data Route


@app.route('/catalogo', methods=['POST'])
def addDestino():
    new_destino = {
        "nombre": request.json['nombre'],
        "publicidad": request.json['publicidad'],
        "precio": request.json['precio'],
        "paquete": request.json['paquete'],
        "promocion": request.json['promocion'],
        "url": request.json['url'],
        "thumb_image_url": request.json['thumb_image_url'],
        "thumb_banner": request.json['thumb_banner'],
        "id": request.json['id'],
        "logo_url": request.json['logo_url'],
       


    }
    catalogo.append(new_destino)
    return jsonify({"message": "Destino agregado", "catalogo": catalogo})

# Update Data Route


@app.route('/catalogo/<string:catalogo_nombre>', methods=['PUT'])
def editDestino(catalogo_nombre):
    catalogosFound = [
        catalogo for catalogo in catalogo if catalogo['nombre'] == catalogo_nombre]
    if (len(catalogosFound) > 0):
        catalogosFound[0]['nombre'] = request.json['nombre']
        catalogosFound[0]['precio'] = request.json['precio']
        catalogosFound[0]['paquete'] = request.json['paquete']
        catalogosFound[0]['promocion'] = request.json['promocion']
       
        return jsonify({"message": "Destino actualizado", "catalogo": catalogosFound[0]})
    return jsonify({"Lo siento NO encontramos el destino"})

# Delete Data Route


@app.route('/catalogo/<string:catalogo_nombre>', methods=['DELETE'])
def deleteDestino(catalogo_nombre):
    catalogosFound = [
        catalogo for catalogo in catalogo if catalogo['nombre'] == catalogo_nombre]
    if len(catalogosFound) > 0:
        catalogo.remove(catalogosFound[0])
        return jsonify({"message": "Destino eliminado", "catalogo": catalogo})
    return jsonify({"message": "Destino NO encontrado"})


if __name__ == '__main__':
    app.run(debug=True)
