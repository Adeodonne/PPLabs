from sqlalchemy import *

#DB info
meta = MetaData()

#Creating tables
'''
user = Table("user", meta,
            Column("iduser", Integer, primary_key = True),
            Column("username", String(45), nullable = False),
            Column("full_name", String(45), nullable = False),
            Column("phone_number", String(45), nullable = False),
            Column("email", String(45), nullable = False)
)

order = Table("order", meta,
            Column("idorder", Integer, primary_key = True),
            Column("delivery_adress", String(45), nullable = False),
            Column("status", Enum("confirmation", "shipping", "completed"), nullable = False),
            Column("user_id", Integer, ForeignKey("user.iduser"))
)

order_and_trainer = Table("order_and_trainer", meta,
            Column("order_id", Integer, ForeignKey("order.idorder")),
            Column("trainer_id", Integer, ForeignKey("trainer.idtrainer")),
            Column("count", Integer, primary_key = True),
)

trainer = Table("trainer", meta,
            Column("idtrainer", Integer, primary_key = True),
            Column("name", String(45), nullable = False),
            Column("size", Float, nullable = False),
            Column("price", Float, nullable = False)
)
'''

engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/shop")
meta.create_all(engine)

connection = engine.connect()

#Request for databases
# insert_trainer = trainer.insert().values(idtrainer = 1, name = "Yeezy Boost 350", size = 44, price = 400)
# delete_trainer = trainer.delete().where(trainer.c.idtrainer == 2)
# update_trainer = trainer.update().where(trainer.c.idtrainer == 1).values(price = 500)
# select_trainer = trainer.select()

#connection.execute(delete_trainer)
#connection.execute(update_trainer)
#connection.execute(insert_trainer)
#result = connection.execute(select_trainer)

#for row in result:
#    print(row)
