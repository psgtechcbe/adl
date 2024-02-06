from flask import *

from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return redirect(url_for('greet'))
    return render_template('index1.html')

@app.route('/greet')
def greet():
    name = session.get('name', 'Guest')
    start_time = session.get('start_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return render_template('index2.html', name=name, start_time=start_time)

@app.route('/logout', methods=['POST'])
def logout():
    name = session.pop('name', 'Guest')
    start_time = session.pop('start_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    end_time = datetime.now()
    duration = end_time - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    return render_template('index3.html', name=name, duration=duration)

if __name__ == '__main__':
    app.run(debug=True)
