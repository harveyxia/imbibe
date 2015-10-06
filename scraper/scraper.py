import urllib2
from bs4 import BeautifulSoup

class Scraper:
    RECIPE_ENDPOINT = "http://www.cocktaildb.com/recipe_detail?id="
    INGR_ENDPOINT = "http://www.cocktaildb.com/ingr_detail?id="
    LAST_RECIPE_INDEX = 4758
    LAST_INGREDIENT_INDEX = 631

    def scrape_cocktails(self):
        recipes = []
        # scrape all recipes
        for id in xrange(1, 100):
            print id
            res = urllib2.urlopen(self.RECIPE_ENDPOINT + str(id))
            if res.getcode() == 200 and res.url == self.RECIPE_ENDPOINT + str(id):
                soup = BeautifulSoup(res.read(), 'html.parser')
                recipes.append(self._parse_recipe(soup, id))
            else:
                print "Error code: " + str(res.getcode())
        return recipes

    def scrape_ingredients(self):
        ingredients = []
        for id in xrange(1, 4):
            print id
            res = urllib2.urlopen(self.INGR_ENDPOINT + str(id))
            if res.getcode() == 200 and res.url == self.INGR_ENDPOINT + str(id):
                soup = BeautifulSoup(res.read(), 'html.parser')
                ingredients.append(self._parse_ingredient(soup, id))
            else:
                print "Error code: " + str(res.getcode())
        return ingredients

    def _parse_recipe(self, soup, id):
        recipe = {}
        recipe['id'] = id
        recipe['title'] = soup.find(id="wellTitle").get_text().strip().split('\n')[0]
        recipe['ingredients'] = self._parse_ingredients(soup)
        recipe['directions'] = self._parse_directions(soup)
        return recipe

    def _parse_ingredients(self, soup):
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
                ingredient['description'] = element
            elif header_text == 'flavor':
                ingredient['flavor'] = element.text

        # href = soup.contents[4].attrs['href']
        # ingredient['type_name'] = soup.contents[4].get_text()
        # ingredient['type_id'] = href[href.rfind('category=')+9:]
        # ingredient['description'] = soup.contents[7]
        # ingredient['flavor'] = soup.contents[9].get_text()
        return ingredient