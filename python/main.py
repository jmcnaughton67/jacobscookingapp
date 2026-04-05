from utils.global_variables import *
get_variables()
from utils.global_variables import *

from utils.html_footer import *
from utils.html_header import *
from utils.html_recipe_blocks import *
from utils.link_helpers import *
from utils.bilg_ol_text import *
from utils.javascript import *

import json
import os
import re
import random
import copy
import math
from datetime import datetime

# Fetch and compile data from json files
for root, _, files in os.walk(search_path):
    for file in files:
        if file.endswith(".json") and not root.endswith("listacles") and not root.endswith("data") and not root.endswith("shared_notes"):
            json_path = os.path.join(root, file)
            with open(json_path, 'r') as f:
                data = json.load(f)

            # print(data['name'])

            # print(type(data['recipeCuisine']))

            keywords = data['keywords'].split(", ")
            cuisine_list = [data['recipeCuisine']]  if not isinstance(data['recipeCuisine'], list) else data['recipeCuisine']
            category_list = [data['recipeCategory']]  if not isinstance(data['recipeCategory'], list) else data['recipeCategory']
            ingredients = data['ingredientKeywords']
            prefix = data['recipeIngredient']

            recipes.append(data)
            small_recipes.append({
                "name": data['name'],
                "folder": data['folder'],
                "ingredientKeywords": data['ingredientKeywords'],
                "recipeCategory": ", ".join(category_list),
                "recipeCuisine": ", ".join(cuisine_list)
            })
            smallest_recipes.append(data['folder'])

            for keyword in keywords:
                if keyword in keyword_map:
                    keyword_map[keyword].append(data)
                else:
                    keyword_map[keyword] = [data]

            for ingredient in ingredients:
                if ingredient not in small_ingredient_map:
                    small_ingredient_map.append(ingredient)
            for ingredient in ingredients:
                if ingredient in ingredient_map:
                    ingredient_map[ingredient].append(data)
                else:
                    ingredient_map[ingredient] = [data]

            if "equipment" in data:
                equipments = data['equipment']
                for equipment in equipments:
                    if equipment not in small_equipment_map:
                        small_equipment_map.append(equipment)
                for equipment in equipments:
                    if equipment in equipment_map:
                        equipment_map[equipment].append(data)
                    else:
                        equipment_map[equipment] = [data]

            if "diet" in data:
                diets = data['diet']
                for diet in diets:
                    if diet not in small_diet_map:
                        small_diet_map.append(diet)
                for diet in diets:
                    if diet in diet_map:
                        diet_map[diet].append(data)
                    else:
                        diet_map[diet] = [data]

            if "sharedNotes" in data:
                notes = data['sharedNotes']
                for note in notes:
                    if note in shared_note_map:
                        shared_note_map[note].append(data)
                    else:
                        shared_note_map[note] = [data]

            for cuisine in cuisine_list:
                if cuisine not in small_cuisine_map:
                    small_cuisine_map.append(cuisine)
                if cuisine in cuisine_map:
                    cuisine_map[cuisine].append(data)
                else:
                    cuisine_map[cuisine] = [data]

            for category in category_list:
                if category not in small_category_map:
                    small_category_map.append(category)
                if category in category_map:
                    category_map[category].append(data)
                else:
                    category_map[category] = [data]

            for ingredient in prefix:
                if len(ingredient.split(" ")) > 1:
                    if ingredient.split(" ")[1] in ingredient_prefix:
                        ingredient_prefix[ingredient.split(" ")[1]].append(data)
                    else:
                        ingredient_prefix[ingredient.split(" ")[1]] = [data]

# Scrape shared notes
for root, _, files in os.walk(search_path):
    for file in files:
        if file.endswith(".json") and root.endswith("shared_notes"):
            json_path = os.path.join(root, file)
            with open(json_path, 'r') as f:
                data = json.load(f)

            shared_notes[data['folder']] = data

# Dump recipe data into folder for easy backup
for recipe_data in recipes:
    html_name = recipe_data['folder'] + ".json"
    html_path = os.path.join(current_directory, "data", html_name)

    with open(html_path, 'w') as f:
        f.write(json.dumps(recipe_data))

# create recipe htmls
for root, _, files in os.walk(search_path):
    for file in files:
        if file.endswith(".json") and not root.endswith("listacles") and not root.endswith("data") and not root.endswith("shared_notes"):
            json_path = os.path.join(root, file)
            with open(json_path, 'r') as f:
                data = json.load(f)

            html_name = "index.html"
            html_path = os.path.join(root, html_name)

            with open(html_path, 'w') as f:

                # --- JSON Schema Generation ---
                json_schema = copy.deepcopy(data)
                json_schema['recipeIngredient'] = []
                for ingredient in data['recipeIngredient']:
                    if (ingredient != "" and ":" not in ingredient):
                        json_schema['recipeIngredient'].append(ingredient)

                json_schema['recipeInstructions'] = []
                for step in data['recipeInstructions']:
                    formatted_base_url = get_recipe_link(data['folder'])
                    json_schema['recipeInstructions'].append({
                        "@type": "HowToStep",
                        "name": step['name'],
                        "url": f"{formatted_base_url}#{step['url']}",
                        "text": step['text']
                    })

                json_schema['image'] = []
                for image in data['image']:
                    json_schema['image'].append(f"https://justmy.cooking/{data['folder']}/{image}")

                cuisine_list = [data['recipeCuisine']]  if not isinstance(data['recipeCuisine'], list) else data['recipeCuisine']
                category_list = [data['recipeCategory']]  if not isinstance(data['recipeCategory'], list) else data['recipeCategory']

                json_schema['recipeCuisine'] = cuisine_list[0]
                json_schema['recipeCategory'] = category_list[0]

                if "diet" in data:
                    json_schema['suitableForDiet'] = []
                    for diet in data['diet']:
                        if diet in ["Diabetic", "Gluten Free", "Halal", "Hindu", "Kosher", "Low Calorie", "Low Fat", "Low Lactose", "Low Salt", "Vegan", "Vegetarian"]:
                            json_schema['suitableForDiet'].append(diet.replace(" ", "") + "Diet")


                f.write(f"{get_opener()}")
                f.write(f"<script type=\"application/ld+json\">{json.dumps(json_schema)}</script>")
                f.write(f"<title>{data['name']} - Cooking With Spud</title>")
                f.write(f"<meta name=\"description\" content=\"{data['description']}\">")
                f.write(f"{get_header()}")

                f.write(f"<div id=\"recipePage\">")
                f.write(f"<div id=\"recipe\">")
                f.write(f"<h1 class=\"offset offsetHeight\">{data['name']}</h1>")
                
                f.write(f"<div id=\"recipeImg\" class=\"border\"><img alt=\"{data['name']}\" src=\"{directory_path}/{data['folder']}/{data['image'][0]}\"></img></div>")
                
                f.write(f"<div class=\"recipeContainer\">")
                f.write(f"<div style=\"min-width: fit-content;\" class=\"recipeComponent border\">")

                f.write(f"<p>{data['description']}</p>")

                f.write(f"<div class=\"keywordContainer\">")
                f.write(f"<div class=\"keywords border\"><a onClick=\"sharePage();\" href=\"#\"><p>Share <i class=\"fa\">&#xf1e0;</i></p></a></div>")
                # f.write(f"<div class=\"keywords border\" style=\"background-color: unset;\"><p>Author: {data['author']['name']}</p></div>")
                f.write(f"<div class=\"keywords border\" style=\"background-color: unset;\"><p>Published: {data['datePublished']}</p></div>")
                if data['datePublished'] != data['lastMod']:
                    f.write(f"<div class=\"keywords border\" style=\"background-color: unset;\"><p>Last Modified: {data['lastMod']}</p></div>")
                f.write(f"<div class=\"keywords border\" style=\"background-color: unset;\"><p>Creates: {data['recipeYield']}</p></div>")
                f.write(f"</div>")

                f.write(f"</br>")
                f.write(f"<div class=\"keywordContainer\">")
                f.write(f"<h3>Time:</h3>")

                if iso8601_to_human_readable(data['prepTime']) != "0 minutes" and iso8601_to_human_readable(data['prepTime']) != "0 hours":
                    f.write(f"<div class=\"keywords border\" style=\"background-color: unset;\"><p>Prep: {iso8601_to_human_readable(data['prepTime'])}</p></div>")
                if "marinatingTime" in data:
                    f.write(f"<div class=\"keywords border\" style=\"background-color: unset;\"><p>Marinate: {iso8601_to_human_readable(data['marinatingTime'])}</p></div>")
                if iso8601_to_human_readable(data['cookTime']) != "0 minutes" and iso8601_to_human_readable(data['cookTime']) != "0 hours":
                    f.write(f"<div class=\"keywords border\" style=\"background-color: unset;\"><p>Cook: {iso8601_to_human_readable(data['cookTime'])}</p></div>")
                f.write(f"<div class=\"keywords border\" style=\"background-color: unset;\"><p>Total: {iso8601_to_human_readable(data['totalTime'])}</p></div>")

                f.write(f"</div>")

                if "equipment" in data:
                    f.write(f"</br>")
                    f.write(f"<div class=\"keywordContainer\">")
                    f.write(f"<h3>Equipment:</h3>")
                    
                    for equipment in data['equipment']:
                        link = format_link(f"{directory_path}/keywords/{equipment.lower().replace(' ', '_')}.html")
                        f.write(f"<div class=\"keywords border\"><a href=\"{link}\"><p>{equipment}</p></a></div>")

                    f.write(f"</div>")

                if "diet" in data:
                    f.write(f"</br>")
                    f.write(f"<div class=\"keywordContainer\">")
                    f.write(f"<h3>Dietary:</h3>")
                    
                    for diet in data['diet']:
                        link = format_link(f"{directory_path}/keywords/{diet.lower().replace(' ', '_')}.html")
                        f.write(f"<div class=\"keywords border\"><a href=\"{link}\"><p>{diet}</p></a></div>")

                    f.write(f"</div>")


                # f.write(f"<h3>Description:</h3>")
                # f.write(f"<p>{data['description']}</p>")
                f.write(f"</div>")

                # Ingredients Section
                f.write(f"<div class=\"recipeComponent border\">")
                f.write(f"<h2 class=\"removeOffsetTop\">Ingredients</h2>")
                f.write(f"<ul>")
                for ingredient in data['recipeIngredient']:
                    if ingredient == "":
                        f.write(f"</ul><ul>")
                    elif ":" in ingredient:
                        f.write(f"<p class=\"removeOffsetHeight\">{ingredient}</p>")
                    else:
                        ingredient_linked = ingredient
                        replacement = ""
                        ingredient_text_to_replace = ""
                        for ingre_name in ingredient_map:
                            if ingre_name in ingredient_linked:
                                if len(ingre_name) > len(replacement):
                                    replacement = ingre_name
                                    ingredient_text_to_replace = ingre_name 
                            # Check for plurals
                            if (ingre_name + "s") in ingredient_linked:
                                if len(ingre_name + "s") > len(replacement):
                                    replacement = ingre_name
                                    ingredient_text_to_replace = ingre_name + "s" 
                            # Check for "es" plurals
                            if (ingre_name + "es") in ingredient_linked:
                                if len(ingre_name + "es") > len(replacement):
                                    replacement = ingre_name
                                    ingredient_text_to_replace = ingre_name + "es"
                            # Check for y to "ies" plurals
                            if ingre_name.endswith("y"):
                                if (ingre_name[:-1] + "ies") in ingredient_linked:
                                    if len(ingre_name[:-1] + "ies") > len(replacement):
                                        replacement = ingre_name
                                        ingredient_text_to_replace = ingre_name[:-1] + "ies"
                            # Check for leaves
                            if "Leaf" in ingre_name:
                                leave_ingre_name = ingre_name.replace("Leaf", "Leaves")
                                if leave_ingre_name in ingredient_linked:
                                    if len(leave_ingre_name) > len(replacement):
                                        replacement = ingre_name
                                        ingredient_text_to_replace = leave_ingre_name 

                        if replacement and ingredient_text_to_replace:
                            link = format_link(f"{directory_path}/keywords/{replacement.lower().replace(' ', '_')}.html")
                            ingredient_linked = ingredient_linked.replace(ingredient_text_to_replace, f"<a href=\"{link}\">{ingredient_text_to_replace}</a>")

                        f.write(f"<li>{ingredient_linked}</li>")
                f.write(f"</ul>")
                f.write(f"</div>")

                # Steps Section
                f.write(f"<div class=\"recipeComponent border\">")
                f.write(f"<h2 class=\"removeOffsetTop\">Steps</h2>")
                f.write(f"<ol>")
                for step in data['recipeInstructions']:
                    f.write(f"<li><a href=\"#{str(step['url'])}\"></a>{step['text']}</li>")
                f.write(f"</ol>")
                f.write(f"</div>")

                # Notes Section
                f.write(f"<div style=\"min-width: fit-content;\" class=\"recipeComponent border\">")
                if "sharedNotes" in data:
                    f.write(f"<h2 class=\"removeOffsetTop\">Notes for {data['name']}</h2>")
                else:
                    f.write(f"<h2 class=\"removeOffsetTop\">Notes</h2>")
                f.write(f"<ul>")
                for note in data['notes']:
                    f.write(f"<li>{note}</li>")
                f.write(f"</ul>")

                f.write(f"</br>")
                f.write(f"<div class=\"keywordContainer\">")
                f.write(f"<h3>Categories:</h3>")
                for category_linked in category_list:
                    category_to_replace = ""
                    for category_name in category_map:
                        if category_name in category_linked:
                            if len(category_name) > len(category_to_replace):
                                category_to_replace = category_name
                    link = format_link(f"{directory_path}/keywords/{category_to_replace.lower().replace(' ', '_')}.html")
                    category_linked = category_linked.replace(category_to_replace, f"<a href=\"{link}\"><p>{category_to_replace}</p></a>")
                    f.write(f"<div class=\"keywords border\">{category_linked}</div>")
                f.write(f"</div>")

                f.write(f"</br>")
                f.write(f"<div class=\"keywordContainer\">")
                f.write(f"<h3>Cuisines:</h3>")
                for cuisine_linked in cuisine_list:
                    cuisine_to_replace = ""
                    for cuisine_name in cuisine_map:
                        if cuisine_name in cuisine_linked:
                            if len(cuisine_name) > len(cuisine_to_replace):
                                cuisine_to_replace = cuisine_name
                    link = format_link(f"{directory_path}/keywords/{cuisine_to_replace.lower().replace(' ', '_')}.html")
                    cuisine_linked = cuisine_linked.replace(cuisine_to_replace, f"<a href=\"{link}\"><p>{cuisine_to_replace}</p></a>")
                    f.write(f"<div class=\"keywords border\">{cuisine_linked}</div>")
                f.write(f"</div>")

                f.write(f"</div>")

                if "sharedNotes" in data:
                    for note_name in data['sharedNotes']:
                        f.write(f"{return_shared_note_html(note_name, data['folder'])}")

                f.write(f"</div>") # Close recipeContainer
                f.write(f"</div>") # Close recipe

                # Sidecar Section
                f.write(f"<div id=\"recipeSidecar\">")
                if "relatedRecipes" in data:
                    f.write(f"<h1 class=\"offset removeOffsetHeight\">Related Recipes</h1>")
                    f.write(f"<div class=\"recipeContainer\">")

                    for related_recipe in data['relatedRecipes']:
                        f.write(f"{return_recipe_tile(get_recipe(related_recipe))}")
                                

                    f.write(f"</div>")

                    if len(data['relatedRecipes']) < 3:
                        f.write(f"<h1 class=\"offset\">Other Recipes</h1>")
                        f.write(f"<div class=\"recipeContainer\">")

                        printed_recipes = set()
                        printed_recipes.add(data['name'])
                        for _ in range(4):
                            while True:
                                random_recipe = random.choice(recipes)
                                if random_recipe['name'] not in printed_recipes:
                                    f.write(f"{return_recipe_tile(random_recipe)}")
                                    printed_recipes.add(random_recipe['name'])
                                    break

                        f.write(f"</div>")
                else:
                    f.write(f"<h1 class=\"offset removeOffsetHeight\">Other Recipes</h1>")
                    f.write(f"<div class=\"recipeContainer\">")

                    printed_recipes = set()
                    printed_recipes.add(data['name'])
                    for _ in range(4):
                        while True:
                            random_recipe = random.choice(recipes)
                            if random_recipe['name'] not in printed_recipes:
                                f.write(f"{return_recipe_tile(random_recipe)}")
                                printed_recipes.add(random_recipe['name'])
                                break

                    f.write(f"</div>")

                f.write(return_keyword_setion("style=\"min-width: fit-content;\"", 20))
                f.write(f"</div>")
                f.write(f"</div>")

                f.write(f"{get_footer()}")

# Create Listacle pages
for root, _, files in os.walk(search_path):
    for file in files:
        if file.endswith(".json") and root.endswith("listacles"):
            json_path = os.path.join(root, file)
            with open(json_path, 'r') as f:
                data = json.load(f)

            listacle_name = data['folder']
            
            listacle_map[listacle_name] = data

            html_name = data['folder'] + ".html"
            html_path = os.path.join(root, html_name)

            with open(html_path, 'w') as f:
                f.write(f"{get_opener()}")
                f.write(f"<title>{data['name']} - Cooking With Spud</title>")
                f.write(f"<meta name=\"description\" content=\"{data['description']}\">")

                itemList = []
                position = 1
                for recipe in data['recipes']:
                    
                    formatted_url = get_recipe_link(recipe['folder'])
                    itemList.append({
                        "@type": "ListItem",
                        "position": position,
                        "url": formatted_url
                    })
                    position += 1

                f.write(f"""
                    <script type="application/ld+json">
                    {{
                    "@context": "https://schema.org",
                    "@type": "ItemList",
                    "itemListElement": {json.dumps(itemList)}
                    }}
                    </script>
                """)
                f.write(f"{get_header()}")

                f.write(f"<h1 class=\"offset\" style=\"margin-bottom:0rem;\">{data['name']}</h1>")
                f.write(f"<p class=\"offset\" style=\"margin-bottom:0rem;\">{data['description']}</p>")
                f.write(f"<div class=\"recipeContainer\">")
                
                for recipe in data['recipes']:
                    f.write(f"{return_recipe_tile(get_recipe(recipe['folder']), recipe['description'])}")
                f.write(f"</div>")
                f.write(f"{get_footer()}")

# Create listacle listacle
html_name = "listacles.html"
html_path = os.path.join(search_path, html_name)

with open(html_path, 'w') as f:
    f.write(f"{get_opener()}")
    f.write(f"<title>Listacles - Cooking With Spud</title>")
    f.write(f"<meta name=\"description\" content=\"Just my cooking listacles. No bells or whistles, no life stories (ish), just groupings of recipes I use every other week.\">")

    # ItemList Schema
    itemList = []
    position = 1 
    for listacle_name, listacle in listacle_map.items():
        listacle_base_url = f"https://justmy.cooking/listacles/{listacle['folder']}.html"
        formatted_url = format_link(listacle_base_url)
        itemList.append({
            "@type": "ListItem",
            "position": position,
            "url": formatted_url
        })
        position += 1

    f.write(f"""
        <script type="application/ld+json">
        {{
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": {json.dumps(itemList)}
        }}
        </script>
    """)
    f.write(f"{get_header()}")

    # Add recipe pages
    f.write(f"<h1 class=\"offset\" style=\"margin-bottom:0rem;\">Listacles</h1>")
    f.write(f"<p class=\"offset\" style=\"margin-bottom:0rem;\">Meaningful groupings of recipes on this site. Things like classics from my childhood or collections of what I made for Christmas.</p>")
    f.write(f"<div class=\"recipeContainer\">")
    for listacle_name, listacle in listacle_map.items():
        f.write(f"{return_listacle_tile(listacle)}")
    f.write(f"</div>")

    f.write(return_keyword_setion("", 20))
    f.write(f"{get_footer()}")

# Create index.html (and paginated index pages)
def process_chunks(input_map, chunk_size=30):
    if isinstance(input_map, dict):
        items = list(input_map.items())
    elif isinstance(input_map, (list, tuple, str, set)):
        items = list(input_map)
    else:
        raise TypeError("Input map must be a dictionary, list, tuple, string, or set") # Keeping this check as it was in original

    num_chunks = math.ceil(len(items) / chunk_size)

    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        if isinstance(input_map, dict):
            chunk_map = dict(chunk)
        elif isinstance(input_map, list):
            chunk_map = chunk
        elif isinstance(input_map, tuple):
            chunk_map = tuple(chunk)
        elif isinstance(input_map, str):
            chunk_map = "".join(chunk)
        elif isinstance(input_map, set):
            chunk_map = set(chunk)
        else:
            chunk_map = chunk

        create_index_pages(chunk_map, int(i / chunk_size), num_chunks - 1)


def return_page_numbers(index, num_chunks_minus_1):
    page_string = ""
    pages = ""
    num_chunks = num_chunks_minus_1 + 1

    for i in range(num_chunks):
        is_current_page = (i == index)
        style = " style=\"text-decoration: underline; background-color: light-dark(var(--light-recipe-background), var(--dark-recipe-background));\"" if is_current_page else ""
        page_num_display = str(i + 1)

        if i == 0:
            link = format_link(f"{directory_path}/index.html")
        else:
            link = format_link(f"{directory_path}/index{str(i)}.html")
        pages += f"<div class=\"keywords border\"><a href=\"{link}\"><p{style}>{page_num_display}</p></a></div>"

    prev_link_html = ""
    next_link_html = ""
    if index > 0:
        prev_page_index = index - 1
    else:
        prev_page_index = str(index) + "#"
    prev_link = format_link(f"{directory_path}/index.html" if prev_page_index == 0 else f"{directory_path}/index{prev_page_index}.html")
    prev_link_html = f"<div class=\"keywords border\"><a href=\"{prev_link}\"><p>&lt;--</p></a></div>"
    if index < num_chunks_minus_1:
        next_page_index = index + 1
    else:
        next_page_index = str(index) + "#"
    next_link = format_link(f"{directory_path}/index{next_page_index}.html")
    next_link_html = f"<div class=\"keywords border\"><a href=\"{next_link}\"><p>--&gt;</p></a></div>"
    

    page_string += "<div class=\"keywordContainer offsetLeftEight\">"
    page_string += prev_link_html
    page_string += pages
    page_string += next_link_html
    page_string += "</div>"

    return page_string


def create_index_pages(map_chunk, index, num_chunks_minus_1):
    html_name = "index.html" if index == 0 else f"index{index}.html"
    html_path = os.path.join(search_path, html_name)
    index_pages.append(html_name)

    with open(html_path, 'w') as f:
        f.write(f"{get_opener()}")
        f.write(f"<title>Cooking With Spud</title>")
        f.write(f"<meta name=\"description\" content=\"Just my cooking. No bells or whistles, no life stories, just recipes I use every other week.\">")

        # ItemList Schema
        itemList = []
        position = 1 
        for recipe in map_chunk:
            formatted_url = get_recipe_link(recipe['folder'])
            itemList.append({
                "@type": "ListItem",
                "position": position,
                "url": formatted_url
            })
            position += 1

        f.write(f"""
            <script type="application/ld+json">
            {{
            "@context": "https://schema.org",
            "@type": "ItemList",
            "itemListElement": {json.dumps(itemList)}
            }}
            </script>
        """)
        f.write(f"{get_header()}")

        # Add recipe pages
        f.write(f"<h1 class=\"offset\" style=\"margin-bottom:0rem;\">Cooking with Spud</h1>")
        f.write(f"<div class=\"recipeContainer\">")
        recipe_count = 0
        for recipe in map_chunk:
            f.write(f"{return_recipe_tile(recipe)}")
            recipe_count += 1
            if recipe_count >= 30:
                break
        f.write(f"</div>")

        f.write(return_page_numbers(index, num_chunks_minus_1))
        f.write(return_keyword_setion("", 20))
        f.write(f"{get_footer()}")

process_chunks(get_sorted_recipes())

# Create all_recipes.html
html_name = "all_recipes.html"
html_path = os.path.join(search_path, html_name)

with open(html_path, 'w') as f:
    f.write(f"{get_opener()}")
    f.write(f"<title>All Recipes - Cooking With Spud</title>")
    f.write(f"<meta name=\"description\" content=\"All of the recipes on Cooking With Spud\">")

    itemList = []
    position = 1
    for recipe in recipes:
        
        formatted_url = get_recipe_link(recipe['folder'])
        itemList.append({
            "@type": "ListItem",
            "position": position,
            "url": formatted_url
        })
        position += 1

    f.write(f"""
        <script type="application/ld+json">
        {{
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": {json.dumps(itemList)}
        }}
        </script>
    """)
    f.write(f"{get_header()}")

    f.write(f"<h1 class=\"offset\" style=\"margin-bottom:0rem;\">All Recipes (A-Z)</h1>")
    f.write(f"<div class=\"recipeContainer\">")
    
    for recipe in recipes:
        f.write(f"{return_recipe_tile(recipe)}")
    f.write(f"</div>")
    f.write(f"{get_footer()}")

# Create keyword pages
def create_keyword_pages(map_data, description_start, description_end):
    keywords_dir = os.path.join(search_path, "keywords")

    for key, values in map_data.items():
        file_name_base = key.lower().replace(" ", "_")
        html_name = file_name_base + ".html"
        html_path = os.path.join(keywords_dir, html_name)

        with open(html_path, 'w') as f:
            f.write(f"{get_opener()}")
            f.write(f"<title>{key} Recipes - Cooking With Spud</title>")
            f.write(f"<meta name=\"description\" content=\"{description_start} {key} {description_end} - Cooking With Spud\">")

            itemList = []
            position = 1
            for object_data in values:
                formatted_url = get_recipe_link(object_data['folder'])
                itemList.append({
                    "@type": "ListItem",
                    "position": position,
                    "url": formatted_url
                })
                position += 1

            f.write(f"""
                <script type="application/ld+json">
                {{
                "@context": "https://schema.org",
                "@type": "ItemList",
                "itemListElement": {json.dumps(itemList)}
                }}
                </script>
            """)
            f.write(f"{get_header()}")
            f.write(f"<h1 class=\"offset removeOffsetHeight\">{description_start} {key} {description_end}</h1>")
            f.write(f"<div class=\"recipeContainer\">")
            for object_data in values:
                f.write(f"{return_recipe_tile(object_data)}")
            f.write(f"</div>")
            f.write(return_keyword_setion("", 20))
            f.write(f"{get_footer()}")

create_keyword_pages(cuisine_map, "Recipes that are", "(roughly) in origin")
create_keyword_pages(category_map, "", "recipes")
create_keyword_pages(ingredient_map, "Recipes that contain", "as an ingredient")
create_keyword_pages(equipment_map, "Recipes that require a", "")
create_keyword_pages(diet_map, "Recipes for a", "diet")

# Create all keywords page
html_name = "all_keywords.html"
html_path = os.path.join(search_path, html_name)

with open(html_path, 'w') as f:
    f.write(f"{get_opener()}")
    f.write(f"<title>All Keywords - Cooking With Spud</title>")
    f.write(f"<meta name=\"description\" content=\"Listing out and linking to all keyword pages\">")
    f.write(f"{get_header()}")
    f.write(f"<h1 class=\"offset removeOffsetHeight\">All Keyword Pages</h1>")
    f.write(return_keyword_setion("style=\"min-width: fit-content;\"", 99999))
    f.write(f"{get_footer()}")


# Create about page
html_name = "about.html"
html_path = os.path.join(search_path, html_name)

with open(html_path, 'w') as f:
    f.write(f"{get_opener()}")
    f.write(f"<title>About - Cooking With Spud</title>")
    f.write(f"<meta name=\"description\" content=\"The obligatory about page for Cooking With Spud\">")
    f.write(f"{get_header()}")
    f.write(f"<div id=\"about\" class=\"\">")
    f.write(f"<h1 class=\"removeOffsetHeight offset\">About</h1>")
    f.write(f"<p class=\"removeOffsetTop offset\">That obligatory about page</p>")
    f.write(f"{get_about_text()}")

    f.write(f"<h1 class=\"removeOffsetTop removeOffsetHeight offset\">Stats</h1>")
    f.write(f"<p class=\"removeOffsetTop offset\">Just some stats I wanted</p>")

    f.write(f"<div class=\"keywordSection\">")

    # Recipe Stats
    most_ingredient_recipe = ["", 0]
    least_ingredient_recipe = ["", 20]
    most_step_recipe = ["", 0]
    least_step_recipe = ["", 20]
    most_equipment_recipe = ["", 0]
    shortest_recipe = ["", 999999999]
    longest_recipe = ["", 0]
    total_ingredients = 0
    total_steps = 0
    total_seconds = 0
    for recipe in recipes:
        total_ingredients = total_ingredients + len(recipe["recipeIngredient"])
        total_steps = total_steps + len(recipe["recipeInstructions"])
        total_seconds = total_seconds + iso8601_to_seconds(recipe["totalTime"])
        if len(recipe["recipeIngredient"]) > most_ingredient_recipe[1]:
            most_ingredient_recipe[0] = recipe["name"]
            most_ingredient_recipe[1] = len(recipe["recipeIngredient"])
        if len(recipe["recipeIngredient"]) < least_ingredient_recipe[1]:
            least_ingredient_recipe[0] = recipe["name"]
            least_ingredient_recipe[1] = len(recipe["recipeIngredient"])
        if len(recipe["recipeInstructions"]) > most_step_recipe[1]:
            most_step_recipe[0] = recipe["name"]
            most_step_recipe[1] = len(recipe["recipeInstructions"])
        if len(recipe["recipeInstructions"]) < least_step_recipe[1]:
            least_step_recipe[0] = recipe["name"]
            least_step_recipe[1] = len(recipe["recipeInstructions"])
        if "equipment" in recipe:
            if len(recipe["equipment"]) > most_equipment_recipe[1]:
                most_equipment_recipe[0] = recipe["name"]
                most_equipment_recipe[1] = len(recipe["equipment"])
        if iso8601_to_seconds(recipe["totalTime"]) < shortest_recipe[1]:
            shortest_recipe[0] = recipe["name"]
            shortest_recipe[1] = iso8601_to_seconds(recipe["totalTime"])
        if iso8601_to_seconds(recipe["totalTime"]) > longest_recipe[1]:
            longest_recipe[0] = recipe["name"]
            longest_recipe[1] = iso8601_to_seconds(recipe["totalTime"])

    
    f.write(f"<div class=\"keywordBlock border\">")
    f.write(f"<h1 class=\"\">Recipe Stats</h1>")
    f.write(f"<div class=\"keywordContainer\">")
    f.write(f"<div class=\"keywords border\"><p>{len(recipes)} Recipes</p></div>")
    f.write(f"<div class=\"keywords border\"><a href=\"{get_recipe_link(most_ingredient_recipe[0])}\"><p>Min Ingredients: {most_ingredient_recipe[0]} ({most_ingredient_recipe[1]})</p></a></div>")
    f.write(f"<div class=\"keywords border\"><p>AVG Ingredients: {math.floor(total_ingredients / len(recipes))}</p></div>")
    f.write(f"<div class=\"keywords border\"><a href=\"{get_recipe_link(least_ingredient_recipe[0])}\"><p>Max Ingredients: {least_ingredient_recipe[0]} ({least_ingredient_recipe[1]})</p></a></div>")
    f.write(f"<div class=\"keywords border\"><a href=\"{get_recipe_link(most_step_recipe[0])}\"><p>Max Steps: {most_step_recipe[0]} ({most_step_recipe[1]})</p></a></div>")
    f.write(f"<div class=\"keywords border\"><p>AVG Steps: {math.floor(total_steps / len(recipes))}</p></div>")
    f.write(f"<div class=\"keywords border\"><a href=\"{get_recipe_link(least_step_recipe[0])}\"><p>Min Steps: {least_step_recipe[0]} ({least_step_recipe[1]})</p></a></div>")
    f.write(f"<div class=\"keywords border\"><a href=\"{get_recipe_link(most_equipment_recipe[0])}\"><p>Most Equipment: {most_equipment_recipe[0]} ({most_equipment_recipe[1]})</p></a></div>")
    f.write(f"<div class=\"keywords border\"><a href=\"{get_recipe_link(longest_recipe[0])}\"><p>Max Duration: {longest_recipe[0]} ({math.floor((longest_recipe[1]/60))} Minutes)</p></a></div>")
    f.write(f"<div class=\"keywords border\"><p>AVG Duration: {math.floor((total_seconds/60) / len(recipes))} Minutes</p></div>")
    f.write(f"<div class=\"keywords border\"><a href=\"{get_recipe_link(shortest_recipe[0])}\"><p>Min Duration: {shortest_recipe[0]} ({math.floor((shortest_recipe[1]/60))} Minutes)</p></a></div>")
    f.write(f"</div>")
    f.write(f"</div>")
    
    f.write(f"{return_basic_stats(ingredient_map, 'Ingredients', 'Ingredient Stats')}")
    f.write(f"{return_basic_stats(cuisine_map, 'Cuisines', 'Cuisine Stats')}")
    f.write(f"{return_basic_stats(category_map, 'Categories', 'Category Stats')}")
    f.write(f"{return_basic_stats(equipment_map, 'Equipment', 'Equipment Stats')}")

    f.write(f"</div>")
    f.write(f"</div>")

    f.write(return_keyword_setion("", 20))
    
    f.write(f"{get_footer()}")


# Create random js file
js_name = "random.js"
js_path = os.path.join(search_path, js_name)

with open(js_path, 'w') as f:
    f.write(get_random_js())

# Create search js file
js_name = "search.js"
js_path = os.path.join(search_path, js_name)

with open(js_path, 'w') as f:
    f.write(get_search_js())

# Create search page
html_name = "search.html"
html_path = os.path.join(search_path, html_name)

# Reverted: Removed encoding
with open(html_path, 'w') as f:
    f.write(f"{get_opener()}")
    f.write(f"<title>Search - Cooking With Spud</title>")
    f.write(f"<meta name=\"description\" content=\"Search recipes and find what you're looking for using keywords\">")
    f.write(f"<script type=\"text/javascript\" src=\"{directory_path}/search.js\"></script>")
    f.write(f"{get_header()}")

    f.write(f"<div class=\"offset offsetHeight border\" id=\"searchHead\">")
    f.write(f"<h1>Search</h1>")
    f.write(f"<h3>Enter ingredients, recipes, cuisines or categories below to start searching. You can combine search terms by clicking the + to add things as a filter.</h3>")
    f.write(f"<input onkeyup=\"search()\" class=\"keywords border offsetHeight\" id=\"searchInput\" type=\"text\" placeholder=\"Search...\"></input>")
    f.write(f"<h3>Filters</h3>")
    f.write(f"<div class=\"keywordContainer\" id=\"filters\">")
    f.write(f"<div class=\"keywords border\"><p>No Filters Selected</p></div>")
    f.write(f"</div>")
    f.write(f"</div>")

    f.write(f"<div class=\"offset border\" id=\"searchBase\">")
    f.write(f"<h1>Search Results</h1>")
    f.write(f"<h3>Recipes</h3>")
    f.write(f"<div class=\"keywordContainer\" id=\"recipeResults\">")
    f.write(f"<div class=\"keywords border\"><p>No Results</p></div>")
    f.write(f"</div>")
    f.write(f"<h3>Ingredients</h3>")
    f.write(f"<div class=\"keywordContainer\" id=\"ingredientResults\">")
    f.write(f"<div class=\"keywords border\"><p>No Results</p></div>")
    f.write(f"</div>")
    f.write(f"<h3>Cuisines</h3>")
    f.write(f"<div class=\"keywordContainer\" id=\"cuisineResults\">")
    f.write(f"<div class=\"keywords border\"><p>No Results</p></div>")
    f.write(f"</div>")
    f.write(f"<h3>Categories</h3>")
    f.write(f"<div class=\"keywordContainer\" id=\"categoryResults\">")
    f.write(f"<div class=\"keywords border\"><p>No Results</p></div>")
    f.write(f"</div>")
    f.write(f"</div>")

    f.write(f"{get_footer()}")


# Create sitemap
xml_name = "sitemap.xml"
xml_path = os.path.join(search_path, xml_name)
# today_date = datetime.today().strftime('%Y-%m-%d')

with open(xml_path, 'w') as f:
    f.write(f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write(f"<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")

    def sitemap_entry(loc, lastmod):
        formatted_loc = format_link(loc)
        return f"""
    <url>
        <loc>{formatted_loc}</loc>
        <lastmod>{lastmod}</lastmod>
    </url>"""

    # Index Pages
    for index_page_name in index_pages:
        loc = f"{directory_path}/{index_page_name}"
        f.write(sitemap_entry(loc, "2025-02-16"))

    # Static Pages - Add .html before formatting
    static_pages = [
            ["search.html", "2025-02-20"],
            ["about.html", "2026-01-10"],
            ["all_keywords.html", "2025-02-26"],
            ["all_recipes.html", "2025-02-26"],
            ["listacles.html", "2025-05-31"]
        ]
    # static_pages = ["search.html", "about.html", "allKeywords.html", "allRecipes.html"]
    for page in static_pages:
        loc = f"{directory_path}/{page[0]}"
        f.write(sitemap_entry(loc, page[1]))

    # Keyword Pages - Add .html before formatting
    for key in ingredient_map.keys():
        file_name = key.lower().replace(" ", "_") + ".html"
        loc = f"{directory_path}/keywords/{file_name}"
        f.write(sitemap_entry(loc, get_keyword_lastmod(key, ingredient_map)))
    for key in cuisine_map.keys():
        file_name = key.lower().replace(" ", "_") + ".html"
        loc = f"{directory_path}/keywords/{file_name}"
        f.write(sitemap_entry(loc, get_keyword_lastmod(key, cuisine_map)))
    for key in category_map.keys():
        file_name = key.lower().replace(" ", "_") + ".html"
        loc = f"{directory_path}/keywords/{file_name}"
        f.write(sitemap_entry(loc, get_keyword_lastmod(key, category_map)))

    # Recipe Pages - Add .html before formatting
    for data in recipes:
        lastmod_date = data.get('lastMod', data['datePublished'])
        recipe_file = data['folder'] + ".html"
        loc = f"{directory_path}/{data['folder']}/{recipe_file}"
        f.write(sitemap_entry(loc, lastmod_date))

    for listacle_name, data in listacle_map.items():
        lastmod_date = data['lastMod']
        listacle_file = data['folder'] + ".html"
        loc = f"{directory_path}/listacles/{listacle_file}"
        f.write(sitemap_entry(loc, lastmod_date))

    f.write(f"\n</urlset>")

# print(return_keyword_setion("style=\"min-width: fit-content;\"", 20))

# for k, v in ingredient_map.items():
#     if len(v) < 2:
#         print(f"{k} - {v[0]['name']}")

print(f"{len(keyword_map)} keywords")
print(f"{len(ingredient_map)} ingredients")
print(f"{len(category_map)} categories")
print(f"{len(cuisine_map)} cuisins")
print(f"{len(listacle_map)} listacles")
print(f"{len(recipes)} recipes")

print("Script finished.")