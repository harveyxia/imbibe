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

flavor_count = 1
flavors = {}
contains = {}
ingr_flavor = set()
ingr_type = set()
types = set()

# 1. add all cocktails
# 2. add all ingredients
# 3. add all contains

# populate imbibe.cocktail
for cocktail in cocktails:
    print cocktail['id']
    cur.execute("INSERT INTO imbibe.cocktail (id, title, directions) VALUES (%s, %s, %s)",
                (int(cocktail['id']), cocktail['title'], cocktail['directions']) )
    for ingr in cocktail['ingredients']:
        # create set to dump later
        contains[(int(cocktail['id']), int(ingr['id']))] = ingr['q']
        # cur.execute("INSERT INTO imbibe.contains (cocktail_id, ingredient_id, quantity) VALUES (%s, %s, %s)",
        #     (int(cocktail['id']), int(ingr['id']), ingr['q']) )

# populate imbibe.ingredient
for ingr in ingredients:
    print ingr['id']
    ingr_id = int(ingr['id'])
    type_id = int(ingr['type_id'])
    cur.execute("INSERT INTO imbibe.ingredient (id, title, description) VALUES (%s, %s, %s)",
                (ingr_id, ingr['title'], ingr['description']) )
    ingr_type.add( (ingr_id, type_id) )
    types.add( (type_id, ingr['type_name']) )
    if 'flavor' in ingr:
        for flavor in ingr['flavor']:
            if flavor not in flavors:
                flavor_id = flavor_count
                flavors[flavor] = flavor_count
                flavor_count += 1
            else:
                flavor_id = flavors[flavor]
            ingr_flavor.add( (ingr_id, flavor_id) )

# populate imbibe.type
for t in types:
    cur.execute("INSERT INTO imbibe.type (id, title) VALUES (%s, %s)", t)

# populate imbibe.contains
for k,v in contains.iteritems():
    cur.execute("INSERT INTO imbibe.contains (cocktail_id, ingredient_id, quantity) VALUES (%s, %s, %s)", (k[0], k[1], v))

# populate imbibe.flavor
for flavor, id in flavors.iteritems():
    try:
        cur.execute("INSERT INTO imbibe.flavor (id, title) VALUES (%s, %s)",
                (id, flavor))
    except Exception, e:
        print e.pgerror

for t in ingr_flavor:
    cur.execute("INSERT INTO imbibe.ingr_flavor (ingredient_id, flavor_id) VALUES (%s, %s)", t)

for t in ingr_type:
    cur.execute("INSERT INTO imbibe.ingr_type (ingredient_id, type_id) VALUES (%s, %s)", t)

conn.commit()
cur.close()
conn.close()