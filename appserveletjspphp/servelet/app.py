from flask import *
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Database connection info. Usually, this should be in a separate config file.
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

# Simple login form
login_form_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        form input[type=text], form input[type=password] {
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        form input[type=submit] {
            padding: 15px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        form input[type=submit]:hover {
            background-color: #0056b3;
        }
        h2 {
            text-align: center;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login</h2>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="submit" value="Login">
        </form>
    </div>
</body>
</html>

'''

@app.route('/')
def home():
    return login_form_html

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        message = "Login successful."
        color = "green"
    else:
        message = "Login failed."
        color = "red"

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Result</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f0f2f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .message-container {{
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 400px;
                text-align: center;
            }}
            .message {{
                color: {color};
                font-size: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="message-container">
            <p class="message">{message}</p>
            <a href="/">Try Again</a>
        </div>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)
