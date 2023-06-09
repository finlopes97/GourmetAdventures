from flask import Blueprint, flash, render_template, request, url_for, redirect
from .models import User
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, login_required, logout_user, current_user
from . import db

#create a blueprint
bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():        
    login_form = LoginForm()
    registration_form = RegistrationForm()
    
    if request.method == 'POST':
        if login_form.submitLogin.data and login_form.validate_on_submit():
            print('User has submitted the login form for validation...')
            email = login_form.email.data
            password = login_form.password.data
            remember = login_form.remember_me.data

            # Query the database to see if the user exists
            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                login_user(user, remember=remember)
                return redirect(url_for('main.index'))
            elif not user:
                print('User does not exist')
                flash('User does not exist')
                return redirect(url_for('auth.login'))
            elif not user.check_password(password):
                print('Incorrect password')
                flash('Incorrect password')
                return redirect(url_for('auth.login'))
            
        elif registration_form.submitRegistration.data and registration_form.validate_on_submit():
            print('User has submitted the registration form for validation...')
            username = registration_form.username.data
            email = registration_form.email.data
            password = registration_form.password.data
            confirm_password = registration_form.confirm_password.data

            user = User.query.filter_by(email=email).first()

            if user:
                print('User already exists')
                flash('User already exists')
                return redirect(url_for('auth.login'))
            elif password != confirm_password:
                print('Passwords do not match')
                flash('Passwords do not match')
                return redirect(url_for('auth.login'))
            else:
                print('Creating new user now...')
                new_user = User(username=username, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
            return redirect(url_for('main.index'))    

    return render_template('login.html', login_form=login_form, registration_form=registration_form, heading='Login')

@bp.route('/user', methods=['GET', 'POST'])
def user(booking=None):
    return render_template('user.html', user=current_user, booking=booking)

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# this is a hint for a login function
# @bp.route('/login', methods=['GET', 'POST'])
# def authenticate(): #view function
#     print('In Login View function')
#     login_form = login_form()
#     error=None
#     if(login_form.validate_on_submit()==True):
#         user_name = login_form.user_name.data
#         password = login_form.password.data
#         user = User.query.filter_by(name=user_name).first()
#         if user is None:
#             error='Incorrect credentials supplied'
#         elif not check_password_hash(user.password_hash, password): # takes the hash and password
#             error='Incorrect credentials supplied'
#         if error is None:
#             login_user(user)
#             nextp = request.args.get('next') #this gives the url from where the login page was accessed
#             print(nextp)
#             if next is None or not nextp.startswith('/'):
#                 return redirect(url_for('index'))
#             return redirect(nextp)
#         else:
#             flash(error)
#     return render_template('user.html', form=login_form, heading='Login')
