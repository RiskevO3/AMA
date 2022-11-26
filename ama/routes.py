from flask import redirect,render_template,url_for,flash,request,session
from ama import app,socketio
from ama.models import db,User,Message,generate_bgcolor,validate_login
from ama.forms import LoginForm,MessageForm,RegisterForm
from flask_login import login_user,logout_user,login_required,current_user

@app.errorhandler(404)
def page_not_found(e):
    flash('This page is doesnt exist!',category='error')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))

@app.route('/')
def home_page():
    session['url'] = url_for('home_page')
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login_page():
    if not current_user.is_authenticated:
        session['url'] = url_for('login_page')
        form = LoginForm()
        if form.validate_on_submit():
            return validate_login(username=form.username.data,password=form.password.data)
        return render_template('login.html',form=form)
    flash(f'user is logged in as {current_user.username}.',category='info')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))

@app.route('/register',methods=['GET','POST'])
def register_page():
    if not current_user.is_authenticated:
        session['url'] = url_for('register_page')
        form = RegisterForm()
        if form.validate_on_submit():
            user = User(username=form.username.data,email=form.email.data,password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f'Sukses!, kamu login sebagai {user.username}',category='success')
            return redirect(url_for('user_page'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(err_msg[0],category='error')
        return render_template('register.html',form=form)
    flash(f'Kamu telah login sebagai {current_user.username}',category='info')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))

@app.route('/logout',methods=['GET'])
@login_required
def logout_page():
    logout_user()
    flash('user telah logout!',category='success')
    return redirect(url_for('home_page'))

@app.route('/account',methods=['POST','GET'])
@login_required
def user_page():
    session['url'] = url_for('user_page')
    return render_template('user_page.html')


@app.route('/send/<username>',methods=['POST','GET'])
def send_message_page(username):
    user = User.query.filter_by(username=username).first()
    if user:
        session['url'] = url_for('send_message_page',username=username)
        form = MessageForm()
        if form.validate_on_submit():
            message = Message(name=form.name.data,message=form.message.data,bg_color=generate_bgcolor())
            user.messages.append(message)
            db.session.add_all([user,message])
            db.session.commit()
            socketio.emit(f'{username}',{'name':message.name,'message':message.message,'bg_color':message.bg_color})
            return('pesan anda sudah terkirim!',200)
        if form.errors != {}:
            l_err = []
            for err_msg in form.errors.values():
                l_err.append(err_msg[0])
            return (l_err,400)
        return render_template('send_page.html',form=form,user=user)
    flash('username yang anda cari tidak ada!',category='error')
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('home_page'))


