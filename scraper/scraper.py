import urllib2
import logging
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

logging.basicConfig(filename='exceptions.log',level=logging.ERROR)


class Scraper(object):
    RECIPE_ENDPOINT = "http://www.cocktaildb.com/recipe_detail?id="
    INGR_ENDPOINT = "http://www.cocktaildb.com/ingr_detail?id="
    LAST_RECIPE_INDEX = 4758
    LAST_INGREDIENT_INDEX = 631

    def scrape_cocktails(self):
        # scrape all recipes
        def task(start, end):
            recipes = []
            for id in xrange(start, end):
                print id
                try:
                    res = urllib2.urlopen(self.RECIPE_ENDPOINT + str(id))
                except:
                    logging.exception('')
                    continue
                if res.getcode() == 200 and res.url == self.RECIPE_ENDPOINT + str(id):
                    soup = BeautifulSoup(res.read(), 'html.parser')
                    recipes.append(self._parse_recipe(soup, id))
                else:
                    print "Error code: " + str(res.getcode())
            return recipes

        pool = ThreadPool(processes=4)
        a = pool.apply_async(task, (1, 1189))
        b = pool.apply_async(task, (1189, 2378))
        c = pool.apply_async(task, (2378, 3567))
        d = pool.apply_async(task, (3567, self.LAST_RECIPE_INDEX))
        return a.get() + b.get() + c.get() + d.get()

    def scrape_ingredients(self):
        def task(start, end):
            ingredients = []
            for id in xrange(start, end):
                print id
                try:
                    res = urllib2.urlopen(self.INGR_ENDPOINT + str(id))
                except:
                    logging.exception('')
                    continue
                if res.getcode() == 200 and res.url == self.INGR_ENDPOINT + str(id):
                    soup = BeautifulSoup(res.read(), 'html.parser')
                    ingredients.append(self._parse_ingredient(soup, id))
                else:
                    print "Error code: " + str(res.getcode())
            return ingredients

        pool = ThreadPool(processes=4)
        a = pool.apply_async(task, (1, 157))
        b = pool.apply_async(task, (157, 314))
        c = pool.apply_async(task, (314, 471))
        d = pool.apply_async(task, (471, self.LAST_INGREDIENT_INDEX))
        return a.get() + b.get() + c.get() + d.get()
        # return a.get()

    def _parse_recipe(self, soup, id):
        recipe = {}
        recipe['id'] = id
        recipe['title'] = soup.find(id="wellTitle").get_text().strip().split('\n')[0]
        recipe['ingredients'] = self._parse_ingredients_for_recipe(soup)
        recipe['directions'] = self._parse_directions(soup)
        return recipe

    def _parse_ingredients_for_recipe(self, soup):
        ingredients = []
        ingrs = soup.find_all("div", {"class":"recipeMeasure"})
        for ingr in ingrs:
            ingredient = {}
            ingredient['q'] = ingr.contents[0].strip()
            ingredient['name'] = ingr.contents[1].get_text().strip()
            href = ingr.contents[1].attrs['href']
            ingredient['id'] = href[href.rfind('id=')+3:]
            ingredients.append(ingredient)
        return ingredients

    def _parse_directions(self, soup):
        directions = []
        dirs = soup.find_all("div", {"class": "recipeDirection"})
        return ". ".join(map(lambda dir: dir.get_text(), dirs)) + "."

    def _parse_ingredient(self, soup, id):
        ingredient = {'id': id}
        soup = soup.find("div", {"class":"detail"})
        headers = soup.find_all('h3')
        for header in headers:
            header_text = header.text.lower()
            element = header.nextSibling
            if header_text == 'type':
                href = element.attrs['href']
                ingredient['type_name'] = element.text
                ingredient['type_id'] = href[href.rfind('category=')+9:]
            elif header_text == 'description':
                ingredient['description'] = unicode(element)
            elif header_text == 'flavor':
                ingredient['flavor'] = self._parse_flavors_for_ingredient(element)
                break
        return ingredient

    # grab all <a> before next h3 tag
    def _parse_flavors_for_ingredient(self, node):
        flavors = []
        while node:
            if node.name == 'h3':
                break
            flavors.append(node.text)
            node = node.findNextSibling()
        return flavors