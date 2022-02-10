from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_potion import Api, ModelResource, fields
from flask_potion.routes import ItemRoute

app = Flask(__name__, template_folder="templates", static_folder="templates", static_url_path="")
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

db.create_all()

class UserResource(ModelResource):
    class Meta:
        model = User

    @ItemRoute.GET
    def greeting(self, user) -> fields.String():
        return "Hello, {}!".format(user.name)

api.add_resource(UserResource)

# Test base route 
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)