from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    role = SelectField('Role', choices=[('admin', 'Admin'), ('student', 'Student')], validators=[DataRequired()])
    
    submit = SubmitField('Sign Up')
    
    # checking if username exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Account already exists. Please choose a different one.')
    
    
class LoginForm(FlaskForm):
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
   
    role = SelectField('Role', choices=[('admin', 'Admin'), ('student', 'Student')], validators=[DataRequired()])
    
    submit = SubmitField('Update')
    
    # checking if username exists
    def validate_username(self, username):
        if username.data != current_user.username:
            
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Account already exists. Please choose a different one.')
            
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    post_type = SelectField('Application Type', choices=[
        ('Bursaries', 'Bursaries'),
        ('Scholarships', 'Scholarships'),
        ('Grants', 'Grants')
    ], validators=[DataRequired()])
    application_deadline = StringField('Application Deadline', validators=[DataRequired()])
    eligibility_criteria = TextAreaField('Eligibility Criteria', validators=[DataRequired()])
    funding_amount = IntegerField('Funding Amount ', validators=[DataRequired()])
    contact_email = StringField('Contact Email', validators=[DataRequired()])
    choose_career = SelectField('Choose Career', choices=[
        ('1', 'Information Technology'),
        ('2', 'Healthcare'),
        ('3', 'Engineering'),
        ('4', 'Finance'),
        ('5', 'Education'),
        ('6', 'Marketing'),
        ('7', 'Hospitality'),
        ('8', 'Art and Design'),
        ('9', 'Law'),
        ('10', 'Construction')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Create')
    
class ApplicationForm(FlaskForm):
    title = SelectField('Title', choices=[('mr', 'Mr'), ('mrs', 'Mrs'), ('ms', 'Ms')], validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    full_name = StringField('Full Name', validators=[InputRequired()])
    id_number = StringField('ID Number', validators=[InputRequired()])
    ethnicity = SelectField('Ethnicity', choices=[('african', 'African'), ('white', 'White'), ('indian', 'Indian'), ('coloured', 'Coloured')], validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired()])
    motivation = TextAreaField('Motivation', validators=[InputRequired()])
    registration_proof = FileField('Registration Proof', validators=[InputRequired()])
    id_copy = FileField('ID Copy', validators=[InputRequired()])
    academic_results = FileField('Academic Results', validators=[InputRequired()])
    submit = SubmitField('Submit')
	