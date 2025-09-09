from flask import Flask, jsonify, request, url_for, redirect, session, render_template

app = Flask(__name__)
application = app

# Config stuff goes here at the top before the routes.
# The Secret Key is necessary for starting a session.
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'

# This is the "index.html" route.
@app.route('/')
def index():
    session.pop('name', None)
    return render_template('index.html')

# This is the "terms.html" route.
@app.route('/terms')
def terms():
    session.pop('name', None)
    return render_template('terms-conditions.html')

# This is the "index.html" route.
@app.route('/privacy')
def privacy():
    session.pop('name', None)
    return render_template('privacy-policy.html') 

# GET is the default method if nothing is specified. 
# Notice that a session name variable gets set in this route.
# (leaving this old example code here in case it helps... it shows
# methods, defaults, and passing arguments for render_template)

@app.route('/home', methods=['POST', 'GET'], defaults={'name' : 'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return render_template('home.html', name=name, display=False) # , mylist=['one', 'two', 'three', 'four'], listofdictionaries=[{'name' : 'Zach'}, {'name' : 'Zoe'}])

if __name__ == '__main__':
    app.run()