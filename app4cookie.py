from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'cookie_name' in request.form and 'cookie_value' in request.form:
        resp = make_response(render_template_string(home_html))
        resp.set_cookie(request.form['cookie_name'], request.form['cookie_value'])
        return resp
    
    return render_template_string(home_html)

@app.route('/list-cookies')
def list_cookies():
    cookies = request.cookies
    cookie_list = '<ul>' + ''.join([f'<li>{name}: {value}</li>' for name, value in cookies.items()]) + '</ul>'
    return render_template_string(list_cookies_html, cookies=cookie_list)

home_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Cookie Manager</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; margin: 40px; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h2 { text-align: center; }
        form { display: flex; flex-direction: column; }
        input, button { margin: 10px 0; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { background-color: #007bff; color: white; cursor: pointer; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Add a Cookie</h2>
        <form method="POST">
            <input type="text" name="cookie_name" placeholder="Cookie Name" required>
            <input type="text" name="cookie_value" placeholder="Cookie Value" required>
            <button type="submit">Add Cookie</button>
        </form>
        <form action="/list-cookies" method="get">
            <button type="submit">List Cookies</button>
        </form>
    </div>
</body>
</html>
'''

list_cookies_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>List of Cookies</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; margin: 40px; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h2 { text-align: center; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Cookies Stored</h2>
        {{ cookies|safe }}
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
