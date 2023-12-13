import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key=True)
    innings_id = db.Column(db.Integer, nullable=False)
    over_id = db.Column(db.Integer, nullable=False)
    ball_id = db.Column(db.Integer, nullable=False)
    team_batting_id = db.Column(db.Integer, nullable=False)
    team_bowling_id = db.Column(db.Integer, nullable=False)
    striker_id = db.Column(db.Integer, nullable=False)
    striker_batting_position = db.Column(db.Integer, nullable=False)
    non_striker_id = db.Column(db.Integer, nullable=False)
    bowler_id = db.Column(db.Integer, nullable=False)
    batsman_scored = db.Column(db.Integer, nullable=False)



@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        # Retrieve data from the form
        match_id = request.form['match_id']
        innings_id = request.form['innings_id']
        over_id = request.form['over_id']
        ball_id = request.form['ball_id']
        team_batting_id = request.form['team_batting_id']
        team_bowling_id = request.form['team_bowling_id']
        striker_id = request.form['striker_id']
        striker_batting_position = request.form['striker_batting_position']
        non_striker_id = request.form['non_striker_id']
        bowler_id = request.form['bowler_id']
        batsman_scored = request.form['batsman_scored']

        # Create a new Match instance and save it to the database
        new_match = Match(
            match_id=match_id,
            innings_id=innings_id,
            over_id=over_id,
            ball_id=ball_id,
            team_batting_id=team_batting_id,
            team_bowling_id=team_bowling_id,
            striker_id=striker_id,
            striker_batting_position=striker_batting_position,
            non_striker_id=non_striker_id,
            bowler_id=bowler_id,
            batsman_scored=batsman_scored
        )

        db.session.add(new_match)
        db.session.commit()

        return redirect(url_for('view'))

    return render_template('add_record.html')


@app.route('/get_record', methods=['POST'])
def get_record():
    batsman_score = request.form.get('batsman_score')
    match = Match.query.filter_by(batsman_scored=batsman_score).first()
    return render_template('get_record.html', match=match)

@app.route('/matches')
def matches():
    # Retrieve data from the database and sort by bowler_id
    matches = Match.query.order_by(Match.bowler_id).all()
    return render_template('view.html', matches=matches)

@app.route('/matches_by_bowler', methods=['POST'])
def matches_by_bowler():
    bowler_id = request.form.get('bowler_id')
    # Retrieve data from the database filtered by the entered Bowler ID
    matches = Match.query.filter_by(bowler_id=bowler_id).all()
    return render_template('view.html', matches=matches)

@app.route('/view')
def view():
    matches = Match.query.all()
    return render_template('view.html', matches=matches)

@app.route('/')
def home():
    return render_template('home2.html')

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()# Inside the app context block where you read and insert data from CSV
        df = pd.read_csv('data.csv')
        print(f"Number of rows read from CSV: {len(df)}")
        try:
            df.to_sql('match', con=db.engine, if_exists='replace', index=False)
            print("Data insertion successful.")
        except Exception as e:
            print(f"Error during data insertion: {str(e)}")
        print("Number of rows inserted into the database:", len(Match.query.all()))


    app.run(debug=True)
