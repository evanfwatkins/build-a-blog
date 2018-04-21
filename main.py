from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

#TODO 1 - Sumbit a post to the main blog page
#TODO 2 - Get rid of "Main Blog Page" and "Post a Blog" from the register/loing template 
#TODO 3 - Fix the create new blog fucntionality "TItle/Body"


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#SECERET KEY
app.secret_key = "abcdefg1"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    blog = db.Column(db.String(1200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    
    def __init__(self, title, blog, owner):
        self.title = title
        self.blog = blog
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner') 

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash('Logged In')
            return redirect('/')
        else:
            flash('User password incorrect or user does not exist','error')
    
    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existin_user = User.query.filter_by(email=email).first()
        if not existin_user:
            new_user = User(email,password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            #TODO - user better response messaging 
            return "<h1>Duplicate user</h1>"

    return render_template('register.html')
    
@app.route('/logout')    
def logout():
    del session['email']
    return redirect('/')

@app.route('/newblog')
def newblog():
    return render_template('newblog.html')

@app.route('/blog', methods=['POST','GET'])
def blog():
    
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        blog = request.form['blog']

    return render_template('blog.html',title="Blogs", blog=blog)

if __name__ == '__main__':
    app.run()