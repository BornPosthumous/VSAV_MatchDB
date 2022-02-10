from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from urllib.parse import quote
import os

app = Flask(__name__, template_folder="templates", static_folder="templates", static_url_path="")

credentials = {
    'username'  : os.environ['DB_USERNAME'],
    'password'  : os.environ['DB_PASSWORD'],
    'host'      : os.environ['DB_HOST'],
    'database'  : os.environ['DB_DATABASE'],
    'port'      : os.environ['DB_PORT'],
}
app = Flask(__name__)
print(credentials)
# postgresql://username:password@localhost:port/database
con_string = f"postgresql://{credentials['username']}:%s@{credentials['host']}:5432/{credentials['database']}" % quote('dem0nscr@d00')

app.config['SQLALCHEMY_DATABASE_URI'] = con_string
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TestModel(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String())
    price = db.Column(db.Integer())

    def __init__(self, model, doors):
        self.model = model
        self.doors = doors

    def __repr__(self):
        return f"<Test {self.model}>"

@app.route('/test')
def runtest():
    v = TestModel.query.all()
    print(v)
    return 'OK'

# Test base route 
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7000, debug=True)