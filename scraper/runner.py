from scraper import Scraper
import pickle

scraper = Scraper()

# cocktails = scraper.scrape_cocktails()
# cocktails_file = open('cocktails.pickle', 'w')
# pickle.dump(cocktails, cocktails_file)

ingredients = scraper.scrape_ingredients()
ingredients_file = open('ingredients.pickle', 'w')
pickle.dump(ingredients, ingredients_file)
