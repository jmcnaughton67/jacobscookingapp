from .global_variables import *

def format_link(link):
    if remove_html_extension:
        root_index_link = f"{directory_path}/index.html"
        if link == root_index_link:
            return directory_path if directory_path else "/"

        if link.endswith('/index.html'):
             if link.split('/')[-1] == 'index.html':
                 return link[:-10]

        if link.endswith('.html'):
            return link[:-5]

        return link
    else:
        return link
    

def get_keyword_link(keyword):
    keyword_link = keyword.lower().replace(" ", "_")
    keyword_link = format_link(f"{directory_path}/keywords/{keyword_link}.html")
    return keyword_link

def get_recipe_link(recipe_name):
    recipe_link = recipe_name.lower().replace(" ", "_")
    recipe_link = format_link(f"{directory_path}/{recipe_link}/{recipe_link}.html")
    return recipe_link