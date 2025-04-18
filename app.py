import os
from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/link-vault'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


# user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=request.form['username'], email=request.form['email'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return "User registered!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            return "Login successful!"
        return "Invalid credentials!"
    return render_template('login.html')

@app.route('/upload', methods = ["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file.filename == "":
            return "No file selected"
        else:
            filename =secure_filename(uploaded_file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(file_path)
            return f"File uploaded successfully: {filename}"

    return render_template("upload.html")

@app.route('/')
def hello():
    return "Link Vault Home Page"


if __name__ == '__main__':
    app.run(debug = True)