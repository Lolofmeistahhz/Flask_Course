from datetime import datetime

from flask import Blueprint, render_template, url_for, redirect, session, request

from app import db
from app.forms import LoginForm, PostForm
from app.models import Users, Posts, Menu

admin = Blueprint('admin',__name__,template_folder = 'templates',static_folder='static')

menu = [{'name':'Посты','url':'/admin/delete_post'},{'name':'Добавить блюдо','url':'/admin/add_dish'},{'name':'Заказы','url':'/admin/orders'}]

footer = [{'url': 'https://vk.com/lolofmeistahhz', 'class': 'fa-brands fa-vk'},
          {'url': 'https://github.com/Lolofmeistahhz', 'class': 'fa-brands fa-github'},
          {'url': 'https://t.me/lolofmeistahhz', 'class': 'fa-brands fa-telegram'}]


def login_admin():
    session['adminlogged'] = 1

def is_logged():
    return True if session.get('adminligged') else False


def logout_admin():
    session.pop('admin_logged',None)

@admin.route('/')
@admin.route('/index')
def index():
    # d = Menu(name='Сырный суп',description = 'Мама мия луиджи, куда ты украл мой сыр? Марио, успокойся - только поробуй этот суп!',price = 99,photo='/admin/static/images/pizza1.jpg')
    # db.session.add(d)
    # db.session.commit()
    return render_template('admin_index.html',title='Админ - панель',menu = menu)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data, pasword=form.password.data).first()
        if user is not None:
            login_admin()
            return redirect(url_for('.index'))
        else:
            print('Error')
    return render_template('login.html', title='Авторизация', FlaskForm=form)

@admin.route('/logout')
def logout():
    if not is_logged():
        return  redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))

@admin.route('/add_post',methods=['GET', 'POST'])
def add_post():
    form = PostForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        p = Posts(title=form.title.data, text=form.text.data)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('add_post.html',title = 'Добавить пост',FlaskForm = form)



@admin.route('/delete_post')
def delete_posts():
    posts = db.session.query(Posts).order_by(Posts.id).all()
    return render_template('delete_posts.html', title='Удалить пост',menu=menu,posts=posts)


@admin.route('/delete_post/<num>')
def delete_post(num):
    try:
        post = Posts.query.get_or_404(num)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('.delete_posts'))
    except:
        return 'error'


@admin.route('/update_post')
def update_posts():
    posts = db.session.query(Posts).order_by(Posts.id).all()
    return render_template('delete_posts.html', title='Удалить пост',menu=menu,posts=posts


@admin.route('/update_post/<num>',methods=['GET', 'POST'])
def update_post(num):
    post = Posts.query.get(num)
    form = PostForm(request.form, csrf_enabled=False)
    if request.method == "POST":
        post.title = form.title.data
        post.text = form.text.data
        post.data = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('.update_posts'))
    return render_template('update_posts.html', title='Удалить пост',menu=menu,posts=post,FlaskForm = form)





