from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.models import User


class InputForm(FlaskForm):
    task = StringField('Task Content:', validators=[DataRequired()])
    creator = StringField('Creator:', validators=[DataRequired()])
    assign = StringField('Assignee:', validators=[DataRequired()])
    endtime = DateField('End Time:', validators=[DataRequired()])
    status = SelectField('Status:', choices=['Created', 'Processed', 'Finished'])
    submit = SubmitField('Create')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username= StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复')
