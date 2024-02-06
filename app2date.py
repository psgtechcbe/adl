from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def show_datetime():
    # Get the current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # HTML template as a string with embedded CSS for styling
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Current Date and Time</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                margin: 40px;
                background-color: #f0f2f5;
                color: #333;
            }
            h1 {
                color: #007bff;
            }
            .datetime {
                background-color: #fff;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 5px;
                display: inline-block;
                margin: 20px;
            }
            footer {
                margin-top: 20px;
                font-size: 0.8em;
                color: #666;
            }
        </style>
    </head>
    <body>
        <h1>Current Date and Time</h1>
        <div class="datetime">{{ datetime }}</div>
    </body>
    </html>
    '''
    # Render the template with the current date and time
    return render_template_string(html_template, datetime=current_datetime)

if __name__ == '__main__':
    app.run(debug=True)
