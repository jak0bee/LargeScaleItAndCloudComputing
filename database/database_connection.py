from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


database_url = "mysql+pymysql://admin:wawmoz-juqre4-ragsYh@aws-lsitcc.cnke6sycown6.eu-north-1.rds.amazonaws.com/Main"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socket = SocketIO(app)

db = SQLAlchemy(app)


# Print the connected database name
with app.app_context():
    query = db.text("SELECT DATABASE();")
    result = db.session.execute(query)
    for row in result:
        print(f"Connected to database: {row[0]}")



