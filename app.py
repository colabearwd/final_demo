# encoding: utf-8
from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User
from exts import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u"手机号码或者密码错误"


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('phonenumber')
        username = request.form.get('username')
        passwd1 = request.form.get('passwd1')
        passwd2 = request.form.get('passwd2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u"该手机号以及被注册"
        else:
            if passwd1 != passwd2:
                return u"两次密码不同"
            else:
                user = User(telephone=telephone, username=username, password=passwd1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.context_processor
def my_content_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

@app.route('logout')
def logout():
    session.pop('user_id')
    #del  session.__delattr__('user_id')
    # session.clear
    return redirect('index')



if __name__ == '__main__':
    app.run()
