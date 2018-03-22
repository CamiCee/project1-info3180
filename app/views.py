"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import SignUpForm, SendID
from models import UserProfile
from werkzeug.utils import secure_filename
import os, datetime, json, psycopg2

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

def format_date_joined():
    now=datetime.datetime.now();
    date_joined=datetime.date(now.year, now.month, now.day)
    d= "Joined " + date_joined.strftime("%B %d, %Y")
    return d
    
@app.route('/profile', methods=["GET","POST"])
def profile():
    form=SignUpForm()
    if request.method == "POST" and form.validate_on_submit():
        check = UserProfile.query.filter_by(email = form.email.data).first()
        if not check:
            img_data = form.image.data
            filename = secure_filename(img_data.filename)
            img_data.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            join=format_date_joined()
            #user = UserProfile(form.fname.data, form.lname.data, form.gender.data, form.email.data, form.location.data, form.bib.data, os.path.join(app.config['UPLOAD_FOLDER'],filename), join )
            user = UserProfile(form.fname.data, form.lname.data, form.gender.data, form.email.data, form.location.data, form.bib.data, filename, join )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('profiles'))
    return render_template("profile.html", form=form)
 
@app.route('/profiles', methods=["GET","POST"])    
def profiles():
    #d=UserProfile.query.all()
    form=SendID
    if request.method == "POST":
        flash(form.myid)
        return redirect(url_for('home'))
        #return render_template
    return render_template('profiles.html', a=getall(),d="", form=form)#d=UserProfile.query.all())
    
def getall():
    #id=userid
    conn = None
    #row=k
    #params = app.config()
    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'], sslmode='require') #**params)
    #conn = psycopg2.connect("postgresql://snwrsyweqruemh:78217000d03a8e13303e883488233b14ddaa9e1eb738cceb81b9f533d7037e07@ec2-54-243-210-70.compute-1.amazonaws.com:5432/d6skuaqkm425rb")
    cur = conn.cursor()
    cur.execute("SELECT myid,fname, lname, gender,location, image from user_profile")
    row=cur.fetchall()
    cur.close()
    '''try:
        params = app.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT fname from user_profile WHERE id = userid")
        row=cur.fetchone()
        cur.close()
        row="bbbbbb"
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)'''
    #finally:
    if conn is not None:
        conn.close()
    #row=row0
    return row
    
@app.route('/profile/<userid>', methods=["GET","POST"])
def show_user_profile(userid):
    form=""
    check= UserProfile.query.filter_by(myid = userid).first()
    if check:
        #flash(json.dumps(check))
       # d=check
        d = getperson(userid)
        return render_template("individual.html", d = getperson(userid))
        #return render_template("profiles.html", a="", d = getperson(userid))
        #return render_template("profile.html", d = getperson(userid), form=form)
        #return redirect(url_for('profiles.html', d=check))
    return render_template("profile.html",form=form)
    
def getperson(userid):
    myid=int(userid)
    
    conn = None
    #row=k
    #params = app.config()
    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI']) #**params)
    cur = conn.cursor()
    i=userid
    #cur.execute("select * from user_profile where myid::numeric=myid")
    cur.execute("select * from user_profile where myid= myid")
    row=cur.fetchall()
    cur.close()
    """if row[1][0] == myid:
        row="bat"
        return row"""
    for rows in row:
        if rows[0]==myid:
            #row="batter"
            return rows
    '''for r in row:
        if r[0] == i:
            return r'''
    #b=row[1][0]
    
    
    '''try:
        params = app.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT fname from user_profile WHERE id = userid")
        row=cur.fetchone()
        cur.close()
        row="bbbbbb"
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    #row=row0
    #row = userid'''
    #row = myid
    #row=type(userid)
    return row
    
        

'''@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        # change this to actually validate the entire form submission
        # and not just one field
        if form.username.data:
            # Get the username and password values from the form.

            # using your model, query database for a user based on the username
            # and password submitted
            # store the result of that query to a `user` variable so it can be
            # passed to the login_user() method.

            # get user id, load into session
            login_user(user)

            # remember to flash a message to the user
            return redirect(url_for("home"))  # they should be redirected to a secure-page route instead
    return render_template("login.html", form=form)'''


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
