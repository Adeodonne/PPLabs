from flask import Flask, request, render_template
from waitress import serve
from models import *
from marshmallow import validate, ValidationError
from flask_bcrypt import Bcrypt
import json


app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET'])
def helloworld():
    return 'Backend is working'

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
        user = user_schema.load(args, session=session)
        #user.Password = bcrypt.generate_password_hash(user.password)
        session.add(user)
        session.commit()
        return user_schema.dump(user)
    except ValidationError as err:
        return json.dumps({'success':False, 'status':400, "error":str(err)}), 400, {'ContentType':'application/json'}

@app.route('/user/', methods=['PUT'])
def UpdateUser():
    session = Session()
    args = request.get_json()
    arg = request.args
    id = arg.get('id')
    userSchema = UserSchema()
    try:
        user = userSchema.load(args, session=session)
        if 'password' in args.keys():
            args['password'] = bcrypt.generate_password_hash(user.password)
        session.query(User).filter(User.id == id).update(args)
        user = userSchema.dump(session.query(User).filter(User.id == id).first())
        session.commit()
        session.close()
        return user, 200
    except ValidationError as err:
        session.close()
        return str(err), 400
@app.route('/user/', methods=['DELETE']) # http://0.0.0.0:8080/user/?id=1
def DeleteUser():
    session = Session()
    args = request.args
    id = args.get('id')
    session.query(User).filter(User.id == id).delete()
    session.commit()
    session.close()
    return "User deleted"

@app.route('/shipment/', methods=['GET'])
def FindShipment():
    session = Session()
    args = request.args
    id = args.get('id')

    shipments = session.query(Shipment).filter(Shipment.id == id).first()
    shipmentSchema = ShipmentSchema()

    seller = session.query(Seller).filter(Seller.id == id).first()
    sellerSchema = SellerSchema()

    res = {"shipment" : {**shipmentSchema.dump(shipments)}, "seller" : {**sellerSchema.dump(seller)}}

    session.close()
    return json.dumps(res), 200

"""
Example for post

{
"shipment":
    {
        "id": 1,
        "idUser": 0,
        "idShipmentType": 0,
        "reciveTime": "2011-04-15T00:03:20",
        "idPostOffice": 0,
        "idProductType": 0,
        "idSeller": 1
    },
"seller":
    {
    "id": 1,
    "weight": 1,
    "volume": 1,
    "idPostOfficeSender": 0,
    "sendTime":"2011-04-15T00:03:20",
    "description": "Description1",
    "approximatelyPrice": 1
    }
}
"""

@app.route('/shipment', methods=['POST'])
def CreateShipment():
    session = Session()
    args = request.get_json()
    try:
        sellerSchema = SellerSchema()
        seller = sellerSchema.load(args.get("seller"), session=session)
        session.add(seller)

        shipmentSchema = ShipmentSchema()
        shipment = shipmentSchema.load(args.get("shipment"), session=session)
        session.add(shipment)

        session.commit()
        session.expunge_all()
        session.close()
        return "Created seller and shipment" #json.dumps({"shipment" : {**shipmentSchema.dump(shipment)}, "seller" : {**sellerSchema.dump(seller)}})
    except ValidationError as err:
        return json.dumps({'success':False, 'status':400, "error":str(err)}), 400, {'ContentType':'application/json'}

@app.route('/shipment/', methods=['PUT'])
def UpdateShipment():
    session = Session()
    args = request.get_json()
    arg = request.args
    id = arg.get('id')
    shipmentSchema = ShipmentSchema()
    sellerSchema = SellerSchema()
    try:
        shipmentSchema.load(args.get("shipment"), session=session)
        session.query(Shipment).filter(Shipment.id == id).update(args.get("shipment"))
        shipment = shipmentSchema.dump(session.query(Shipment).filter(Shipment.id == id).first())

        sellerSchema.load(args.get("seller"), session=session)
        session.query(Seller).filter(Seller.id == id).update(args.get("seller"))
        seller = sellerSchema.dump(session.query(Seller).filter(Seller.id == id).first())

        session.commit()
        session.close()
        return "Seller and shipment updated" #json.dumps({"shipment" : {**shipmentSchema.dump(shipment)}, "seller" : {**sellerSchema.dump(seller)}}), 200
    except ValidationError as err:
        session.close()
        return str(err), 400
@app.route('/shipment/', methods=['DELETE'])
def DeleteShipment():
    session = Session()
    args = request.args
    id = args.get('id')
    session.query(Shipment).filter(Shipment.id == id).delete()
    session.query(Seller).filter(Seller.id == id).delete()
    session.commit()
    session.close()
    return "Shipment and seller deleted"


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
    serve(app)

#cd Lab4
#waitress-serve routes:app
