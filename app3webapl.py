from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    form_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enter Details</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            form {
                display: flex;
                flex-direction: column;
            }
            input[type="text"], input[type="number"], input[type="submit"] {
                padding: 10px;
                margin: 10px 0;
                border-radius: 4px;
                border: 1px solid #ddd;
                font-size: 16px;
            }
            input[type="submit"] {
                background-color: #007bff;
                color: white;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <form action="/" method="post">
                <input type="text" name="name" placeholder="Enter your name" required>
                <input type="number" name="age" placeholder="Enter your age" required min="1" max="100">
                <input type="submit" value="Submit">
            </form>
        </div>
    </body>
    </html>
    '''
    
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        if age < 18:
            message = f"Hello {name}, you are not authorized to visit the site."
        else:
            message = f"Welcome {name} to this site."
        
        return f'<h2 style="text-align:center; margin-top:20px;">{message}</h2>'
    
    return form_html

if __name__ == "__main__":
    app.run(debug=True)
