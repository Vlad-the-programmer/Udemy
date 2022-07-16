
from flask import Flask, render_template, redirect, url_for, request, jsonify, abort, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf import FlaskForm, csrf
from werkzeug import Response
from wtforms import StringField, IntegerField, FloatField, BooleanField, URLField, SubmitField
from wtforms.validators import DataRequired, URL, Length, Optional
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
    __tablename__ = "cafe"
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

    def __init__(self, name, location, seats, coffe_price, has_sockets, has_toilet, has_wifi, can_take_calls, map_url=None, img_url=None):
        self.name = name

        self.location = location
        self.seats = seats
        self.coffe_price = coffe_price
        self.has_wifi = has_wifi
        self.has_toilet = has_toilet
        self.can_take_calls = can_take_calls
        self.has_sockets = has_sockets
        self.img_url = img_url
        self.map_url = map_url

    def __repr__(self):
        return f"""{self.name} {self.location} {self.seats} {self.coffe_price}-
                Wifi {self.has_wifi} - Sockets {self.has_sockets} - Toilet {self.has_toilet} - Calls {self.can_take_calls}\n"""

    def json(self):
        return {'id': self.id, 'name': self.name, 'img_url': self.img_url, 'location': self.location,
                'has_sockets': self.has_sockets, 'has_wifi': self.has_wifi, 'has_toilet': self.has_toilet,
                'can_take_calls': self.can_take_calls, 'seats': self.seats, 'coffe_price': self.coffe_price
                }


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
    has_sockets = BooleanField('Sockets?',  default=False)
    has_toilet = BooleanField('Toilet?',  default=False)
    has_wifi = BooleanField('Wifi?',  default=False)
    has_take_calls = BooleanField('Take calls',  default=False)
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
    cafes = Cafe.query.all()
    # if request.method == 'POST':
    #     csrf.generate_csrf()
    #     if search_form.validate_on_submit():
    #         searched_cafes = db.session.query(Cafe).filter_by(name=search_form['name'].data).all()
    #         search_form = CafeSearchForm()
    #         return render_template('index.html', searched_cafes=searched_cafes, form=search_form, cafes=cafes)
    #     return redirect(url_for('home'))
    return render_template('index.html', cafes=cafes)


@app.route('/search-cafe', methods=['POST', 'GET'])
def search_cafe():
    search_form = CafeSearchForm()

    csrf.generate_csrf()
    if search_form.validate_on_submit():
        # Does not filter by the boolean values
        searched_cafes = db.session.query(Cafe).filter_by(name=search_form['name'].data,
                                                          location=search_form['location'].data,
                                                          # has_sockets=bool(search_form['has_sockets'].data),
                                                          # has_wifi=bool(search_form['has_wifi'].data),
                                                          # has_toilet=bool(search_form['has_toilet'].data),
                                                          # can_take_calls=bool(search_form['has_take_calls'].data),
                                                          seats=search_form['seats'].data,
                                                          coffe_price=search_form['coffe_price'].data
        ).all()

        return render_template('search_cafe.html', searched_cafes=searched_cafes, form=search_form)
    flash('No cafe was found...', category='error')
    return render_template('search_cafe.html', form=search_form)


# @app.route('/cafe/<int:pk>', methods=['POST', 'GET'])
# def get_cafe(pk):
#     cafe = Cafe.query.get(pk)
#     return cafe_schema.jsonify(cafe)


@app.route('/cafes', methods=['GET'])
def get_cafes():
    cafes = Cafe.query.all()
    return cafe_schemas.jsonify(cafes)


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeCreateForm()
    cafes = Cafe.query.all()

    csrf.generate_csrf()
    request_data = request.form

    if form.validate_on_submit():

        cafe = Cafe(name=request_data.get('name'),
                    location=request_data.get('location'),
                    seats=request_data.get('seats'),
                    coffe_price=request_data.get('coffe_price'),
                    has_sockets=request_data.get('has_sockets', type=bool),
                    has_wifi=request_data.get('has_wifi', type=bool),
                    has_toilet=request_data.get('has_toilet', type=bool),
                    can_take_calls=request_data.get('has_take_calls', type=bool))

        if not cafe:
            flash("Invalid input...", 'error')

        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_cafe.html', form=form, cafes=cafes)


@app.route('/update/<int:pk>', methods=['PUT', 'GET', 'POST'])
def update_cafe(pk):
    cafe = Cafe.query.filter_by(id=pk).first()
    request_data = request.form
    cafes = Cafe.query.all()
    form = CafeCreateForm()
    if request.method == 'POST':
        if cafe:
            db.session.delete(cafe)

            cafe = Cafe(name=request_data.get('name'),
                        location=request_data.get('location'),
                        seats=request_data.get('seats'),
                        coffe_price=request_data.get('coffe_price'),
                        has_sockets=request_data.get('has_sockets', type=bool),
                        has_wifi=request_data.get('has_wifi', type=bool),
                        has_toilet=request_data.get('has_toilet', type=bool),
                        can_take_calls=request_data.get('has_take_calls', type=bool))

            db.session.add(cafe)
            db.session.commit()

            return redirect('/')

        abort_if_cafe_doesnt_exist(pk)
        flash(f'The cafe with the id {pk} does not exist...', 'error')
    return render_template('update_cafe.html', form=form, cafes=cafes)

# Does not work
@app.route('/cafe/<int:pk>/delete', methods=['POST', 'GET'])
def delete_cafe(pk):
    '''Function to delete movie from our database'''
    cafe = Cafe.query.filter_by(id=pk).first()
    cafes = Cafe.query.all()
    if request.method == 'POST':
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return redirect('/')
        abort_if_cafe_doesnt_exist(pk)
        flash('The cafe does not exist...', 'error')

    return render_template('index.html', cafes=cafes)


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

