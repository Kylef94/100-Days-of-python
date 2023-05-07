from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/all")
def get_all():
    all_cafes = db.session.query(Cafe).all()
    return jsonify(cafes= [cafe.to_dict() for cafe in all_cafes])

@app.route("/search")
def search():
    location = request.args.get("loc")
    cafe = Cafe.query.filter_by(location=location).first()

    if cafes:
        return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location"})


## HTTP GET - Read Record

@app.route("/random")
def get_random_cafe():
    with app.app_context():
        all_cafes = db.session.query(Cafe).all()
        random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())

## HTTP POST - Create Record

@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_price(cafe_id):
    new_price = request.args.get('new_price')
    with app.app_context():
        cafe = db.session.query(Cafe).get(cafe_id)

    if cafe:
        with app.app_context():
            cafe.coffee_price = new_price
            db.session.commit()
        return jsonify(success="Successfully updated the price.")

    else:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in our database"})
## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
