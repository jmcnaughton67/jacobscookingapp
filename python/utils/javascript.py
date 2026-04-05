from .global_variables import *
from .link_helpers import *

def get_search_js():
    return f"""

recipes = {small_recipes};
ingredients = {small_ingredient_map};
cuisines = {small_cuisine_map};
categories = {small_category_map};
filters = [];

function stringContainsAll(mainString) {{
    const lowerMainString = mainString.toLowerCase();
    if (!filters || filters.length === 0) {{
        return true;
    }}
    for (let i = 0; i < filters.length; i++) {{
        if (!lowerMainString.includes(filters[i].toLowerCase())) {{
            return false;
        }}
    }}
    return true;
}}

function formatJsLink(basePath, itemName, isKeyword = false) {{
    const removeHtmlExtension = "{remove_html_extension}";
    let link;
    if (isKeyword) {{
        link = `${{basePath}}/keywords/${{itemName.split(' ').join('_').toLowerCase()}}`;
    }} else {{
        link = `${{basePath}}/${{itemName}}/`;
    }}
    if (removeHtmlExtension === "False") {{
        link += ".html";
    }}
    return link;
}}

function search() {{
    const searchText = document.getElementById("searchInput").value.toLowerCase(); 

    let output = "";
    let outputs = 0;
    for (let i = 0; i < recipes.length; i++) {{
        const jsonObject = recipes[i];
        const combinedText = (jsonObject.name || "") + (jsonObject.recipeCuisine || "") + (jsonObject.recipeCategory || "") + (jsonObject.ingredientKeywords || []).toString();

        if (searchText === '' || combinedText.toLowerCase().includes(searchText)) {{
            if (stringContainsAll(combinedText)) {{ 
                const recipeLink = formatJsLink('{directory_path}', jsonObject.folder, false);
                // Original HTML structure
                output += `<div class="keywords noBG"><div class="keywords border"><a href="${{recipeLink}}"><p>${{jsonObject.name}}</p></a></div></div>`;
                outputs++;
            }}
        }}
        if (outputs >= 9) {{ break; }}
    }}
    document.getElementById("recipeResults").innerHTML = (output === "") ? '<div class="keywords border"><p>No Results</p></div>' : output;


    output = "";
    outputs = 0;
    for (let i = 0; i < ingredients.length; i++) {{
        const keyword = ingredients[i];
        if (typeof keyword === 'string' && (searchText === '' || keyword.toLowerCase().includes(searchText))) {{
             const keywordLink = formatJsLink('{directory_path}', keyword, true);
             output += `<div class="keywords noBG"><div class="keywords border"><a href="${{keywordLink}}"><p>${{keyword}}</p></a></div><div class="keywords keywordSidecar border"><a onClick="addFilter('${{keyword}}')"><p>+</p></a></div></div>`;
             outputs++;
        }}
        if (outputs >= 16) {{ break; }}
    }}
    document.getElementById("ingredientResults").innerHTML = (output === "") ? '<div class="keywords border"><p>No Results</p></div>' : output;

    // Cuisines
    output = "";
    outputs = 0;
    for (let i = 0; i < cuisines.length; i++) {{
        const keyword = cuisines[i];
         if (typeof keyword === 'string' && (searchText === '' || keyword.toLowerCase().includes(searchText))) {{
            const keywordLink = formatJsLink('{directory_path}', keyword, true);
            output += `<div class="keywords noBG"><div class="keywords border"><a href="${{keywordLink}}"><p>${{keyword}}</p></a></div><div class="keywords keywordSidecar border"><a onClick="addFilter('${{keyword}}')"><p>+</p></a></div></div>`;
            outputs++;
         }}
        if (outputs >= 9) {{ break; }}
    }}
    document.getElementById("cuisineResults").innerHTML = (output === "") ? '<div class="keywords border"><p>No Results</p></div>' : output;

    // Categories
    output = "";
    outputs = 0;
    for (let i = 0; i < categories.length; i++) {{
        const keyword = categories[i];
         if (typeof keyword === 'string' && (searchText === '' || keyword.toLowerCase().includes(searchText))) {{
            const keywordLink = formatJsLink('{directory_path}', keyword, true);
            output += `<div class="keywords noBG"><div class="keywords border"><a href="${{keywordLink}}"><p>${{keyword}}</p></a></div><div class="keywords keywordSidecar border"><a onClick="addFilter('${{keyword}}')"><p>+</p></a></div></div>`;
            outputs++;
         }}
        if (outputs >= 9) {{ break; }}
    }}
    document.getElementById("categoryResults").innerHTML = (output === "") ? '<div class="keywords border"><p>No Results</p></div>' : output;
}}


function addFilter(filter) {{
    filters.push(filter);
    let output = "";
    for (let i = 0; i < filters.length; i++) {{
         const keywordLink = formatJsLink('{directory_path}', filters[i], true);
         output += `<div class="keywords noBG"><div class="keywords border"><a href="${{keywordLink}}"><p>${{filters[i]}}</p></a></div><div class="keywords keywordSidecar border"><a onClick="removeFilter('${{filters[i]}}')"><p>-</p></a></div></div>`;
    }}
    document.getElementById("filters").innerHTML = output;
    search();
}}

function removeFilter(filter) {{
    filters = filters.filter(item => item !== filter);
    let output = "";
    for (let i = 0; i < filters.length; i++) {{
         const keywordLink = formatJsLink('{directory_path}', filters[i], true);
         output += `<div class="keywords noBG"><div class="keywords border"><a href="${{keywordLink}}"><p>${{filters[i]}}</p></a></div><div class="keywords keywordSidecar border"><a onClick="removeFilter('${{filters[i]}}')"><p>-</p></a></div></div>`;
    }}
    if (output === "") {{
        output = '<div class="keywords border"><p>No Filters Selected</p></div>';
    }}
    document.getElementById("filters").innerHTML = output;
    search();
}}
"""

def get_random_js():
    return f"""
randomRecipes = {smallest_recipes};
function random() {{
    const removeHtmlExtension = "{remove_html_extension}";
    const url = window.location.href;
    const parts = url.split("/");
    const folderName = parts[parts.length - 1];
    const pageName = folderName.replace(".html", "");

    rand = Math.floor(Math.random() * randomRecipes.length);

    if(randomRecipes[rand] === pageName) {{
        random();
    }} else {{
        if (removeHtmlExtension === "True") {{
            document.querySelector(".keywords.random.border > a").href = '/' + randomRecipes[rand] + '/'
        }} else {{
            document.querySelector(".keywords.random.border > a").href = '/' + randomRecipes[rand] + '/index.html'
        }}
    }}
}} 


function sharePage() {{
  const shareData = {{
    title: "Cooking With Spud",
    text: document.getElementsByTagName("title")[0].innerHTML,
    url: window.location.href,
  }};
  try {{
    navigator.share(shareData);
  }} catch (err) {{
    resultPara.textContent = `Error: ${{err}}`;
  }}
}};
"""
# Prefil search box code, dont touch k thx

# window.addEventListener("load", (event) => {{
#     // Reverted: No check if element exists
#     const searchPlaceholders = ["garlic", "chili", "onion", "beef"];
#     const randomIndex = Math.floor(Math.random() * searchPlaceholders.length);
#     document.getElementById("searchInput").value = searchPlaceholders[randomIndex];
#     search();
# }});