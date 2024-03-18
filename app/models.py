from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False) 
    role = db.Column(db.String(20), nullable=False)  # Add role field to distinguish between admin and student
    posts = db.relationship('Post', backref='author', lazy=True)
    applications = db.relationship('Application', backref='applicant', lazy=True)  # Add relationship to applications
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(20), nullable=False)
    application_deadline = db.Column(db.String(50), nullable=False)  # Add application_deadline field
    eligibility_criteria = db.Column(db.Text, nullable=False)  # Add eligibility_criteria field
    funding_amount = db.Column(db.Integer, nullable=False)  # Add funding_amount field
    contact_email = db.Column(db.String(120), nullable=False)  # Add contact_email field
    choose_career = db.Column(db.String(50), nullable=False)  # Add choose_career field
   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applications = db.relationship('Application', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10), nullable=False)  # Assuming titles are abbreviated (e.g., Mr., Mrs., etc.)
    surname = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    id_number = db.Column(db.String(20), nullable=False)
    ethnicity = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    motivation = db.Column(db.Text, nullable=False)
    registration_proof_filename = db.Column(db.String(100), nullable=False)
    id_copy_filename = db.Column(db.String(100), nullable=False)
    academic_results_filename = db.Column(db.String(100), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f"Application('{self.title}', '{self.full_name}', '{self.date_applied}')"