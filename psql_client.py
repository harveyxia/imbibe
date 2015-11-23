import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

class Client(object):

    def __init__(self):
        # urlparse.uses_netloc.append("postgres")
        # url = urlparse.urlparse(os.environ["DATABASE_URL"])
        # conn = psycopg2.connect(
        #     database=url.path[1:],
        #     user=url.username,
        #     password=url.password,
        #     host=url.hostname,
        #     port=url.port
        # )
        # cur = conn.cursor()
        self.conn = psycopg2.connect("host=localhost user=harvey")
        self.cur = self.conn.cursor()

    def get_cocktail_by_id(self, id):
        colnames = ('id', 'title', 'directions')
        q = "SELECT * FROM imbibe.cocktail WHERE id=%s;" % id
        self.cur.execute(q)
        cocktail = dict(zip(colnames, self.cur.fetchone()))
        cocktail['ingredients'] = self.get_cocktail_ingredients_by_cocktail_id(id)
        return cocktail

    def get_cocktail_ingredients_by_cocktail_id(self, cocktail_id):
        colnames = ('cocktail_id', 'ingredient_id', 'quantity', 'id', 'title', 'description')
        q = "SELECT * FROM imbibe.contains JOIN imbibe.ingredient ON ingredient_id=id WHERE cocktail_id=%s;" % cocktail_id
        self.cur.execute(q)
        return [dict(zip(colnames, result)) for result in self.cur.fetchall()]

    def get_cocktail_by_flavors(self, flavors):
        q = "WITH t AS (SELECT * FROM imbibe.cocktail_flavors) SELECT cocktail_id FROM imbibe.cocktail_flavors"
        if len(flavors) > 0:
            q += " WHERE flavor_id=%s" % flavors[0]
        for flavor in flavors[1:]:
            q += " AND (cocktail_id, %s) IN (SELECT * FROM t)" % flavor
        q += ";"
        self.cur.execute(q)
        return self.cur.fetchall()

    def get_most_used_flavors(self):
        q = "select id, title, count from (select flavor_id, count(cocktail_id) from imbibe.cocktail_flavors group by flavor_id order by count(cocktail_id) desc) as t join imbibe.flavor on t.flavor_id=imbibe.flavor.id order by count desc;"
        return self.cur.execute(q).fetchall()
