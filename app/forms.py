from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

from app.models import Menu


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Вход')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, *kwargs)


class RegForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])
    submit = SubmitField('Регистрация')

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)


class OrderForm(FlaskForm):
    dish1 = SelectField()
    dish2 = SelectField()
    dish3 = SelectField()
    dish4 = SelectField()
    dish5 = SelectField()
    amount = IntegerField()
    submit1 = SubmitField('Рассчитать стоимость заказа',validators=[DataRequired()])
    submit2 = SubmitField('Сделать заказ')


    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.dish1.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.dish2.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.dish3.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.dish4.choices = [(c.id,c.name)for c in Menu.query.all()]
        self.dish5.choices = [(c.id, c.name) for c in Menu.query.all()]

class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    text = StringField('text', validators=[DataRequired()])
    submit = SubmitField('Добавить',validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

