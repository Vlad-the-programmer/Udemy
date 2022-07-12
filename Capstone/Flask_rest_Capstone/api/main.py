from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, RadioField, URLField, SubmitField
from wtforms.validators import DataRequired, URL, Length
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'vlad123'
db = SQLAlchemy(app)
Bootstrap(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

csrf = CSRFProtect(app)


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


@app.route('/', methods=['POST', 'GET'])
def home():
    cafes = Cafe.query.all()
    search_form = CafeSearchForm()
    if request.method == 'POST':

        # cafe_data = request.search_form
        searched_cafes = db.session.query(Cafe).filter_by(name=search_form['name'], location=search_form['location'])

        return redirect(url_for('home')), searched_cafes
    return render_template('index.html', cafes=cafes, form=search_form)


if '__main__' == __name__:
    app.run(debug=True, port=5000, use_reloader=True)