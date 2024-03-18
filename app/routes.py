import os
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ApplicationForm
from app.models import User, Post, Application
from flask_login import login_user, current_user, logout_user, login_required  
from werkzeug.utils import secure_filename  


@app.route("/")
@app.route("/home")
def home():
    query = request.args.get('query', '')  

    if query:
        # Perform a search for applications based on the query
        applications = Post.query.filter(Post.title.ilike(f'%{query}%')).all()
    else:
        # Fetch all applications if no search query is provided
        applications = Post.query.all()

    return render_template('home.html', applications=applications, query=query, title = 'Home')
    


@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Check if the role is admin or student
        role = form.role.data
        if role not in ['admin', 'student']:
            flash('Invalid role selected.', 'danger')
            return redirect(url_for('register'))

        # Create the user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:   
            flash('login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.role = form.role.data 
        db.session.commit()
        flash('Account updated successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username 
        form.email.data = current_user.email 
        form.role.data = current_user.role
    return render_template('account.html', title='Account', form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.role != 'admin':
        flash('You are not authorized to create applications.', 'danger')
        return redirect(url_for('login'))

    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post_type = form.post_type.data
        application_deadline = form.application_deadline.data
        eligibility_criteria = form.eligibility_criteria.data
        funding_amount = form.funding_amount.data
        contact_email = form.contact_email.data
        choose_career = form.choose_career.data
        

        # Create the post with the specified type and assign the current user as the author
        post = Post(
            title=title,
            content=content,
            post_type=post_type,
            application_deadline=application_deadline,
            eligibility_criteria=eligibility_criteria,
            funding_amount=funding_amount,
            contact_email=contact_email,
            choose_career=choose_career,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()

        flash('Application created successfully!', 'success')
        return redirect(url_for('home'))  # Redirect to home after creating the application

    return render_template('create_post.html', title='Create Application', form=form, legend='Create Application')
	

def tpost(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>')
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    return render_template('post.html', title=post.title, post=post)

    
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.all()
    post = Post.query.get_or_404(post_id)
    # Determine the template based on post_type
    if post.post_type == 'Bursaries':
        template = 'bursaries.html'
    elif post.post_type == 'Scholarships':
        template = 'scholarships.html'
    elif post.post_type == 'Grants':
        template = 'grants.html'
    else:
        template = 'default_post.html'  # Provide a default template if post_type is not recognized
    return render_template(template, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # Forbidden error if the current user is not the author of the post
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Application has been updated!', 'info')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data= post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Application', form=form
                           , legend='Update Application')
    
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # Forbidden error if the current user is not the author of the post
    db.session.delete(post)
    db.session.commit()
    flash('Deleted application successfully', 'info')
    return redirect(url_for('home'))
     
    

@app.route('/bursaries')
@login_required
def bursaries():
    bursaries_posts = Post.query.filter_by(post_type='Bursaries').all()
    return render_template('bursaries.html', posts=bursaries_posts)

@app.route('/scholarships')
@login_required
def scholarships():
    scholarships_posts = Post.query.filter_by(post_type='Scholarships').all()
    return render_template('scholarships.html', posts=scholarships_posts)

@app.route('/grants')
@login_required
def grants():
    grants_posts = Post.query.filter_by(post_type='Grants').all()
    return render_template('grants.html', posts=grants_posts)

@app.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    form = ApplicationForm()
    if form.validate_on_submit():
        # Save uploaded files
        registration_proof_filename = secure_filename(form.registration_proof.data.filename)
        id_copy_filename = secure_filename(form.id_copy.data.filename)
        academic_results_filename = secure_filename(form.academic_results.data.filename)
        
        registration_proof_path = os.path.join(app.config['UPLOAD_FOLDER'], registration_proof_filename)
        id_copy_path = os.path.join(app.config['UPLOAD_FOLDER'], id_copy_filename)
        academic_results_path = os.path.join(app.config['UPLOAD_FOLDER'], academic_results_filename)

        form.registration_proof.data.save(registration_proof_path)
        form.id_copy.data.save(id_copy_path)
        form.academic_results.data.save(academic_results_path)

        # Create new application object and save to database
        new_application = Application(
            title=form.title.data,
            surname=form.surname.data,
            full_name=form.full_name.data,
            id_number=form.id_number.data,
            ethnicity=form.ethnicity.data,
            gender=form.gender.data,
            motivation=form.motivation.data,
            registration_proof_filename=registration_proof_filename,
            id_copy_filename=id_copy_filename,
            academic_results_filename=academic_results_filename,
            date_applied=datetime.today(),
            applicant=current_user,
            post=None  # Update this if you want to associate the application with a specific post
        )

        db.session.add(new_application)
        db.session.commit()

        flash('Application submitted successfully!', 'success')
        return redirect(url_for('view_applications'))  # Redirect to dashboard or another route after submission

    return render_template('apply.html', form=form)

@app.route('/view_applications')
@login_required
def view_applications():
    # Fetch applications related to the current user from the database
    applications = Application.query.filter_by(applicant=current_user).all()

    return render_template('view_applications.html', applications=applications)




@app.route('/search_results')
def search_results():
    query = request.args.get('query', '')  # Get the search query from the URL parameters

    if query:
        # Perform a search for applications based on the query
        applications = Post.query.filter(Post.title.ilike(f'%{query}%')).all()
    else:
        # If no query is provided, return to the home page
        return redirect(url_for('home'))

    return render_template('search_results.html', applications=applications, query=query)