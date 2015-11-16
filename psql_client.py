import psycopg2
import urlparse

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
        return dict(zip(colnames, self.cur.fetchone()))

    def get_cocktail_by_flavors(self, flavors):
        q = "WITH t AS (SELECT * FROM imbibe.cocktail_flavors) SELECT cocktail_id FROM imbibe.cocktail_flavors"
        if len(flavors) > 0:
            q += " WHERE flavor_id=%s" % flavors[0]
        for flavor in flavors[1:]:
            q += " AND (cocktail_id, %s) IN (SELECT * FROM t)" % flavor
        q += ";"
        self.cur.execute(q)
        return self.cur.fetchall()

# select cocktail_id from imbibe.cocktail_flavors where flavor_id=2 and (cocktail_id, 3) in (select * from imbibe.cocktail_flavors) and (cocktail_id, 11) in (select * from imbibe.cocktail_flavors) and (cocktail_id, 9) in (select * from imbibe.cocktail_flavors);

# with t as (select * from imbibe.cocktail_flavors)
# select cocktail_id from imbibe.cocktail_flavors
#   where flavor_id=2
#   and (cocktail_id, 3) in (select * from t)
#   and (cocktail_id, 11) in (select * from t)
#   and (cocktail_id, 9) in (select * from t);