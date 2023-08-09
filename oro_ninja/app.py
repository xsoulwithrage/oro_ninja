from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Reemplaza 'your_secret_key' con una clave secreta adecuada

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'gold' not in session:
        session['gold'] = 0
        session['activities'] = []

    return render_template('index.html', activities=session['activities'], gold=session['gold'])

@app.route('/process_money', methods=['POST'])
def process_money():
    places = {
        'farm': {'min': 10, 'max': 20},
        'cave': {'min': 5, 'max': 10},
        'house': {'min': 2, 'max': 5},
        'casino': {'min': -50, 'max': 50}
    }

    building = request.form['building']
    gold_change = random.randint(places[building]['min'], places[building]['max'])

    if building == 'casino':
        gold_change *= random.choice([-1, 1])

    session['gold'] += gold_change

    activity = {
        'message': f"Earned {gold_change} gold from the {building}!",
        'color': 'green' if gold_change >= 0 else 'red'
    }

    session['activities'].insert(0, activity)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
