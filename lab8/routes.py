from flask import Flask, request, render_template, jsonify
# from waitress import serve
from models import *
from marshmallow import validate, ValidationError
from flask_jwt_extended import *
import bcrypt
import json


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret"
# app.config["ADMIN_SECRET_KEY"] = "extra-secret"
jwt = JWTManager(app)
# bcrypt = Bcrypt(app)


@app.route('/user/', methods=['GET']) # http://0.0.0.0:8080/user/?id=0
def FindUser():
    args = request.args
    id = args.get('id')
    users = Session.query(User).filter(User.id == id)
    return json.dumps([i.to_dict() for i in users])


"""
Example for post
{
    "id": 1,
    "fullName": "User1 Name",
    "address": "User1 Address",
    "idCity": 0,
    "phoneNumber": "+380111111111",
    "password": "User1Password",
    "role": 0
}
"""


@app.route('/user', methods=['POST'])
def NewUser():
    args = request.get_json()
    try:
        user_schema = UserSchema()
        hashed = bcrypt.hashpw(args["password"].encode("utf-8"), bcrypt.gensalt())
        args["password"] = hashed
        user = user_schema.load(args, session=session)
        session.add(user)
        session.commit()
        access_token = create_access_token(identity = args["id"])
        return {"access_token": access_token}, 200
    except ValidationError as err:
        return json.dumps({'success':False, 'status':400, "error":str(err)}), 400, {'ContentType':'application/json'}


@app.route('/user/<int:id>', methods=['DELETE']) # http://0.0.0.0:8080/user/?id=1
@jwt_required()
def DeleteUser(id):
    if not protect()["access"]:
        return {"Error": "Not enough rights"}, 200

    session = Session()
    session.query(User).filter(User.id == id).delete()
    session.commit()
    session.close()
    return {"Result": "Successful"}, 200


@app.route('/shipment/', methods=['GET'])
def FindShipment():
    args = request.args
    id = args.get('id')
    shipments = Session.query(Shipment).filter(Shipment.id == id)
    return json.dumps([i.to_dict() for i in shipments])


"""
Example for post
{
    "id": 0,
    "weight" : 100,
    "volume": 100,
    "idPostOfficeSender": 0,
    "sendTime": "2011-04-15 00:03:20",
    "description": "Description0",
    "approximatelyPrice" : 0
}
"""


@app.route('/shipment', methods=['POST'])
@jwt_required()
def CreateShipment():
    user_id = get_jwt_identity()

    args = request.get_json()
    try:
        shipmentSchema = ShipmentSchema()
        shipment = shipmentSchema.load(args, session=session)
        session.add(shipment)
        session.commit()
        return shipmentSchema.dump(shipment)
    except ValidationError as err:
        return json.dumps({'success':False, 'status':400, "error":str(err)}), 400, {'ContentType':'application/json'}


@app.route('/shipment/', methods=['DELETE'])
@jwt_required()
def DeleteShipment():
    user_id = get_jwt_identity()

    session = Session()
    args = request.args
    id = args.get('id')
    session.query(Shipment).filter(Shipment.id == id).delete()
    session.commit()
    session.close()
    return "Shipment deleted"


@app.route('/seller/', methods=['GET'])
@jwt_required()
def FindSeller():
    user_id = get_jwt_identity()

    args = request.args
    id = args.get('id')
    sellers = Session.query(Seller).filter(Seller.id == id)
    return json.dumps([i.to_dict() for i in sellers])


"""
Example for post
{
    "id": 0,
    "idUser" : 0,
    "idShipmentType": 0,
    "reciveTime": "2011-04-15 00:03:20",
    "idPostOffice" : 0,
    "idProductType": 0,
    "idSeller" : 0
}
"""


@app.route('/seller', methods=['POST'])
@jwt_required()
def CreateSeller():
    user_id = get_jwt_identity()

    args = request.get_json()
    try:
        sellerSchema = SellerSchema()
        shipment = sellerSchema.load(args, session=session)
        session.add(shipment)
        session.commit()
        return sellerSchema.dump(shipment)
    except ValidationError as err:
        return json.dumps({'success':False, 'status':400, "error":str(err)}), 400, {'ContentType':'application/json'}


@app.route('/seller/', methods=['DELETE'])
@jwt_required()
def DeleteSeller():
    user_id = get_jwt_identity()

    session = Session()
    args = request.args
    id = args.get('id')
    session.query(Seller).filter(Seller.id == id).delete()
    session.commit()
    session.close()
    return "Seller deleted"


@app.route('/user/login', methods = ['GET'])
def login():
    args = request.get_json()
    phone = args["phoneNumber"]
    password = args["password"]

    user = session.query(User).filter(User.phoneNumber == phone)

    cPassword = ""
    id = 0
    for row in user:
        id = row.to_dict()["id"]
        cPassword = row.to_dict()["password"]

    if cPassword == "" or not bcrypt.checkpw(password.encode("utf-8"), cPassword.encode("utf-8")):
        return {"Error": "invalid input"}, 405

    access_token = create_access_token(identity = id)
    return {"access_token": access_token}, 200 #jsonify(access_toke = access_token)


def protect():
    id = get_jwt_identity()

    result = session.query(User).filter(User.id == id)

    role = False

    for row in result:
        role = bool(row.to_dict()["role"])

    return {"access": True} if role else {"access": False}


if __name__ == '__main__':
    app.run(debug=True, port = 5000, host = "127.0.0.1")
