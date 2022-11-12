from flask import Flask, request, render_template
from waitress import serve
from models import *
from marshmallow import validate, ValidationError
from flask_bcrypt import Bcrypt
import json


app = Flask(__name__)
bcrypt = Bcrypt(app)
@app.route('/api/v1/hello-world-2', methods=['GET'])
def helloorld():
    return 'Hello World 2!'

@app.route('/', methods=['GET'])
def helloworld():
    return 'Hello World 2!'

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
def CreateShipment():
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
def DeleteShipment():
    session = Session()
    args = request.args
    id = args.get('id')
    session.query(Shipment).filter(Shipment.id == id).delete()
    session.commit()
    session.close()
    return "Shipment deleted"

@app.route('/seller/', methods=['GET'])
def FindSeller():
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
def CreateSeller():
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
def DeleteSeller():
    session = Session()
    args = request.args
    id = args.get('id')
    session.query(Seller).filter(Seller.id == id).delete()
    session.commit()
    session.close()
    return "Seller deleted"

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
    serve(app)

#cd Lab4
#waitress-serve routes:app
