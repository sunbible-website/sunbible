from flask import Flask, request, url_for, session, render_template
import json, os
from html import escape
from datetime import datetime

app = Flask(__name__, static_folder="../public_html/static", template_folder="templates")
application = app

app.config.update(
    DEBUG=True,
    SECRET_KEY='Thisisasecret!',
    TEMPLATES_AUTO_RELOAD=True
)

with open('./json/gl_active_list.json') as f:
    nav_menu = json.load(f)
with open('./json/SUN_BIBLE_page_list.json') as f:
    sun_menu = json.load(f)


def read_json(path):
    """
    Read the passed in JSON file.

    Returns:
        Object: The contents from the passed in JSON file.
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def json_to_html_table(table_data):
    """
    Converts a JSON object, represented as a list of key:value pairs, as an HTML table.

    Returns:
        HTML markup table
    """
    data = json.loads(table_data)
    header = ''.join(f"<th>{escape(k)}</th>" for k in data[0].keys())
    rows = ''.join(
        "<tr>" + ''.join(f"<td>{escape(str(v))}</td>" for v in item.values()) + "</tr>"
        for item in data
    )
    return f"<table border='5'><tr>{header}</tr>{rows}</table>"


def generate_html_list(items, subfolder):
    """
    Generates an HTML unordered list of downlaodable files.

    Args:
        items (list): List of downloadable files.
        subfolder (str): Subfolder within the '/home/suntrans/public_html/static/' directory. 

    Returns:
        HTML markup for the list of download links.
    """
    html = ""
    for entry in items:
        label, filename = entry['File Label'], entry['Download File Name']
        target_path = f"/home/suntrans/public_html/static/{subfolder}/{filename}"
        link = url_for('static', filename=f"{subfolder}/{filename}")
        if os.path.exists(target_path):
            date = datetime.fromtimestamp(os.path.getmtime(target_path)).strftime('%Y-%m-%d')
        else:
            date = "Coming soon"
        html += f"<li><i class='fas fa-square'></i><a href='{link}' target='_blank'>{label}</a> - {date}</li>\n"
    return html


def render_page(template, title, **kwargs):
    """
    Helper function for flask's render_template function. 
    Injects the shared navigation menu and the sun navigation menu into render_template.
    
    Args:
        template (str): Template file name (e.g. 'Index.html')
        title (str): Page title

    Returns:
        Response: Rendered HTML response for the specific template.
    """
    return render_template(template, title=title, json_data=nav_menu, json_data1=sun_menu, **kwargs)


@app.before_request
def clear_name_session():
    """
    Clear the section key 'name' before every page request.
    """
    session.pop('name', None)


@app.route('/')
@app.route('/home')
def index():
    """
    URL handler for the website 'index.html' home page.
    """
    return render_page('index.html', 'SUN Translation Resources', navindex=True)

@app.route('/where')
def where():
    """
    URL handler for the website 'where-org.html' page.
    """
    return render_page('where-org.html', 'Projects')

@app.route('/contact')
def contact():
    """
    URL handler for the website 'contact-teach.html' page.
    """
    return render_template('contact-teach.html', title='Contact Us')

@app.route('/contactus')
def contactus():
    """
    URL handler for the website 'contact-translator.html' page.
    """
    return render_template('contact-translator.html', title='Contact Us')

@app.route('/terms')
def terms():
    """
    URL handler for the website 'terms-conditions.html' page.
    """
    return render_page('terms-conditions.html', 'Terms and Conditions')

@app.route('/privacy')
def privacy():
    """
    URL handler for the website 'privacy-policy.html' page.
    """
    return render_page('privacy-policy.html', 'Privacy Policy')

@app.route('/status')
def status():
    """
    URL handler for the website 'status.html' page.
    The contents of the status table will be read from 'lang_status.json' file
    found in the json folder.
    """
    with open('./json/lang_status.json') as f:
        html_table = json_to_html_table(f.read())
    return render_page('status.html', 'Translation Status', html_table=html_table)

@app.route('/partners')
def partners():
    """
    URL handler for the website 'partners.html' page.
    The contents of the status table will be read from 'web_partner_list.json' file
    found in the json folder.
    """
    with open('./json/web_partner_list.json') as f:
        html_table = json_to_html_table(f.read())
    return render_page('partners.html', 'Partners', html_table=html_table)

@app.route('/resource/<code>')
def resource_page(code):
    """
    Handles pages for downloadable resource files.

    Loads a JSON file named '<code>-page.json' from the 'json' folder, then
    builds a list of resource links with file names in the specific language.

    Args:
        code (str): The resource code specifying the langauge (e.g. "ENG", "PORB").

    Returns:
        Rendered HTML page showing available learning resource files.
    """
    data = read_json(f'./json/{code}-page.json')
    html_content = generate_html_list(data, 'resource') if data else 'No data available.'
    return render_page('resource.html', 'Resource Files', html_content=html_content, code=code)

@app.route('/sun/<code>')
def sun_page(code):
    """
    Handles pages for downloadable Bible books.

    Loads a JSON file named '<code>-page.json' from the 'json' folder, then
    builds a list of Bible files in the specific language.

    Args:
        code (str): The resource code specifying the langauge (e.g. "ENG", "PORB").

    Returns:
        Rendered HTML page showing available Bible books for downlaod.
    """
    data = read_json(f'./json/{code}-page.json')
    html_content = generate_html_list(data, 'bible') if data else 'No data available.'
    return render_page('sun.html', 'Sun Files', html_content=html_content, code=code)

@app.route('/Bible')
def Bible():
    """
    URL handler for the website 'Bible-page.html' page.
    The contents of the status table will be read from 'gl_active_list.json' file
    found in the json folder.
    """
    with open('./json/gl_active_list.json') as f:
        json_data = json.load(f)
    return render_template('Bible-page.html', title='SUN Translation Resources', json_data=json_data)

@app.errorhandler(404)
def not_found(e):
    """
    Error handler for missing pages. 

    Returns:
        Response: Custom '404.html' page and HTTP 404 status.
    """
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
