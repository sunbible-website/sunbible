from flask import Flask, jsonify, request, url_for, redirect, session, render_template
import json
from html import escape
import os.path
from datetime import datetime
import sys
import time



app = Flask(__name__, static_folder="../public_html/static", template_folder="templates")
application = app

# Config stuff goes here at the top before the routes.
# The Secret Key is necessary for starting a session.
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'

TEMPLATES_AUTO_RELOAD = True

with open('./json/gl_active_list.json') as file:
    menu_data = json.load(file)
    
with open('./json/SUN_BIBLE_page_list.json') as file:
    menu_data1 = json.load(file)    

# This is the "index.html" route.
@app.route('/')
def index():
    #with open('./json/gl_active_list.json') as file:
       #menu_data = json.load(file)
    session.pop('name', None)
    return render_template('index.html', title='SUN Translation Resources', navindex=True, json_data = menu_data, json_data1 = menu_data1 )
    
# This is the "where-page.html" route.
@app.route('/where')
def where():
    #with open('./json/gl_active_list.json') as file:
      #menu_data = json.load(file)
    session.pop('name', None)
    return render_template('where-org.html', title='projects', json_data = menu_data, json_data1 = menu_data1 )
    
# This is the "contact-teach.html" route.
@app.route('/contact')
def contact():
    session.pop('name', None)
    return render_template('contact-teach.html', title='Contact Us')
    
# This is the "contact-translator.html" route.
@app.route('/contactus')
def contactus():
    session.pop('name', None)
    return render_template('contact-translator.html', title='Contact Us')

# This is the "terms.html" route.
@app.route('/terms')
def terms():
    #with open('./json/gl_active_list.json') as file:
      #menu_data = json.load(file)
    session.pop('name', None)
    return render_template('terms-conditions.html', title='Terms and Conditions', json_data = menu_data, json_data1 = menu_data1 )


# This is the "privacy.html" route.
@app.route('/privacy')
def privacy():
    #with open('./json/gl_active_list.json') as file:
      #menu_data = json.load(file)
    session.pop('name', None)
    return render_template('privacy-policy.html', title='Privacy Policy', json_data = menu_data, json_data1 = menu_data1 )


# This is the "status.html" route.
@app.route('/status')
def status():
    session.pop('name', None)
    with open('./json/lang_status.json','r') as file:
      table_data = file.read()
    html_table = json_to_html_table(table_data)
    session.pop('name', None)
    return render_template('status.html', title='Translation Status', html_table=html_table, json_data = menu_data, json_data1 = menu_data1 )

# create HTML table.
def json_to_html_table(table_data):
    data = json.loads(table_data)

    # Create HTML table header
    table_html = "<table border='5'><tr>"
    for key in data[0].keys():
        table_html += f"<th>{escape(key)}</th>"
    table_html += "</tr>"

    # Create HTML table rows
    for item in data:
        table_html += "<tr>"
        for value in item.values():
            table_html += f"<td>{escape(str(value))}</td>"
        table_html += "</tr>"

    # Close HTML table
    table_html += "</table>"

    return table_html
    
@app.route('/process', methods=['POST'])
def process_data():
    session.pop('name', None)
    selected_option = request.form.get('selected_option')
    return f'The selected option is: {selected_option}'    
    
# This is the "partners.html" route.
@app.route('/partners')
def partners():
    session.pop('name', None)
    with open('./json/web_partner_list.json','r') as file:
     table_data = file.read()
    html_table = json_to_html_table(table_data)
    session.pop('name', None)
    return render_template('partners.html', title='partners',html_table=html_table, json_data = menu_data, json_data1 = menu_data1 )

# This is the "resource-page.html" route.
@app.route('/resource/<code>', methods=["GET", "POST"])
def resource_page(code):
    session.pop('name', None)
    json_data = read_json_file(code)
    html_content = generate_html_from_json(json_data)
    session.pop('name', None)
    return render_template('resource.html', title='Resource Files', html_content=html_content, code=code, json_data = menu_data, json_data1 = menu_data1 )
    
def read_json_file(received_code):
    file_name = f"./json/{received_code}-page.json"

    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None
        
# This is the "sun-page.html" route.
@app.route('/sun/<code>', methods=["GET", "POST"])
def sun_page(code):
    session.pop('name', None)
    json_data1 = read_json_file1(code)
    html_content = generate_html_from_json1(json_data1)
    session.pop('name', None)
    return render_template('sun.html', title='Sun Files', html_content=html_content,code=code, json_data = menu_data, json_data1 = menu_data1 )
    
def read_json_file1(received_code):
    file_name = f"./json/{received_code}-page.json"

    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None    
        
# This is the "ENG-page.html" route.
@app.route('/ENG')
def ENG():
    session.pop('name', None)
    return render_template('ENG-page.html', title='ENG Resource Files')

# This is the "Testy-page.html" route.
@app.route('/TESTY')
def TESTY():
    session.pop('name', None)
    return render_template('testy-page.html', title='TESTY Resource Files')


# This is the "PORB-page.html" route.
@app.route('/PORB')
def PORB():
    session.pop('name', None)
    return render_template('PORB-page.html', title='PORB Resource Files')


# This is the "Bible-page.html" route.
@app.route('/Bible')
def Bible():
    with open('./json/gl_active_list.json') as file:
     json_data = json.load(file)
    session.pop('name', None)
    return render_template('Bible-page.html', title='SUN Translation Resources', json_data=json_data)
   # return render_template('Bible-page.html', title="SUN Bible Files")
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def generate_html_from_json(html_data):
    # Customize this function based on your JSON structure and HTML template
    # For simplicity, it assumes a basic structure with links to download PDF files
    html_content = ""
    for entry in html_data:
        file_name = entry['File Label']
        download_file = entry['Download File Name']
        target_url = url_for('static', filename='resource/' + download_file)
        download_link = target_url
        target_directory = '/home/suntrans/public_html/static/resource/'
        target_path = os.path.join(target_directory, download_file)
        if os.path.exists(target_path):
            last_modified_timestamp = os.path.getmtime(target_path)
            last_modified_date = datetime.fromtimestamp(last_modified_timestamp).date()
            last_modified_date_str = last_modified_date.strftime('%Y-%m-%d')
        else:
            last_modified_date_str = "Coming soon"
        html_content += f"        <li><i class='fas fa-square'></i><a href='{download_link}' target='_blank'>{file_name}</a> - {last_modified_date_str}</li>\n"
    return html_content
    
def generate_html_from_json1(html_data):
    # Customize this function based on your JSON structure and HTML template
    # For simplicity, it assumes a basic structure with links to download PDF files
    html_content = ""
    for entry in html_data:
        file_name = entry['File Label']
        download_file = entry['Download File Name']
        target_url = url_for('static', filename='bible/' + download_file)
        download_link = target_url
        target_directory = '/home/suntrans/public_html/static/bible/'
        target_path = os.path.join(target_directory, download_file)
        if os.path.exists(target_path):
            last_modified_timestamp = os.path.getmtime(target_path)
            last_modified_date = datetime.fromtimestamp(last_modified_timestamp).date()
            last_modified_date_str = last_modified_date.strftime('%Y-%m-%d')
        else:
            last_modified_date_str = "Coming soon"
        html_content += f"        <li><i class='fas fa-square'></i><a href='{download_link}' target='_blank'>{file_name}</a> - {last_modified_date_str}</li>\n"
    return html_content    

# GET is the default method if nothing is specified.
# Notice that a session name variable gets set in this route.
# (leaving this old example code here in case it helps... it shows
# methods, defaults, and passing arguments for render_template)

# @app.route('/home', methods=['POST', 'GET'], defaults={'name' : 'Default'})
# @app.route('/home/<string:name>', methods=['POST', 'GET'])
# def home(name):
# session['name'] = name
# return render_template('home.html', name=name, display=False) # , mylist=['one', 'two', 'three', 'four'], listofdictionaries=[{'name' : 'Zach'}, {'name' : 'Zoe'}])

if __name__ == '__main__':
    app.run()
