from admin.admin import admin
from app import app, db
from flask import render_template, request
from app.forms import OrderForm
from app.models import Users, Posts, Menu, Orders


app.register_blueprint(admin,url_prefix='/admin')


menu = [{'name': 'Главная', 'url': '/index'}, {'name': 'Новости', 'url': '/posts'}, {'name': 'Меню', 'url': '/dishes'},
        {'name': 'Контакты', 'url': '/index#contacts'}, {'name': 'Оформить заказ', 'url': '/do_order'}]

footer = [{'url': 'https://vk.com/lolofmeistahhz', 'class': 'fa-brands fa-vk'},
          {'url': 'https://github.com/Lolofmeistahhz', 'class': 'fa-brands fa-github'},
          {'url': 'https://t.me/lolofmeistahhz', 'class': 'fa-brands fa-telegram'}]



@app.route('/')
@app.route('/index')
def index():
    posts = Posts.query.order_by(Posts.id.desc()).limit(5).all()
    return render_template('index.html', title='Главная', menu=menu, footer=footer, posts=posts)


@app.route('/posts')
def posts():
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.order_by(Posts.id).paginate(page=page, per_page=10)
    return render_template("posts.html", pagination=pagination, menu=menu, footer=footer)


@app.route('/dishes')
def dishes():
    page = request.args.get('page', 1, type=int)
    pagination = Menu.query.order_by(Menu.id).paginate(page=page, per_page=12)
    return render_template("dishes.html", pagination=pagination, menu=menu, footer=footer)



@app.route('/post/<num>')
def post(num):
    post = Posts.query.filter(Posts.id == num)
    return render_template("post.html", menu=menu, post=post)





@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        if form.password.data == form.password2.data:
            u = Users(login=form.login.data, pasword=form.password.data)
            db.session.add(u)
            db.session.commit()
        else:
            print('eeerrr')
    return render_template('register.html', title='Регистрация', FlaskForm=form)


@app.route('/do_order', methods=['GET', 'POST'])
def do_order():
    dishes = Menu.query.order_by(Menu.id).all()
    form = OrderForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        price1 = db.session.query(Menu.price).filter_by(id=int(*form.dish1.raw_data)).first()
        price2 = db.session.query(Menu.price).filter_by(id=int(*form.dish2.raw_data)).first()
        price3 = db.session.query(Menu.price).filter_by(id=int(*form.dish3.raw_data)).first()
        price4 = db.session.query(Menu.price).filter_by(id=int(*form.dish4.raw_data)).first()
        price5 = db.session.query(Menu.price).filter_by(id=int(*form.dish5.raw_data)).first()
        amo = int(*price1) + int(*price2) + int(*price3) + int(*price4) + int(*price5)
        if form.submit2.__call__():
            o = Orders(dish1=form.dish1.data, dish2=form.dish2.data, dish3=form.dish3.data, dish4=form.dish4.data,
                           dish5=form.dish5.data,amount = amo)
            db.session.add(o)
            db.session.commit()
        return render_template("do_order.html", menu=menu, footer=footer, dishes=dishes, FlaskForm=form, amo=amo)
    else:
        return render_template("do_order.html", menu=menu, footer=footer, dishes=dishes, FlaskForm=form)
