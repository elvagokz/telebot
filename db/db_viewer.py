from peewee import Model, SqliteDatabase, CharField, DateTimeField

db = SqliteDatabase('commands.db')

class CommandHistory(Model):
    command = CharField()
    time = DateTimeField()

    class Meta:
        database = db

db.connect()

# Print the contents of the CommandHistory table
print("Command History:")
print("-" * 30)
for entry in CommandHistory.select():
    print('Command: {}, Time: {}'.format(entry.command, entry.time))

db.close()
