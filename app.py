import os
from psql_client import Client
from flask import Flask, render_template, request
app = Flask(__name__)

client = Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cocktail/<id>')
def get_cocktail(id):
    cocktail = client.get_cocktail_by_id(id)
    # return render_template('cocktail.html', title=cocktail['title'], directions=cocktail['directions'])
    return render_template('cocktail.html', cocktail=cocktail)

@app.route('/search')
def get_cocktail_by_flavors():
    flavor_ids = parse_flavor_ids(request.args)
    cocktails = client.get_cocktail_by_flavors(flavor_ids)
    print cocktails
    return "hello"

def parse_flavor_ids(args):
    flavor_ids = []
    for arg in args:
        if arg[0] == 'id':
            flavor_ids.append(arg[1])
    return flavor_ids

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)