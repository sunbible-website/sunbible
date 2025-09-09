from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    # Python variable

    with open('/static/json/gl_active_list.json') as json_file:
        data = json.load(json_file)

        # Pass the variable to the template

        return render_template('allothernav.html', menus=data)


if __name__ == '__main__':
    app.run(debug=True)