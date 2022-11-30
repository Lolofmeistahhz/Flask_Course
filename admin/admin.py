from datetime import datetime

from flask import Blueprint, render_template, url_for, redirect, session, request, flash

from admin.forms import LoginForm, PostForm, DishForm
from app import db

from app.models import Users, Posts, Menu, Orders

admin = Blueprint('admin',__name__,template_folder = 'templates',static_folder='static')

menu = [{'name':'Вход','url':'/admin/login'},{'name':'Посты','url':'/admin/delete_post'},{'name':'Блюда','url':'/admin/delete_dishes'},{'name':'Заказы','url':'/admin/orders'},{'name':'О себе','url':'/admin/about'},{'name':'Выйти','url':'/admin/logout'}]

footer = [{'url': 'https://vk.com/lolofmeistahhz', 'class': 'fa-brands fa-vk'},
          {'url': 'https://github.com/Lolofmeistahhz', 'class': 'fa-brands fa-github'},
          {'url': 'https://t.me/lolofmeistahhz', 'class': 'fa-brands fa-telegram'}]


def login_admin():
    session['adminlogged'] = 1

def is_logged():
    return True if session.get('adminlogged') else False


def logout_admin():
    session.pop('admin_logged',None)
    session.clear()

@admin.route('/')
@admin.route('/index')
def index():
    # d = Menu(name='Сырный суп',description = 'Мама мия луиджи, куда ты украл мой сыр? Марио, успокойся - только поробуй этот суп!',price = 99,photo='/admin/static/images/pizza1.jpg')
    # db.session.add(d)
    # db.session.commit()
    return render_template('admin_index.html',title='Админ - панель',menu = menu)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged():
        flash('Вы уже успешно авторизовались в системе',
              category='error')
        return redirect(url_for('.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data, pasword=form.password.data).first()
        if user is not None:
            login_admin()
            flash('Вы  успешно авторизовались в системе',
                  category='success')
            return redirect(url_for('.index'))
        else:
            print('Error')
    return render_template('login.html', title='Авторизация', FlaskForm=form)

@admin.route('/logout')
def logout():
    if not is_logged():
        flash('Вы уже успешно вышли из системы',
              category='error')
        return  redirect(url_for('.index'))
    logout_admin()
    flash('Вы  успешно вышли из системы',
          category='success')
    return redirect(url_for('.index'))

@admin.route('/add_post',methods=['GET', 'POST'])
def add_post():
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        form = PostForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            p = Posts(title=form.title.data, text=form.text.data)
            db.session.add(p)
            db.session.commit()
            flash('Пост был добавлен',
                  category='success')
            return redirect(url_for('.delete_posts'))
        return render_template('add_post.html',title = 'Добавить пост',FlaskForm = form)



@admin.route('/delete_post')
def delete_posts():
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        page = request.args.get('page', 1, type=int)
        pagination = Posts.query.order_by(Posts.id).paginate(page=page, per_page=4)
        return render_template('delete_posts.html', title='Удалить пост',menu=menu,pagination=pagination)


@admin.route('/delete_post/<num>')
def delete_post(num):
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        try:
            post = Posts.query.get_or_404(num)
            db.session.delete(post)
            db.session.commit()
            flash('Пост был удален',
                  category='success')
            return redirect(url_for('.delete_posts'))
        except:
            flash('Пост не был удален',
                  category='error')


@admin.route('/update_post')
def update_posts():
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        page = request.args.get('page', 1, type=int)
        pagination = Posts.query.order_by(Posts.id).paginate(page=page, per_page=4)
        return render_template('delete_posts.html', title='Удалить пост',menu=menu,pagination=pagination)


@admin.route('/update_post/<num>',methods=['GET', 'POST'])
def update_post(num):
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        post = Posts.query.get(num)
        form = PostForm(request.form, csrf_enabled=False)
        if request.method == "POST":
            post.title = form.title.data
            post.text = form.text.data
            post.data = datetime.utcnow()
            db.session.commit()
            flash('Пост был изменен',
                  category='success')
            return redirect(url_for('.update_posts'))
        return render_template('update_posts.html', title='Удалить пост',posts=post,FlaskForm = form)


@admin.route('/delete_dishes')
def delete_dishes():
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        page = request.args.get('page', 1, type=int)
        pagination = Menu.query.order_by(Menu.id).paginate(page=page, per_page=6)
        return render_template('delete_dishes.html', title='Удалить блюдо',menu = menu,pagination=pagination)

@admin.route('/delete_dishes/<num>')
def delete_dish(num):
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        try:
            dish = Menu.query.get_or_404(num)
            db.session.delete(dish)
            db.session.commit()
            flash('Блюдо было удалено',
                  category='success')
            return redirect(url_for('.delete_dishes'))
        except:
            flash('Блюдо не было удалено',
                  category='error')


@admin.route('/add_dishes',methods=['GET', 'POST'])
def add_dish():
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        form = DishForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            d = Menu(name=form.name.data, description=form.description.data,price=form.price.data,photo=form.photo.data)
            db.session.add(d)
            db.session.commit()
            flash('Блюдо было добавлено',
                  category='success')
            return redirect(url_for('.delete_dishes'))
        return render_template('add_dish.html',title = 'Добавить блюдо',FlaskForm = form)

@admin.route('/update_dish')
def update_dishes():
    dish = db.session.query(Menu).order_by(Menu.id).all()
    return render_template('update_dishes.html', title='Удалить блюдо',menu=menu,dish=dish)

@admin.route('/update_dish/<num>',methods=['GET', 'POST'])
def update_dish(num):
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        dish = Menu.query.get(num)
        form = DishForm(request.form, csrf_enabled=False)
        if request.method == "POST":
            dish.name = form.name.data
            dish.description = form.description.data
            dish.price = form.price.data
            dish.photo = form.photo.data
            db.session.commit()
            flash('Информация о блюде была изменена',
                  category='success')
            return redirect(url_for('.delete_dishes'))
        return render_template('update_dishes.html', title='Удалить блюдо',dish=dish,FlaskForm = form)

@admin.route('/orders')
def orders():
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        page = request.args.get('page', 1, type=int)
        pagination = Orders.query.order_by(Orders.id).paginate(page=page, per_page=5)
        dishes = db.session.query(Menu.id,Menu.name,Menu.price).order_by(Menu.id).all()
        return render_template('orders.html', title='Заказы',menu=menu,pagination=pagination,dishes = dishes)

@admin.route('/orders/<num>')
def delete_order(num):
    if not is_logged():
        return redirect(url_for('.login'))
    elif is_logged():
        try:
            order = Orders.query.get_or_404(num)
            db.session.delete(order)
            db.session.commit()
            flash('Информация о заказе была удалена',
                  category='success')
            return redirect(url_for('.orders'))
        except:
            flash('Произошел сбой',
                  category='error')

@admin.route('/about')
def about():
    return render_template('about.html', title='О себе',menu=menu)