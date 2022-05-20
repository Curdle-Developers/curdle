
import os
from app import app, db
from app.forms import AdminLoginForm, PuzzleUploadForm
from flask import render_template, flash, redirect, request
from wtforms import ValidationError
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from app.models import Cheese, Type, Country, Animal, Continent, Admin

# Used to index a puzzle for the day, should increment by +1 every day
cheese_id_counter = 2
# Somehow increment this every day - APScheduler can help?

# Routes are written as shown below
# The decorators at the beginning (starting with @app) define what URL's the code below them is run on
# The view function contains this code

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
# A view function for the homepage
def index():
    # get cheese puzzle by ID
    # This could be randomised?

    global cheese_id_counter

    image = db.session.query(Cheese.image_filename).filter(Cheese.id == cheese_id_counter).scalar()
    # If the database query fails because the id does not exist it should return none...
    if image == None:
        # If this is the case, reset the cheese id counter to 1, starting the puzzles from the beginning again
        cheese_id_counter = 1
        image = db.session.query(Cheese.image_filename).filter(Cheese.id == cheese_id_counter).scalar()

    # Get list of cheeses from the database to be used in the game's guess selector field
    # SQLAlchemy returns this as a list of KeyedTuples for some reason, even though there is only one value stored..
    result = db.session.query(Cheese.cheese_name).all()
    
    # Iterate through results and add all cheese name values to a list
    cheeses = []
    for row in result:
        cheeses.append(row[0])

    # Render the game html template in the browser
    # Image filename and sorted list of cheeses are passed to the template renderer
    return render_template('index.html', cheeses=sorted(cheeses), image=image)

# This route below can receive GET and POST requests, required for receiving form data - Default without this set is just to receive GET requests
@app.route('/auth', methods=['GET', 'POST'])
def auth():

    # initialize new object of AdminLoginForm() class
    form = AdminLoginForm()

    # Use WTForms' FlaskForms functions to validate user input
    # The validations set in admin_login.py are checked, and if data is valid, browser is redirected to /index
    if form.validate_on_submit():

        password = request.form['password']

        # Need to start a session for user login - old method did not work
        if check_password_hash(hash, password):
            flash('Administration Portal Authentication Successful')
            return redirect('/puzzle-uploader')
        else:   
            raise ValidationError('The password you entered in incorrect')

    # Else, browser stays at /authorise view
    return render_template('auth.html', form=form)
    

@app.route('/puzzle-uploader', methods=['GET', 'POST']) 
def puzzle_uploader():
    
    #global authorised

    # Create new instance of PuzzleUploadForm()
    form = PuzzleUploadForm()

    # Retreive lists of cheese attributes from the database

    form.type.choices = db.session.query(Type.id, Type.type).all()
    form.animal.choices = db.session.query(Animal.id, Animal.animal_name).all() 
    form.country.choices = db.session.query(Animal.id, Country.country_name).all() 

    if form.validate_on_submit():
        # Here goes the code that recieves the data and handles adding it to the database
        if request.method == "POST":

            req = request.form


            f = form.image.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.instance_path, 'images', filename))
            
            print(req)

            flash('Puzzle Upload Successful')

            # return redirect(request.url)
    
    return render_template('puzzle-uploader.html', form=form)
    
@app.route('/check-guess', methods=['GET', 'POST'])
def get_guess():
    
    # Get cheese name from client side
    if request.method == "POST":

        cheese_name = request.get_json() # This returns a single entry dict containing the cheese name

        answer = Cheese.query.filter_by(id=cheese_id_counter).first()

        guess = Cheese.query.filter_by(cheese_name=cheese_name['cheese_name']).first() #cheese_name

        results = {'name': True, 'country': True, 'mould': True, 'animal': True, 'type': True, 'continent': True}

        # If the answer and guess share the same ID, the game is won (id is unique in the database)
        if (answer.id == guess.id) and (answer.cheese_name != guess.cheese_name):
                
                return results

        if (answer.country_id != guess.country_id):
            results["country"] = False

        if (answer.mouldy != guess.mouldy):
            results["mould"] = False

        if (answer.animal_id != guess.animal_id):
            results["name"] = False

        if (answer.type_id != guess.type_id):
            results["type"] = False


        guess_country = Country.query.filter_by(id=guess.country_id).first()

        answer_country = Country.query.filter_by(id=answer.country_id).first()

        if (answer_country.continent_id != guess_country.continent_id):
            results["continent"] = False
        
        return results






