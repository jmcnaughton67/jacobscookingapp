from .global_variables import *
from .link_helpers import *
from .date_helpers import *

def return_recipe_tile(data, description = ""):
    recipe_link = get_recipe_link(data['folder'])
    image_link = f"{directory_path}/{data['folder']}/{data['image'][0]}"

    extra = ""

    if description != "":
        extra = f"<p class=\"subtitle\">{description}</p>"

    cuisine = data['recipeCuisine']  if not isinstance(data['recipeCuisine'], list) else data['recipeCuisine'][0]
    category = data['recipeCategory']  if not isinstance(data['recipeCategory'], list) else data['recipeCategory'][0]

    return f"""
        <div class="recipeTile border">
            <a href="{recipe_link}">
                <div class="innerTile">
                    <img alt="{data['name']}" src="{image_link}"></img>
                    <p class="title">{data['name']}</p>
                    <p class="subtitle">{cuisine} {category}</p>
                    <p class="subtitle">Time: {iso8601_to_human_readable(data['totalTime'])}</p>
                    {extra}
                </div>
            </a>
        </div>
        """

def return_listacle_tile(data):
    listacle_link = format_link(f"{directory_path}/listacles/{data['folder']}.html")
    image_link = f"{directory_path}/{data['image']}/{data['image']}_0.jpg"

    listacle_recipes = ""
    for listacle_recipe in data['recipes']:
        listacle_recipes = listacle_recipes + f"<div class=\"keywords border\" style=\"background-color: unset;\"><p>{get_recipe(listacle_recipe['folder'])['name']}</p></div>"

    return f"""
        <div class="recipeTile border">
            <a href="{listacle_link}">
                <div class="innerTile">
                    <img alt="{data['name']}" src="{image_link}"></img>
                    <p class="title">{data['name']}</p>
                    <p class=\"subtitle\">{data['description']}</p>
                    <div class="keywordContainer" style="padding: 1rem 1rem 0 1rem;">
                    {listacle_recipes}
                    </div>
                </div>
            </a>
        </div>
        """

def return_keyword_setion(ingredient_style, limit):
    keyword_section = ""
    keyword_section = keyword_section + f"<div class=\"keywordSection\">"
    # Add ingredient pages
    keyword_section = keyword_section + f"<div {ingredient_style} class=\"keywordBlock border\">"
    keyword_section = keyword_section + f"<h1>Recipes by Ingredient</h1>"
    keyword_section = keyword_section + f"<div class=\"keywordContainer\">"
    outputs = 0
    for key, values in get_sorted_keywords(ingredient_map).items():
        file_name = key.lower().replace(" ", "_")
        link = format_link(f"{directory_path}/keywords/{file_name}.html")
        keyword_section = keyword_section + f"<div class=\"keywords border\"><a href=\"{link}\"><p>{key} ({len(values)})</p></a></div>"
        outputs = outputs + 1
        if (outputs == limit):
            break
    keyword_section = keyword_section + f"</div>"
    keyword_section = keyword_section + f"</div>"
    # Add cuisine pages
    keyword_section = keyword_section + f"<div class=\"keywordBlock border\">"
    keyword_section = keyword_section + f"<h1>Recipes by Cuisine</h1>"
    keyword_section = keyword_section + f"<div class=\"keywordContainer\">"
    outputs = 0
    for key, values in get_sorted_keywords(cuisine_map).items():
        file_name = key.lower().replace(" ", "_")
        link = format_link(f"{directory_path}/keywords/{file_name}.html")
        keyword_section = keyword_section + f"<div class=\"keywords border\"><a href=\"{link}\"><p>{key} ({len(values)})</p></a></div>"
        outputs = outputs + 1
        if (outputs == limit):
            break
    keyword_section = keyword_section + f"</div>"
    keyword_section = keyword_section + f"</div>"
    # Add category pages
    keyword_section = keyword_section + f"<div class=\"keywordBlock border\">"
    keyword_section = keyword_section + f"<h1>Recipes by Category</h1>"
    keyword_section = keyword_section + f"<div class=\"keywordContainer\">"
    outputs = 0
    for key, values in get_sorted_keywords(category_map).items():
        file_name = key.lower().replace(" ", "_")
        link = format_link(f"{directory_path}/keywords/{file_name}.html")
        keyword_section = keyword_section + f"<div class=\"keywords border\"><a href=\"{link}\"><p>{key} ({len(values)})</p></a></div>"
        outputs = outputs + 1
        if (outputs == limit):
            break
    keyword_section = keyword_section + f"</div>"
    keyword_section = keyword_section + f"</div>"
    keyword_section = keyword_section + f"</div>"

    return keyword_section

def return_basic_stats(stat_map, name, title):
    return_string = ""

    single_items = 0
    shortest_item = "aaaaaaaaaaaaaaa"
    longest_item = "a"
    most_common_item = ["", 0]
    for k,v in stat_map.items():
        if len(v) < 2:
            single_items = single_items + 1
        if len(k) < len(shortest_item):
            shortest_item = k
        if len(k) > len(longest_item):
            longest_item = k
        if len(v) > most_common_item[1]:
            most_common_item[0] = k
            most_common_item[1] = len(v)
    return_string = return_string + f"<div class=\"keywordBlock border\">"
    return_string = return_string + f"<h1 class=\"\">{title}</h1>"
    return_string = return_string + f"<div class=\"keywordContainer\">"
    return_string = return_string + f"<div class=\"keywords border\"><p>{len(stat_map)} {name}</p></div>"
    return_string = return_string + f"<div class=\"keywords border\"><p>{single_items} {name} With 1 Recipe</p></div>"
    return_string = return_string + f"<div class=\"keywords border\"><a href=\"{get_keyword_link(shortest_item)}\"><p>Min Name: {shortest_item}</p></a></div>"
    return_string = return_string + f"<div class=\"keywords border\"><a href=\"{get_keyword_link(longest_item)}\"><p>Max Name: {longest_item}</p></a></div>"
    return_string = return_string + f"<div class=\"keywords border\"><a href=\"{get_keyword_link(most_common_item[0])}\"><p>Most Common: {most_common_item[0]} ({most_common_item[1]})</p></a></div>"
    return_string = return_string + f"</div>"
    return_string = return_string + f"</div>"

    return return_string

def return_shared_note_html(folder, recipe_folder):
    note_data = shared_notes[folder]
    html = ""

    html = html + f"<div style=\"min-width: fit-content;\" class=\"recipeComponent border\">"
    html = html + f"<h2 class=\"removeOffsetTop\">{note_data['description']}</h2>"
    html = html + f"<ul>"
    for note in note_data['notes']:
        html = html + f"<li>{note}</li>"
    html = html + f"</ul>"

    html = html + f"<p class=\"removeOffsetHeight\">Other recipes sharing these notes:</p>"
    html = html + f"<div class=\"keywordContainer\">"
    for recipe in shared_note_map[folder]:
        if recipe_folder != recipe['folder']:
            html = html + f"<div class=\"keywords border\"><a href=\"{get_recipe_link(recipe['folder'])}\"><p>{recipe['name']}</p></a></div>"
    html = html + f"</div>"

    html = html + f"</div>"

    return html

def return_related_recipes_html(related_recipes):
    html = ""

    html = html + f"<div style=\"min-width: fit-content;\" class=\"recipeComponent border\">"
    html = html + f"<h2 class=\"removeOffsetTop\">Related Recipes</h2>"

    html = html + f"<div class=\"keywordContainer\">"
    for recipe in related_recipes:
        html = html + f"<div class=\"keywords border\"><a href=\"{get_recipe_link(recipe)}\"><p>{get_recipe(recipe)['name']}</p></a></div>"
    html = html + f"</div>"

    html = html + f"</div>"

    return html