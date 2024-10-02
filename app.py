from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import base64

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///user.db'

db = SQLAlchemy(app)

class User(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), nullable = False)
    image = db.Column(db.LargeBinary, nullable = True)

with app.app_context():
    db.create_all()

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        username = request.form['username']
        image = request.files['image'].read()
        new_user = User(
            username = username,
            image = image
        )
        db.session.add(new_user)
        db.session.commit()
    return render_template("index.html")

@app.route('/database')
def database():
    users = User.query.all()
    images = db.session.query(User).all()

    image_list = []
    for i in images:
        image = base64.b64encode(i.image).decode('ascii')
        image_list.append(image)
    return render_template("database.html", users = users, images = image_list)

if __name__ == "__main__":
    app.run(debug=True)