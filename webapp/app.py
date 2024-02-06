from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = '111'

# Database configuration
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('customize_pc'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/customize_pc')
def customize_pc():
    if 'loggedin' in session:
        return render_template('customize_pc.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/submit_pc', methods=['POST'])


# Assuming the rest of your Flask setup is here

@app.route('/submit_pc', methods=['POST'])
def submit_pc():
    if 'loggedin' in session:
        additionalSpecs = request.form.get('additionalSpecs')
        component_fields = ['processor', 'graphicsCard', 'motherboard', 'ram', 'ssd', 'hdd', 'psu', 'pcCase','additionalSpecs']
        component_details = []
        component_costs = {
                'ryzen3600': 11000, 'i510400': 12000, 'ryzen5900x': 32000, 'i910900k': 34000,'ryzen7900x': 44500,
                'rtx4090': 200000, 'rtx4070ti': 88000, '7600xt': 30000, '7800xt':50000,'6600xt':25000,
                'z790': 32000, 'b760': 25000, 'b550': 24000, 'b660': 20000,'x570':75000 ,
                'ram1': 13000, 'ram2': 10000, 'ram3': 9000, 'ram4': 12000,"ram5":11000,
                'ssd1': 20000, 'ssd2': 21000, 'ssd3': 25000, 'ssd4': 22000,'ssd5': 18000,
                'hdd1': 7000, 'hdd2': 14000, 'hdd3': 11000, 'hdd4': 5000,'hdd5':48000,
                'psu1': 10000, 'psu2': 68000, 'psu3': 5000, 'psu4': 50000,'psu5':32000,
                'case1': 38000, 'case2': 33000, 'case3': 45000, 'case4': 17000,'case5': 8000
        };
        total_cost = 0
        for field in component_fields:
            if field=='additionalSpecs':
                selection = request.form.get(field)
                component_details.append((field.capitalize(), selection, "To be informed later"))
            else:
                selection = request.form.get(field)
                if selection:
                    cost = component_costs.get(selection, 0)
                    total_cost += cost
                    # Append a tuple of (Component Name, Selection, Cost)
                    component_details.append((field.capitalize(), selection, cost))       
            # Now pass all these details to your bill display template
        return render_template('bill_display.html', username=session['username'],components=component_details, total=total_cost)

    # If the user is not logged in, redirect to login page
    return redirect(url_for('login'))


@app.route('/bill_display')
def bill_display():
    if 'loggedin' in session:
        total = request.args.get('total', type=int)
        return render_template('bill_display.html', username=session['username'], total=total)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
