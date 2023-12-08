from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'pailab'
csrf = CSRFProtect(app)
app.config['WTF_CSRF_SECRET_KEY'] = 'a-random-string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email=db.Column(db.String(20), unique=False, nullable=False)
    address= db.Column(db.String(20), unique=False, nullable=False)
    course= db.Column(db.String(20), unique=False, nullable=False)

# Route connecting User html
@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users'))

class MyForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email')
    address = StringField('Address')
    course = StringField('Course')
    submit = SubmitField('Submit')

@app.route('/forms', methods=['GET', 'POST'])
def form():
    form = MyForm()
    if form.validate_on_submit():
        # Create a new User instance and save it to the database
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            address=form.address.data,
            course=form.course.data
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Form submitted successfully!', 'success')
        return redirect(url_for('users'))  # Redirect to the users page

    return render_template('form.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # This condition ensures that the following code is only executed
    # when the script is run directly (not imported as a module).
    # It will create the database tables when the script is run.
    # Create the Flask app context
    with app.app_context():
        # Create the database tables when the script is run
        db.create_all()
        u1=User(username='Sohail', email='sohail.abbas@isb.nu.edu.pk',address='Joharabad',course='PAI')
        u2=User(username='Ammar Masood', email='ammar.masood@isb.nu.edu.pk',address='ISlamabad',course='DS')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
    app.run(debug=True)