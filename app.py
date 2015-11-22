import os
import random
from psql_client import Client
from flask import Flask, render_template, request
app = Flask(__name__)

client = Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cocktail/<id>')
def get_cocktail(id):
    return render_template('cocktail.html', cocktail=client.get_cocktail_by_id(id))

@app.route('/search')
def get_cocktail_by_flavors():
    flavor_ids = [int(id) for id in request.args.getlist('id')]
    cocktails = client.get_cocktail_by_flavors(flavor_ids)
    if len(cocktails) < 1:
        return render_template('none.html')
    else:
        cocktail = random.choice(cocktails)[0]
        return render_template('cocktail.html', cocktail=client.get_cocktail_by_id(cocktail))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
