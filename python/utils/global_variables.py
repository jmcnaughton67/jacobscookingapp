import json
import os

search_path = ""
directory_path = ""
custom_header_html = ""
current_directory = ""

remove_html_extension = True

keyword_map = {}
cuisine_map = {}
category_map = {}
ingredient_map = {}
equipment_map = {}
diet_map = {}
listacle_map = {}
recipes = []
ingredient_prefix = {}

small_keyword_map = []
small_cuisine_map = []
small_category_map = []
small_ingredient_map = []
small_equipment_map = []
small_diet_map = []
small_recipes = []

smallest_recipes = []
index_pages = []

shared_notes = {}
shared_note_map = {}

def get_sorted_keywords(map):
    sorted_items = sorted(map.items(), key=lambda item: len(item[1]), reverse=True)
    sorted_map = {k: v for k, v in sorted_items}
    return sorted_map

def get_sorted_recipes():
    sorted_items = sorted(recipes, key=lambda x: x['datePublished'], reverse=True)
    return sorted_items

def get_keyword_lastmod(keyword, map):
    values = map[keyword]
    published = "19900101"
    returnValue = ""
    for value in values:
        date = value['datePublished'].replace("-", "")
        if int(date) > int(published):
            published = date
            returnValue = value['datePublished']
    return returnValue

def get_recipe(folder):
    for recipe in recipes:
        if recipe["folder"] == folder:
            return recipe
        
def get_variables():
    environment_file = "environment_variables.json"
    current_directory = os.getcwd()

    environment_path = os.path.join(current_directory, "python", environment_file)

    global search_path
    global directory_path
    global custom_header_html

    if os.path.exists(environment_path):
        with open(environment_path, 'r') as f:
            data = json.load(f)
            search_path = data['search_path']
            directory_path = data['url']
            custom_header_html = data['header']
    else:
        search_path = os.environ.get('SEARCH_PATH', os.path.join(current_directory, 'recipes'))
        directory_path = os.environ.get('SITE_URL', '')
        custom_header_html = os.environ.get('SITE_HEADER', '')

def print_variables():
    print(search_path)
    print(directory_path)
    print(custom_header_html)