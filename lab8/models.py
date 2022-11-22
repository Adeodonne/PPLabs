from uuid import UUID
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, scoped_session
from sqlalchemy_serializer import SerializerMixin
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/deliveryserviceupdated")
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()
Base.metadata.create_all(bind=engine)
session = Session()


class CustomSerializerMixin(SerializerMixin):
	serialize_types = (
		(UUID, lambda x: str(x)),
	)


class Country(Base, CustomSerializerMixin):
	__tablename__ = 'country'

	serialize_only = {'id', 'countryName'}

	id = Column('id', Integer, primary_key = True, autoincrement = True, nullable = False)
	countryName = Column('countryName', String(45), nullable = False)


class State(Base, CustomSerializerMixin):
	__tablename__ = 'state'

	serialize_only = {'id', 'stateName', 'idCountry'}

	id = Column('id', Integer, primary_key = True, autoincrement = True, nullable = False)
	stateName = Column('stateName', String(45), nullable = False)
	idCountry = Column('idCountry', Integer, ForeignKey(Country.id), nullable = False)
	country = relationship(Country, backref='state', lazy='joined')


class City(Base, CustomSerializerMixin):
	__tablename__ = 'city'

	serialize_only = {'id', 'cityName', 'idState'}

	id = Column('id', Integer, primary_key = True, autoincrement = True, nullable = False)
	cityName = Column('cityName', String(45), nullable = False)
	idState = Column('idState', Integer, ForeignKey(State.id), nullable = False)
	state = relationship(State, backref='city', lazy='joined')


class User(Base, CustomSerializerMixin):
	__tablename__ = 'user'

	serialize_only = {'id', 'fullName', 'address', 'idCity', "phoneNumber", "password", "role"}

	id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
	fullName = Column('fullName', String(60), nullable=False)
	address = Column('address', String(45), nullable=False)
	idCity = Column('idCity', Integer, ForeignKey(City.id), nullable=False)
	city = relationship(City, backref='user', lazy='joined')
	phoneNumber = Column('phoneNumber', String(13), nullable=False)
	password = Column('password', String(60), nullable=False)
	role = Column('role', Integer, nullable=False)


class UserSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = User
		include_relationships = True
		load_instance = True
		include_fk = True


class PostOffice(Base, CustomSerializerMixin):
	__tablename__ = 'postoffice'

	serialize_only = {'id', 'name', 'idCity', 'address'}

	id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
	name = Column('name', String(45), nullable=False)
	idCity = Column('idCity', Integer, ForeignKey(City.id), nullable=False)
	city = relationship(City, backref='postoffice', lazy='joined')
	address = Column('address', String(45), nullable=False)


class ProductType(Base, CustomSerializerMixin):
	__tablename__ = 'producttype'

	serialize_only = {'id', 'typeName'}

	id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
	TypeName = Column('typeName', String(45), nullable=False)


class ShipmentType(Base, CustomSerializerMixin):
	__tablename__ = 'shipmenttype'

	serialize_only = {'id', 'name'}

	id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
	name = Column('name', String(45), nullable=False)


class PaymentType(Base, CustomSerializerMixin):
	__tablename__ = 'paymenttype'

	serialize_only = {'id', 'paymentTypeName'}

	id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
	paymentTypeName = Column('paymentTypeName', String(45), nullable=False)


class Seller(Base, CustomSerializerMixin):
	__tablename__ = 'seller'

	serialize_only = {'id', 'weight', 'volume', 'idPostOfficeSender', "sendTime", "description", "approximatelyPrice"}

	id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
	weight = Column('weight', Integer, nullable=False)
	volume = Column('volume', Integer, nullable=False)

	idPostOfficeSender = Column('idPostOfficeSender', Integer, ForeignKey(PostOffice.id), nullable=False)
	postOfficeSender = relationship(PostOffice, backref='Seller', lazy='joined')

	sendTime = Column('sendTime', DATETIME, nullable=False)
	description = Column('description', String(200))
	approximatelyPrice = Column('approximatelyPrice', Integer)


class SellerSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Seller
		include_relationships = True
		load_instance = True
		include_fk = True


class Shipment(Base, CustomSerializerMixin):
	__tablename__ = 'shipment'

	serialize_only = {'id', 'idUser', 'idShipmentType', 'reciveTime', "idPostOffice", "idProductType", "idSeller"}

	id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)

	idUser = Column('idUser', Integer, ForeignKey(User.id), nullable=False)
	user = relationship(User, backref='shipment', lazy='joined')

	idShipmentType = Column('idShipmentType', Integer, ForeignKey(ShipmentType.id), nullable=False)
	shipmentType = relationship(ShipmentType, backref='shipment', lazy='joined')

	reciveTime = Column('reciveTime', DATETIME)

	idPostOffice = Column('idPostOffice', Integer, ForeignKey(PostOffice.id), nullable=False)
	postOffice = relationship(PostOffice, backref='shipment', lazy='joined')

	idProductType = Column('idProductType', Integer, ForeignKey(ProductType.id), nullable=False)
	productType = relationship(ProductType, backref='shipment', lazy='joined')

	idSeller = Column('idSeller', Integer, ForeignKey(Seller.id), nullable=False)
	seller = relationship(Seller, backref='shipment', lazy='joined')


class ShipmentSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Shipment
		include_relationships = True
		load_instance = True
		include_fk = True


class ShipmentStatusName(Base, CustomSerializerMixin):
	__tablename__ = 'shipmentstatusname'

	serialize_only = {'id', 'statusName'}
	id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
	statusName = Column('statusName', String(45), nullable=False)


class ShipmentStatus(Base, CustomSerializerMixin):
	__tablename__ = 'shipmentstatus'

	serialize_only = {'id', 'idShipmentStatusName', 'idShipment', 'statusTime', "details"}
	id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)

	idShipmentStatusName = Column('idShipmentStatusName', Integer, ForeignKey(ShipmentStatusName.id), nullable=False)
	shipmentStatusName = relationship(ShipmentStatusName, backref='shipmentstatus', lazy='joined')

	idShipment = Column('idShipment', Integer, ForeignKey(Shipment.id), nullable=False)
	shipment = relationship(Shipment, backref='shipmentstatus', lazy='joined')

	statusTime = Column('statusTime', DATETIME, nullable=False)

	details = Column('details', String(200))


class PaymentDetails(Base, CustomSerializerMixin):
	__tablename__ = 'paymentdetails'

	serialize_only = {'id', 'price', 'idPaymentType', 'paymentTime', "idShipment"}
	id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
	price = Column('price', Integer, nullable=False)

	idPaymentType = Column('idPaymentType', Integer, ForeignKey(PaymentType.id), nullable=False)
	paymentType = relationship(PaymentType, backref='paymentdetails', lazy='joined')

	paymentTime = Column('paymentTime', DATETIME)

	idShipment = Column('idShipment', Integer, ForeignKey(Shipment.id), nullable=False)
	shipment = relationship(Shipment, backref='paymentdetails', lazy='joined')

Base.metadata.create_all(bind=engine)
