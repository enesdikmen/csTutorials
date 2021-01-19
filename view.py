from flask import render_template, request, url_for, redirect, flash, current_app, abort
from user_forms import SignUpForm, LoginForm, User, EditAccountForm
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import login_user, current_user, logout_user, login_required
from db import db
from tables import Topic, Educator, Tutorial



def main():
    tutorials = db.get_tutorials()
    rows = db.get_topic_names()
    
    return render_template('home.html', topics=sorted(rows), tutorials = tutorials)

def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    
    form = SignUpForm()
    if form.validate_on_submit():
        hashed = hasher.hash(form.password.data)
        userID = db.add_user(form.email.data, hashed)
        if userID:
            user = User(userID, form.email.data, form.password.data)
            login_user(user)
            flash(f"Account created for {form.email.data}", "is-success")
            return redirect(url_for('main'))
        else:
            flash(f"An account for {form.email.data} already exists", "is-danger")    

    return render_template('sign_up.html', form=form)

def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        if db.validate_login(form.email.data, form.password.data):
            userID = db.get_userID(form.email.data)
            user = User(userID, form.email.data, form.password.data)
            flash(f"Logged in as {form.email.data}", "is-success")
            login_user(user, remember=False)
            return redirect(request.args.get('next')) if request.args.get('next') else redirect(url_for('main'))
        else:
            flash('Login unsuccesfull. Please check username and password.', "is-danger")
            return redirect(url_for('login'))
    message = request.args.get('message')
    if message:
            flash(message, "is-info")

    return render_template('login.html', form=form)


def logout():
    logout_user()
    return redirect(url_for('main'))

@login_required
def account():
    user = db.get_user(current_user.id)      
    enrollments = db.get_enrollments_of(current_user.id)
    return render_template('account.html', enrollments = enrollments, user=user)

@login_required
def add_tutorial():

    if request.method == "POST":
        tutorialTitle = request.form["tutorialTitle"]
        tutorialTopic = request.form["tutorialTopic"]
        tutorialSkill = request.form["tutorialSkill"]
        tutorialPlatform = request.form["tutorialPlatform"]
        hours = request.form["hours"]
        minutes = request.form["minutes"]
        tutorialURL = request.form["tutorialURL"]
        tutorialInfo = request.form["tutorialInfo"]
        educatorID = request.form["educatorID"]
        lenght = []
        lenght.append(int(hours))
        lenght.append(int(minutes))

        tutorial = Tutorial(tutorialTitle, educatorID, tutorialPlatform, tutorialURL, tutorialSkill, lenght, tutorialInfo)
        tutorialid = db.add_tutorial(tutorial) 
        if tutorialid:
            db.assign_topic(tutorialid, tutorialTopic)
            flash(f"Tutorial '{tutorialTitle}' added", "is-success")
        return redirect(url_for('edit_tutorial', tutorialid=tutorialid))
    else:
        topics = db.get_topics()
        educators = db.get_educator_names()
        return render_template('add_tutorial.html', topics = sorted(topics, key=lambda row: row[1]), educators = sorted(educators))

@login_required
def delete_tutorial():
    tutorialid = request.args.get('tutorialid')
    if db.remove_tutorial(tutorialid):
        db.refresh_alleducatorrating()
        flash(f"Tutorial deleted", "is-success")


    return redirect(url_for('main'))

def tutorial():
    tutorialid = request.args.get('tutorialid')
    if tutorialid == None:
        return redirect(url_for('main'))
    ratings = db.get_tutorial_ratings(tutorialid)
    editcomment = request.args.get('editcomment')
    tutorial = db.get_tutorial(tutorialid)
    topics = db.get_tutorialTopics(tutorialid)
    return render_template('tutorial.html', tutorialid = tutorialid, tutorial = tutorial, ratings = ratings, editcomment = editcomment, topics=topics, db = db) 

def tutorials():
    if request.method == "GET":
        topics = db.get_topics()
    
        tutorials = db.get_tutorials()

        return render_template('tutorials.html', topics = sorted(topics, key=lambda row: row[1]), tutorials = tutorials)
    else:
        topics = db.get_topics()

        skill = request.form["skill"]
        platform = request.form["platform"]
        sortby = request.form["sortby"]
        topicid = request.form["topic"]
        tutorials =db.get_tutorials_filtered(sortby, skill, platform, topicid)
        
        return render_template('tutorials.html', topics = sorted(topics, key=lambda row: row[1]), topicid = int(topicid), tutorials = tutorials, skill = skill, platform = platform, sortby = sortby)
   

@login_required
def edit_tutorial():
    if request.method == 'POST':
        tutorialTitle = request.form["tutorialTitle"]
        #tutorialTopic = request.form["tutorialTopic"]
        tutorialSkill = request.form["tutorialSkill"]
        tutorialPlatform = request.form["tutorialPlatform"]
        hours = request.form["hours"]
        minutes = request.form["minutes"]
        tutorialURL = request.form["tutorialURL"]
        tutorialInfo = request.form["tutorialInfo"]
        educatorID = request.form["educatorID"]
        lenght = []
        lenght.append(int(hours))
        lenght.append(int(minutes))
        tutorialid = request.form["tutorialid"]
        tut_topics = request.form.getlist('topics_check')
        print("asd", tut_topics)
        db.set_topics(tutorialid, tut_topics)
        tutorial = Tutorial(tutorialTitle, educatorID, tutorialPlatform, tutorialURL, tutorialSkill, lenght, tutorialInfo)
        if db.update_tutorial(tutorialid, tutorial):
            flash(f"Tutorial '{tutorialTitle}' edited", "is-success")

        return redirect(url_for('edit_tutorial', tutorialid = tutorialid))
    else:
        tutorialid = request.args.get('tutorialid')
        tutorial = db.get_tutorial(tutorialid)
        topics_with = db.get_topics_with(tutorialid)
        return render_template('edit_tutorial.html', tutorialid = tutorialid, tutorial = tutorial, educators = db.get_educator_names(), topics=sorted(topics_with, key=lambda row: row[1]))

@login_required
def add_topic():
    if request.method == "POST":
        topicName = request.form["topicName"]
        
        if db.add_topic(Topic(topicName)):
            flash(f"Topic '{topicName}' added", "is-success")
        else:
            flash(f"Topic '{topicName}' already exists", "is-danger")
        return redirect(url_for('add_topic')) #later will change        
    else:
        if not current_user.is_admin():
            abort(401)
 
        topics = db.get_topics()
        return render_template('add_topic.html', topics=sorted(topics, key=lambda row: row[1]), to_edit = request.args.get('to_edit') )

@login_required
def edit_topic():
    topicName = request.form["topicName"]
    topicID = request.form['topicID']
    
    if db.update_topic(topicName, topicID):
            flash(f"Topic edited", "is-success")
    return redirect(url_for('add_topic'))

@login_required
def delete_topic():
    form_topics = request.form.getlist('topics_check')
    for topicName in form_topics:
        if db.delete_topic(topicName):        
            flash(f"Topic '{topicName}' deleted", "is-success")
        
    return redirect(url_for('add_topic'))

@login_required
def add_educator():#educatorRarting will be determined at another place
    
    if request.method == "POST":
        educatorName = request.form["educatorName"]
        educatorURL = request.form["educatorURL"]

        if db.add_educator(Educator(name=educatorName, infoURL=educatorURL)): 
            flash(f"Educator '{educatorName}' added", "is-success")
        next_page = request.args.get('next') 
        return redirect(next_page) if next_page else  redirect(url_for('add_educator'))  
    else:
        educators = db.get_educator_names()
        return render_template('add_educator.html', educators=sorted(educators))

@login_required
def delete_educator():
    educatorID = request.args.get('educatorID')
    educatorName = request.args.get('educatorName')
    if not db.educator_rmvalid(educatorID):
        if db.delete_educator(educatorID):
            flash(f"Educator '{educatorName}' deleted", "is-success")
    else:
        flash(f"Educator '{educatorName}' can't be deleted. Remove it's tutorials first.", "is-danger")
        
    return redirect(url_for('add_educator'))

@login_required
def edit_educator():
    educatorName = request.form["educatorName"]
    educatorURL = request.form["educatorURL"]
    educatorID = request.form["educatorID"]
    if db.update_educator(educatorID, educatorName, educatorURL):
            flash(f"Educator '{educatorName}' edited", "is-success")
    return redirect(url_for('educator', educatorName=educatorName)) 

def educator():
    educatorName = request.args.get('educatorName')
    edit = request.args.get('edit')
    educator = db.get_educator(educatorName)

    return render_template('educator.html', educator=educator, edit=edit)

@login_required
def enroll():
    tutorialid = request.args.get('tutorialid')
    if current_user.is_authenticated:
        if db.add_enrollment(current_user.id, tutorialid):
            flash(f"Enrolled", "is-success")  
        return redirect(url_for('account')) 

@login_required
def remove_enrollment():
    enrollmentid = request.args.get('enrollmentid')
    userid = request.args.get('userid')
    title = request.args.get('tite')

    if enrollmentid:
        
        if db.remove_enrollment(enrollmentid):
            db.refresh_enrollmentnum(userid)
            flash(f"Tutorial {title} is dropped.", "is-success")


    return redirect(url_for('account'))

@login_required
def add_comment():
    userid = request.form["userid"]
    tutorialid = request.form["tutorialid"]
    educatorid = request.form["educatorid"]
    rating = request.form["rating"]
    comment = request.form["comment"]
    if db.add_rating(userid, tutorialid, rating, comment):
        db.refresh_tutorialRating(tutorialid)
        db.refresh_educatorrating(educatorid)
        flash(f"Rating saved", "is-success")

    return redirect(url_for('tutorial', tutorialid=tutorialid))

@login_required
def edit_comment():
    ratingid = request.form["ratingid"]
    rating = request.form["rating"]
    comment = request.form["comment"]
    tutorialid = request.form["tutorialid"]
    educatorid = request.form["educatorid"]
    
    if db.update_rating(ratingid, rating, comment):
            db.refresh_tutorialRating(tutorialid)
            db.refresh_educatorrating(educatorid)
            flash(f"Rating updated", "is-success")
    return redirect(url_for('tutorial', tutorialid = tutorialid))

@login_required
def delete_comment():
    ratingid = request.args.get('ratingid')
    tutorialid = request.args.get('tutorialid')
    educatorid = request.args.get('educatorid')
    print(educatorid)
    if db.delete_comment(ratingid):
            db.refresh_tutorialRating(tutorialid)

            db.refresh_educatorrating(educatorid)
            flash(f"Rating deleted", "is-success")
    return redirect(url_for('tutorial', tutorialid = tutorialid))
    
@login_required
def delete_user():
    userid = request.args.get('userid')
    useremail = request.args.get('useremail')
    if db.delete_user(userid):
        db.refresh_allratings()
        db.refresh_alleducatorrating()
        flash(f"Account for {useremail} is deleted.", "is-success")
    return redirect(url_for('main'))

@login_required
def edit_account():
    form = EditAccountForm()
    if form.validate_on_submit():
        new_email = form.email.data
        current_password = form.current_password.data

        validation = db.validate_edituser(new_email, current_user.email, current_password)
        if validation == True:
            new_password = form.password.data 
            hashed = hasher.hash(new_password)
            if db.update_user(current_user.id, new_email, hashed):
                flash(f"Account information updated.", "is-success")
            return redirect(url_for('account'))
        elif validation == -1:
            flash('Incorrect user password. Please Try again.', "is-danger")

        else:
            flash('This email is already in use.', "is-danger")


        
    return render_template('edit_account.html', form=form)  