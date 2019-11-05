from playhouse.postgres_ext import PostgresqlExtDatabase
import models

db = PostgresqlExtDatabase(
    "mega_chat", 
    user = "chat_admin",
    host="localhost",
    port=5432,
    password="47461031"
    )


db.connect()
db.create_tables(
    [models.User, models.Message, models.Chat, models.Salt]
)