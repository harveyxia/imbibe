import psycopg2
import pickle
import os
import urlparse
import sys

if len(sys.argv) < 2 or sys.argv[1] != 'localhost':
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
else:
    conn = psycopg2.connect("host=localhost user=harvey")
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
ingr_flavor = {}
ingr_type = set()
types = set()
cocktail_flavors = set()

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
            # ingr_flavor.add( (ingr_id, flavor_id) )
            if ingr_id not in ingr_flavor:
                ingr_flavor[ingr_id] = set()
            ingr_flavor[ingr_id].add(flavor_id)

# populate imbibe.cocktail
for cocktail in cocktails:
    print cocktail['id']
    cur.execute("INSERT INTO imbibe.cocktail (id, title, directions) VALUES (%s, %s, %s)",
                (int(cocktail['id']), cocktail['title'], cocktail['directions']) )
    for ingr in cocktail['ingredients']:
        ingr_id = int(ingr['id'])
        cocktail_id = int(cocktail['id'])
        # create set to dump later
        contains[(cocktail_id, ingr_id)] = ingr['q']
        # find cocktail's ingredient's flavors
        if ingr_id in ingr_flavor:
            for flavor_id in ingr_flavor[ingr_id]:
                cocktail_flavors.add( (cocktail_id, flavor_id) )

# populate imbibe.flavor
for flavor, id in flavors.iteritems():
    try:
        cur.execute("INSERT INTO imbibe.flavor (id, title) VALUES (%s, %s)",
                (id, flavor))
    except Exception, e:
        print e.pgerror

# populate imbibe.cocktail_flavors
for t in cocktail_flavors:
    cur.execute("INSERT INTO imbibe.cocktail_flavors (cocktail_id, flavor_id) VALUES (%s, %s)", t)

# populate imbibe.type
for t in types:
    cur.execute("INSERT INTO imbibe.type (id, title) VALUES (%s, %s)", t)

i = 0
# populate imbibe.contains
for k,v in contains.iteritems():
    print i
    i += 1
    cur.execute("INSERT INTO imbibe.contains (cocktail_id, ingredient_id, quantity) VALUES (%s, %s, %s)", (k[0], k[1], v))

for ingr_id, flavor_ids in ingr_flavor.iteritems():
    for flavor_id in flavor_ids:
        cur.execute("INSERT INTO imbibe.ingr_flavor (ingredient_id, flavor_id) VALUES (%s, %s)", (ingr_id, flavor_id))

for t in ingr_type:
    cur.execute("INSERT INTO imbibe.ingr_type (ingredient_id, type_id) VALUES (%s, %s)", t)

conn.commit()
cur.close()
conn.close()