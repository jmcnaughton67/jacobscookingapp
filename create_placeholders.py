import json
import os

recipes = [
    {"folder": "bacon_and_leek_potato_soup", "name": "Bacon and Leek Potato Soup", "category": ["Soup"], "cuisine": ["Australian"], "keyword": "Potato"},
    {"folder": "beef_cheek_ragu", "name": "Beef Cheek Ragu", "category": ["Main Course", "Pasta Sauce"], "cuisine": ["Italian"], "keyword": "Beef"},
    {"folder": "big_potato_latke", "name": "Big Potato Latke", "category": ["Side Dish", "Snack"], "cuisine": ["Jewish", "Eastern European"], "keyword": "Potato"},
    {"folder": "breakfast_burrito", "name": "Breakfast Burrito", "category": ["Breakfast"], "cuisine": ["Mexican-American", "American"], "keyword": "Egg"},
    {"folder": "chicken_larb_lettuce_wraps", "name": "Chicken Larb Lettuce Wraps", "category": ["Main Course", "Starter"], "cuisine": ["Thai", "Lao"], "keyword": "Chicken"},
    {"folder": "chicken_quesadilla", "name": "Chicken Quesadilla with Iceberg Lettuce and Hot Sauce", "category": ["Main Course", "Snack"], "cuisine": ["Mexican-American", "American"], "keyword": "Chicken"},
    {"folder": "chicken_thigh_lemongrass_chili", "name": "Chicken Thigh Lemongrass Chilli", "category": ["Main Course"], "cuisine": ["Asian", "Thai"], "keyword": "Chicken"},
    {"folder": "jacobs_chilli_oil", "name": "Jacob's Chilli Oil", "category": ["Condiment", "Sauce"], "cuisine": ["Asian", "Chinese"], "keyword": "Chilli Flake"},
    {"folder": "chive_breadcrumb_pasta", "name": "Chive Breadcrumb Pasta", "category": ["Main Course", "Pasta"], "cuisine": ["Italian", "Italian-American"], "keyword": "Pasta"},
    {"folder": "double_chilli_cheese_smashburger", "name": "Double Chilli Cheese Smashburger", "category": ["Main Course"], "cuisine": ["American"], "keyword": "Beef"},
    {"folder": "frico", "name": "Frico", "category": ["Snack", "Starter"], "cuisine": ["Italian"], "keyword": "Parmesan"},
    {"folder": "fried_pork_belly", "name": "Fried Pork Belly with Toasted Rice", "category": ["Main Course"], "cuisine": ["Asian", "Filipino"], "keyword": "Pork"},
    {"folder": "garlic_steak_fried_rice", "name": "Garlic Steak Fried Rice", "category": ["Main Course"], "cuisine": ["Asian", "Chinese"], "keyword": "Beef"},
    {"folder": "green_goddess_salad", "name": "Green Goddess Salad", "category": ["Salad", "Side Dish"], "cuisine": ["American"], "keyword": "Herb"},
    {"folder": "kingfish_crudo", "name": "Kingfish Crudo", "category": ["Starter", "Seafood"], "cuisine": ["Italian", "Australian"], "keyword": "Kingfish"},
    {"folder": "loose_lasagna_ragu", "name": "Loose Lasagna Ragu", "category": ["Main Course", "Pasta"], "cuisine": ["Italian", "Italian-American"], "keyword": "Beef"},
    {"folder": "paella", "name": "Paella", "category": ["Main Course"], "cuisine": ["Spanish"], "keyword": "Rice"},
    {"folder": "pastel_de_nata", "name": "Pastel De Nata", "category": ["Dessert", "Baking"], "cuisine": ["Portuguese"], "keyword": "Egg"},
    {"folder": "pea_risotto", "name": "Pea Risotto", "category": ["Main Course", "Side Dish"], "cuisine": ["Italian"], "keyword": "Rice"},
    {"folder": "piri_chicken", "name": "Piri Chicken", "category": ["Main Course"], "cuisine": ["Portuguese", "African"], "keyword": "Chicken"},
    {"folder": "porchetta_broccolini_sliders", "name": "Porchetta Broccolini Sliders", "category": ["Main Course", "Snack"], "cuisine": ["Italian", "Italian-American"], "keyword": "Pork"},
    {"folder": "roasted_pumpkin_soup", "name": "Roasted Pumpkin Soup", "category": ["Soup"], "cuisine": ["Australian"], "keyword": "Pumpkin"},
    {"folder": "pulled_pork_benedict", "name": "Pulled Pork Benedict with Aleppo Hollandaise", "category": ["Breakfast", "Main Course"], "cuisine": ["American"], "keyword": "Pork"},
    {"folder": "roti_eggs", "name": "Roti Eggs with Shallots and Coriander", "category": ["Breakfast", "Snack"], "cuisine": ["Malaysian", "Asian"], "keyword": "Egg"},
    {"folder": "saag_paneer", "name": "Saag Paneer", "category": ["Main Course", "Side Dish"], "cuisine": ["Indian"], "keyword": "Paneer"},
    {"folder": "spicy_vodka_arancini", "name": "Spicy Vodka Arancini", "category": ["Starter", "Snack"], "cuisine": ["Italian", "Italian-American"], "keyword": "Rice"},
    {"folder": "spring_onion_chicken_piccata", "name": "Spring Onion Chicken Piccata", "category": ["Main Course"], "cuisine": ["Italian-American", "American"], "keyword": "Chicken"},
    {"folder": "steak_and_waffle_fries", "name": "Steak and Waffle Fries", "category": ["Main Course"], "cuisine": ["American"], "keyword": "Beef"},
    {"folder": "skirt_steak_salsa_mocha", "name": "Skirt Steak with Salsa Mocha", "category": ["Main Course"], "cuisine": ["Mexican", "Latin American"], "keyword": "Beef"},
    {"folder": "steak_waffle_fries_caramelized_onions", "name": "Steak with Waffle Fries and Caramelized Onions", "category": ["Main Course"], "cuisine": ["American"], "keyword": "Beef"},
]

base_path = "/Users/jacobmcnaughton/Projects/RecipeCMS/recipes"

for r in recipes:
    folder_path = os.path.join(base_path, r["folder"])
    os.makedirs(folder_path, exist_ok=True)

    data = {
        "@context": "https://schema.org/",
        "@type": "Recipe",
        "folder": r["folder"],
        "name": r["name"],
        "image": [f"{r['folder']}_0.jpg"],
        "author": {"@type": "Person", "name": "Jacob"},
        "datePublished": "2026-04-03",
        "lastMod": "2026-04-03",
        "description": "Coming soon.",
        "keywords": r["name"],
        "prepTime": "PT0M",
        "cookTime": "PT0M",
        "totalTime": "PT0M",
        "recipeYield": "Serves 4",
        "recipeCategory": r["category"],
        "recipeCuisine": r["cuisine"],
        "diet": [],
        "recipeIngredient": ["Coming soon"],
        "ingredientKeywords": [r["keyword"]],
        "equipment": [],
        "recipeInstructions": [
            {
                "@type": "HowToStep",
                "name": "Coming Soon",
                "url": 1,
                "text": "Recipe coming soon."
            }
        ],
        "notes": [],
        "relatedRecipes": []
    }

    json_path = os.path.join(folder_path, f"{r['folder']}.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Created: {r['name']}")

print(f"\nDone — {len(recipes)} placeholders created.")
