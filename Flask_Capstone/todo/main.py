from flask import Flask, render_template, url_for, redirect, request, flash, get_flashed_messages, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields import TextAreaField, SubmitField, StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm
from wtforms.widgets import TextArea

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'vlad1234'
login_manager = LoginManager(app)
login_manager.init_app(app)

db = SQLAlchemy(app)
Bootstrap(app)

# csrf = CSRFProtect()
# csrf.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.before_first_request
def create_db():
    db.create_all()


class LoginForm(FlaskForm):
    email = EmailField('Your name', [DataRequired(), Email()])
    password = PasswordField('Your password', [DataRequired()])
    login = SubmitField('Login')


class SignUpForm(FlaskForm):
    username = StringField('Your name', [DataRequired(), Length(min=3)])
    email = EmailField(label='Your email', validators=[DataRequired(), Email()])
    password = PasswordField('Create a password with the length no less then 6 characters...', [DataRequired(), Length(min=6)])
    password_conf = PasswordField('Confirm your password', [DataRequired(), EqualTo(password)])
    signup = SubmitField('SignUp')


class ToDoForm(FlaskForm):
    canvas = TextAreaField(label='Enter a task...', validators=[DataRequired()], widget=TextArea())


class ToDo(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50))

    def __int__(self, task_data):
        # super().__init__()
        self.task = task_data

    def __repr__(self):
        return f'{self.id} {self.task}'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return f'{self.id} { self.username} {self.email} {self.password}'

    def __init__(self, username, email, password):

        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = ToDoForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            canvas_data = request.form['canvas']
            task = ToDo(task=canvas_data)
            db.session.add(task)
            db.session.commit()
            return redirect('/')
    tasks = ToDo.query.all()

    return render_template('home.html', form=form, user=current_user, tasks=tasks)


@app.route('/delete/<int:pk>', methods=['GET', 'POST'])
def delete(pk):
    form = ToDoForm()
    tasks = ToDo.query.all()
    if request.method == 'GET':
        task = ToDo.query.get(pk)
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('home.html', user=current_user, form=form, tasks=tasks)


@app.route('/update/<int:pk>', methods=['GET', 'POST'])
def update(pk):
    task = ToDo.query.get(pk)
    print(task)
    form = ToDoForm()
    if request.method == 'POST':
        if task:
            db.session.delete(task)
            db.session.commit()

            task = request.form['canvas']

            new_task = ToDo(task=task)
            db.session.add(new_task)
            db.session.commit()

            return redirect(url_for('home'))
        return f"Employee with id = {pk} Does nit exist"
    return render_template('update.html', user=current_user, form=form, task=task)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    user = db.session.query(User).filter(User.email == login_form['email'].data).first()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            if user and login_form.password.data == user.password:
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('You should register prior to logging in!', category='error')
                redirect(url_for('sign_up'))

    return render_template('login.html', form=login_form, user=current_user)


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    signup_form = SignUpForm()
    if request.method == 'POST':
        if signup_form.validate_on_submit():
            if not User.query.filter_by(email=signup_form.email):
                user = User(username=signup_form.username, email=signup_form.email, password=signup_form.password)
                db.session.add(user)
                db.session.commit()
                return redirect('/')
            else:
                flash('The user already exists...', category='error')
                redirect(url_for('login'))

    return render_template('signup.html', form=signup_form)


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


if '__main__' == __name__:
    SERVER_NAME = 'local.host:8000'
    app.run(debug=True, port=8000, use_reloader=True)


