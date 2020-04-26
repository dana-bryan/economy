from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
application = app

db_name = 'final.db'



# Flask-Bootstrap requires this line
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type

class Unempl(db.Model):
    __tablename__ = 'county'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    gas = db.Column(db.Float)
    unemplfeb20 = db.Column(db.Float)
    unemplmar20 = db.Column(db.Integer)
    laborforce = db.Column(db.Integer)
    medianincome2018 = db.Column(db.Integer)
    pop = db.Column(db.Integer)
    squaremilessize = db.Column(db.Integer)
    countyseat = db.Column(db.Text)

# get sock IDs and names for the select menu BELOW
county = Unempl.query.order_by(Unempl.name).all()
# create the list of tuples needed for the choices value
pairs_list = []
for title in county:
    pairs_list.append( (title.id, title.name) )

# Every form control must be configured here
# Flask-WTF form magic
# set up the quickform - select includes value, option text (value matches db)
# all that is in this form is one select menu and one submit button
class CountySelect(FlaskForm):
    select = SelectField( 'Select a County:',
      choices=pairs_list
      )
    submit = SubmitField('Submit')

# routes
# starting page for app
@app.route('/')
def index():
    # make an instance of the WTF form class we created, above
    form = CountySelect()
    # pass it to the template
    return render_template('index.html', form=form)


# whichever id comes from the form, that one sock will be displayed
@app.route('/county', methods=['POST'])
def county_detail():
    county_id = request.form['select']
    # get all columns for the one sock with the supplied id
    the_county = Unempl.query.filter_by(id=county_id).first()
    # pass them to the template
    return render_template('unempl.html', the_county=the_county)


if __name__ == '__main__':
    app.run(debug=True)
