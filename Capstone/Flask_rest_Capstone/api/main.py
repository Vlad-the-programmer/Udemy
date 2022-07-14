import json

from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf import FlaskForm, csrf
from werkzeug import Response
from wtforms import StringField, IntegerField, FloatField, BooleanField, RadioField, URLField, SubmitField
from wtforms.validators import DataRequired, URL, Length
from flask_restful import Api, Resource, marshal_with, fields, reqparse
from flask_marshmallow import Marshmallow


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'vlad123'
db = SQLAlchemy(app)
Bootstrap(app)

api = Api(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

mm = Marshmallow(app)

@app.before_first_request
def create_db():
    db.create_all()


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=True)
    has_toilet = db.Column(db.Boolean, nullable=True)
    has_wifi = db.Column(db.Boolean, nullable=True)
    can_take_calls = db.Column(db.Boolean, nullable=True)
    seats = db.Column(db.Integer, nullable=True)
    coffe_price = db.Column(db.Float, nullable=True)

    def __init__(self, name, location, seats, coffe_price, has_sockets, has_toilet, has_wifi, can_take_calls):
        self.name = name
        self.location = location
        self.seats = seats
        self.coffe_price = coffe_price
        self.has_wifi = has_wifi
        self.has_toilet = has_toilet
        self.can_take_calls = can_take_calls
        self.has_sockets = has_sockets

    def __repr__(self):
        return f'{self.name} {self.location} {self.seats} {self.coffe_price}'

    def json(self):
        return {'id': self.id, 'name': self.name, 'img_url': self.img_url, 'location': self.location,
                'has_sockets': self.has_sockets, 'has_wifi': self.has_wifi, 'has_toilet': self.has_toilet,
                'can_take_calls': self.can_take_calls, 'seats': self.seats, 'coffe_price': self.coffe_price
                }

    def get_all_cafes(self):
        return [Cafe.json(cafe) for cafe in Cafe.query.all()]

    def get_cafe(self, _id):
        return [Cafe.json(Cafe.query.get(id=_id).first())]

    def add_cafe(self, _name, _location, _seats, _coffe_price, _has_sockets, _has_wifi, _has_toilet, _can_take_calls):
        new_cafe = Cafe(name=_name, location=_location, seats=_seats, coffe_price=_coffe_price,
                        has_sockets=_has_sockets, has_wifi=_has_wifi, has_toilet=_has_toilet,
                        can_take_calls=_can_take_calls)
        db.session.add(new_cafe)
        db.session.commit()
        return new_cafe

    # def update_cafe(_id, _name, _location, _seats, _coffe_price):
    #     '''function to update the details of a movie using the id, name,
    #     location, seats and coffee price as parameters'''
    #     cafe_to_update = Cafe.query.filter_by(id=_id).first()
    #     cafe_to_update.name = _name
    #     cafe_to_update.year = _location
    #     cafe_to_update.seats = _seats
    #     cafe_to_update.coffe_price = _coffe_price
    #
    #     db.session.commit()

    def delete_cafe(_id):
        '''function to delete a cafe from our database using
           the id of the movie as a parameter'''
        Cafe.query.filter_by(id=_id).delete()
        # filter movie by id and delete
        db.session.commit()


class CafeSchema(mm.Schema):
    class Meta:
        fields = ('id', 'name', 'location', 'seats', 'coffe_price')


class CafeSearchForm(FlaskForm):
    name = StringField('A name', [DataRequired(), Length(min=3)])
    location = StringField('A location', [DataRequired(), Length(min=4)])
    has_sockets = BooleanField('Sockets?')
    has_toilet = BooleanField('Toilet?')
    has_wifi = BooleanField('Wifi?')
    has_take_calls = BooleanField('Take calls')
    seats = IntegerField('Seats')
    coffe_price = FloatField('A coffe price')
    search_cafes = SubmitField('Search for cafes')


class CafeCreateForm(FlaskForm):
    name = StringField('A name of a cafe', [DataRequired(), Length(min=3)])
    map_url = URLField('A map url', [URL(), DataRequired()])
    img_url = URLField('An image url', [URL(), DataRequired()])
    location = StringField('Location', [DataRequired(), Length(min=4)])
    has_sockets = BooleanField('Sockets?', [DataRequired()])
    has_toilet = BooleanField('Toilet?', [DataRequired()])
    has_wifi = BooleanField('Wifi?', [DataRequired()])
    has_take_calls = BooleanField('Take calls', [DataRequired()])
    seats = IntegerField('Seats', [DataRequired()])
    coffe_price = FloatField('A coffe price', [DataRequired()])
    create_cafe = SubmitField('Create a cafe')

#
# parser = reqparse.RequestParser()
# parser.add_argument('name', type=str, help='A name of a cafe')
# parser.add_argument('location', type=str, help='A location of a cafe')
# parser.add_argument('coffe_price', type=float, help='A price of a cafe')
# parser.add_argument('seats', type=int, help='A number of seats')
# parser.add_argument('img_url', type=str, help='A url of a cafe\'s image')
# parser.add_argument('has_sockets', type=bool, help='Does a cafe has sockets')
# parser.add_argument('has_toilet', type=bool, help='Does a cafe has toilet')
# parser.add_argument('has_wifi', type=bool, help='Does a cafe has wifi')
# parser.add_argument('can_take_calls', type=bool, help='Can you take calls there')


cafe_schema = CafeSchema()
cafe_schemas = CafeSchema(many=True)


def abort_if_cafe_doesnt_exist(cafe_id):
    if not Cafe.query.get(cafe_id):
        abort(404, f'Cafe {cafe_id} does not exist')


data_format = {
    'id': fields.Integer,
    'name': fields.String,
    'location': fields.String,
    'coffe_price': fields.Float,
}


@app.route('/', methods=['POST', 'GET'])
def home():
    search_form = CafeSearchForm()

    if request.method == 'POST':
        csrf.generate_csrf()
        if search_form.validate_on_submit():
            searched_cafes = db.session.query(Cafe).filter_by(name=search_form['name'].data).all()
            search_form = CafeSearchForm()
            return render_template('index.html', searched_cafes=searched_cafes, form=search_form, cafes=jsonify(Cafe.get_all_cafes()))
        return redirect(url_for('home'))
    return render_template('index.html', form=search_form, cafes=jsonify(Cafe.get_all_cafes()))


@app.route('/cafe/<int:pk>', methods=['POST', 'GET'])
def get_cafe(pk):
    cafe = Cafe.query.get(pk)
    return cafe_schema.jsonify(cafe)


@app.route('/cafes', methods=['GET'])
def get_cafes():
    cafes = Cafe.query.all()

    return cafe_schemas.jsonify(cafes)


@app.route('/add', methods=['POST', 'GET'])
def add_movie():
    request_data = request.get_json()
    # cafe = Cafe.add_cafe(request_data['name'], request_data['location'], request_data['seats'],\
    #               request_data['coffe_price'], request_data['has_sockets'], request_data['has_wifi'],\
    #               request_data['has_toilet'], request_data['can_take_calls'])
    # response = Response("Movie added", 201, mimetype='application/json')
    cafe = Cafe(name=request_data['name'], location=request_data['location'], seats=request_data['seats'],\
                  coffe_price=request_data['coffe_price'], has_sockets=request_data['has_sockets'], has_wifi=request_data['has_wifi'],\
                  has_toilet=request_data['has_toilet'], can_take_calls=request_data['can_take_calls'])

    return cafe_schema.jsonify(cafe)


@app.route('/update/<int:pk>', methods=['PUT'])
def update_cafe(pk):
    request_data = request.get_json()

    cafe = Cafe.query.filter_by(id=pk).first()
    cafe.name = request_data['name']
    cafe.location = request_data['location']
    cafe.seats = request_data['seats']
    cafe.coffe_price = request_data['coffe_price']
    cafe.has_sockets = request_data['has_sockets']
    cafe.has_wifi = request_data['has_wifi']
    cafe.has_toilet = request_data['has_toilet']
    cafe.can_take_calls = request_data['can_take_calls']

    db.session.commit()
    return cafe_schema.jsonify(cafe)


@app.route('/movies/<int:id>', methods=['DELETE'])
def remove_movie(id):
    '''Function to delete movie from our database'''

    Cafe.delete_movie(id)
    response = Response("Movie Deleted", status=200, mimetype='application/json')
    return response


# class Cafes(Resource):
#     @marshal_with(data_format)
#     def get(self):
#         return Cafe.query.all()
#
#
# class CafeItem(Resource):
#     @marshal_with(data_format)
#     def get(self, pk):
#         cafe = Cafe.query.get(pk)
#         abort_if_cafe_doesnt_exist(pk)
#         return cafe
#
#     def post(self):
#         data = parser.parse_args()
#         cafe_id = len(Cafe.query.all())+1
#         new_cafe = Cafe(name=data['name'], location=data['location'], has_sockets=data['has_sockets'], \
#                         has_toilet=data['has_toilet'], has_wifi=data['has_wifi'],\
#                         can_take_calls=data['can_take_calls'], seats=data['seats'], coffe_price=data['coffe_price'])
#
#         db.session.add(new_cafe)
#         db.session.commit()
#         return new_cafe
#
#     @marshal_with(data_format)
#     def put(self, pk):
#         data = parser.parse_args()
#
#         updated_cafe = Cafe(name=data['name'], location=data['location'], has_sockets=data['has_sockets'],\
#                     has_toilet=data['has_toilet'], has_wifi=data['has_wifi'], can_take_calls=data['can_take_calls'],\
#                     seats=data['seats'], coffe_price=data['coffe_price'])
#
#         cafe = Cafe.query.get(pk)
#         abort_if_cafe_doesnt_exist(pk)
#         db.session.add(cafe)
#         db.session.commit()
#         return cafe, 201
#
#     def delete(self, pk):
#         cafe = Cafe.query.get(pk)
#         abort_if_cafe_doesnt_exist(cafe)
#         del cafe
#         return {'response': "Object {pk} was deleted successfully!"}, 204
#
#
# api.add_resource(CafeItem, '/cafe/<int:pk>')
# api.add_resource(Cafes, '/cafes')







if '__main__' == __name__:
    app.run(debug=True, port=5000, use_reloader=True)

