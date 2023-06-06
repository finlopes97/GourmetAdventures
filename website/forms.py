from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from .models import User

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[InputRequired(), Email(), Length(max=120)], render_kw={"class": "form-control"})
	password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)], render_kw={"class": "form-control"})
	remember_me = BooleanField('Remember Me', default=False, render_kw={"class": "form-check-input"})
	
	submitLogin = SubmitField('Login', render_kw={"class": "btn btn-primary"})

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64)], render_kw={"class": "form-control", "placeholder": "foodlover"})
	email = StringField('Email', validators=[InputRequired(), Email(), Length(max=120)], render_kw={"class": "form-control", "placeholder": "foodlover@email.com"})
	password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)], render_kw={"class": "form-control"})
	confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')], render_kw={"class": "form-control"})
	
	submitRegistration = SubmitField('Sign Up', render_kw={"class": "btn btn-primary"})
	
	def validate_email(self, email):
		# Check if email is already taken
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is already taken.')