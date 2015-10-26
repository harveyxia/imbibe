import psycopg2
import pickle

conn = psycopg2.connect("host=lab.zoo.cs.yale.edu user=hx52 password=whispering")
cur = conn.cursor()

f1 = open("cocktails.pickle", "rb")
f2 = open("ingredients.pickle", "rb")
cocktails = pickle.load(f1)
ingredients = pickle.load(f2)
f1.close()
f2.close()

flavors = set()
contains = set()

# 1. add all cocktails
# 2. add all ingredients
# 3. add all contains

for cocktail in cocktails:
    for ingr in cocktail['ingredients']:
        # create set to dump later
        contains.add((int(cocktail['id']), int(ingr['id']), ingr['q']))
        # cur.execute("INSERT INTO imbibe.contains (cocktail_id, ingredient_id, quantity) VALUES (%s, %s, %s)",
        #     (int(cocktail['id']), int(ingr['id']), ingr['q']) )