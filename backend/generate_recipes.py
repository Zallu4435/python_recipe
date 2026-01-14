
import json
import os

recipes = [
    {
        "id": 1,
        "name": "Chicken Biryani",
        "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Chicken", "Basmati Rice", "Onion", "Yogurt", "Ginger Garlic Paste", "Biryani Masala"],
        "hints": ["Main protein in Indian curries", "Long aromatic rice variety", "Turns golden when fried", "Adds sour creaminess", "Used in almost all Indian gravies", "The magic spice mix"]
    },
    {
        "id": 2,
        "name": "Spaghetti Carbonara",
        "image": "https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Spaghetti", "Eggs", "Pecorino Romano", "Guanciale", "Black Pepper"],
        "hints": ["Long, thin cylindrical pasta", "Binder for the sauce", "Hard, salty sheep cheese", "Cured pork jowl", "Spicy dust"]
    },
    {
        "id": 3,
        "name": "Classic Burger",
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Beef Patty", "Burger Bun", "Lettuce", "Tomato", "Cheese", "Ketchup"],
        "hints": ["Ground meat disc", "Bread holder", "Green crunchy leaf", "Red juicy slice", "Melty dairy slice", "Red tomato sauce"]
    },
    {
        "id": 4,
        "name": "Pancakes",
        "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Flour", "Milk", "Eggs", "Baking Powder", "Maple Syrup", "Butter"],
        "hints": ["White powdery base", "Dairy liquid", "Protein binders", "Makes it fluffy", "Sweet tree sap", "Golden fat"]
    },
    {
        "id": 5,
        "name": "Caesar Salad",
        "image": "https://images.unsplash.com/photo-1546793665-c74683f339c1?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Romaine Lettuce", "Croutons", "Parmesan Cheese", "Caesar Dressing", "Lemon Juice"],
        "hints": ["Crispy green leaves", "Crunchy bread cubes", "Aged hard cheese", "Creamy anchovy sauce", "Sour citrus squeeze"]
    },
    {
        "id": 6,
        "name": "Tacos al Pastor",
        "image": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Corn Tortillas", "Marinated Pork", "Pineapple", "Onion", "Cilantro"],
        "hints": ["Soft corn discs", "Red spice meat", "Sweet yellow fruit", "Sharp bulb", "Green herbal garnish"]
    },
    {
        "id": 7,
        "name": "Sushi Rolls",
        "image": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Sushi Rice", "Nori", "Fresh Fish", "Cucumber", "Soy Sauce", "Wasabi"],
        "hints": ["Sticky vinegared grain", "Dried seaweed sheet", "Raw ocean protein", "Green cool crunch", "Salty dipping liquid", "Spicy green paste"]
    },
    {
        "id": 8,
        "name": "Butter Chicken",
        "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Chicken", "Butter", "Tomato Puree", "Cream", "Garam Masala"],
        "hints": ["Bird meat", "Yellow dairy fat", "Red soup base", "Rich white liquid", "Warm spice blend"]
    },
    {
        "id": 9,
        "name": "French Toast",
        "image": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Bread", "Eggs", "Milk", "Cinnamon", "Vanilla Extract"],
        "hints": ["Sliced loaf", "Shell contents", "Cow juice", "Brown spice dust", "Sweet essence"]
    },
    {
        "id": 10,
        "name": "Guacamole",
        "image": "https://images.unsplash.com/photo-1604908177453-7462950a6a3b?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Avocado", "Lime", "Onion", "Cilantro", "Tomato", "Salt"],
        "hints": ["Green creamy fruit", "Green citrus", "White crunchy dice", "Fresh green herb", "Red juicy dice", "Mineral seasoning"]
    },
    {
        "id": 11,
        "name": "Margherita Pizza",
        "image": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Fresh Basil", "Olive Oil"],
        "hints": ["Discoid flour base", "Red spread", "White melting balls", "Aromatic Italian leaf", "Green gold liquid"]
    },
    {
        "id": 12,
        "name": "Pad Thai",
        "image": "https://images.unsplash.com/photo-1559314809-0d155014e29e?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Rice Noodles", "Shrimp", "Tofu", "Peanuts", "Bean Sprouts", "Tamarind Sauce"],
        "hints": ["Flat translucent strips", "Pink curled seafood", "Soy bean curd", "Crunchy legume", "White crunchy shoots", "Sour brown sauce"]
    },
    {
        "id": 13,
        "name": "Beef Stroganoff",
        "image": "https://images.unsplash.com/photo-1553647317-062e2195dfb4?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Beef Strips", "Mushrooms", "Onion", "Sour Cream", "Beef Broth"],
        "hints": ["Red meat slices", "Fungi", "Tear-inducing bulb", "Tangy thick dairy", "Meat soup liquid"]
    },
    {
        "id": 14,
        "name": "Greek Salad",
        "image": "https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Cucumber", "Tomato", "Kalamata Olives", "Feta Cheese", "Red Onion", "Oregano"],
        "hints": ["Cool green cylinder", "Red fruit veg", "Dark salty drupes", "Brined white cheese", "Purple pungency", "Dried herb sprinkles"]
    },
    {
        "id": 15,
        "name": "Tom Yum Soup",
        "image": "https://images.unsplash.com/photo-1548943487-a2e4e43b485c?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Shrimp", "Mushrooms", "Lemongrass", "Kaffir Lime Leaves", "Galangal", "Chili"],
        "hints": ["Sea prawns", "Soft fungi", "Citrusy stalk", "Double-lobed leaves", "Thai ginger", "Hot red pod"]
    },
    {
        "id": 16,
        "name": "Chocolate Chip Cookies",
        "image": "https://images.unsplash.com/photo-1499636136210-6f4ee9155bb9?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Flour", "Butter", "Sugar", "Brown Sugar", "Eggs", "Chocolate Chips"],
        "hints": ["Wheat powder", "Solid dairy fat", "Sweet crystals", "Molasses sweet sand", "Binding agent", "Cocoa morsels"]
    },
    {
        "id": 17,
        "name": "Risotto",
        "image": "https://images.unsplash.com/photo-1476124369491-e7addf5db371?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Arborio Rice", "Chicken Broth", "White Wine", "Onion", "Butter", "Parmesan"],
        "hints": ["Starchy short grain", "Savory liquid stock", "Alcoholic grape juice", "Flavor base bulb", "Creamy finisher", "Sharp grated cheese"]
    },
    {
        "id": 18,
        "name": "Falafel",
        "image": "https://images.unsplash.com/photo-1593001874117-c99c800e3eb7?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Chickpeas", "Parsley", "Cilantro", "Garlic", "Cumin", "Flour"],
        "hints": ["Garbanzo beans", "Green leafy herb", "Another green herb", "Vampire repellent", "Earthy spice", "Binding powder"]
    },
    {
        "id": 19,
        "name": "Mac and Cheese",
        "image": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Macaroni", "Cheddar Cheese", "Milk", "Butter", "Flour"],
        "hints": ["Curved pasta tubes", "Orange sharp dairy", "White liquid", "Yellow fat", "Roux powder"]
    },
    {
        "id": 20,
        "name": "Ratatouille",
        "image": "https://images.unsplash.com/photo-1572453800999-e8d2d1589b7c?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Eggplant", "Zucchini", "Bell Pepper", "Tomato", "Onion", "Herbs de Provence"],
        "hints": ["Purple veggie", "Green summer squash", "Colorful hollow veg", "Sauce fruit", "Layered bulb", "French dried mix"]
    },
    {
        "id": 21,
        "name": "Pesto Pasta",
        "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Pasta", "Basil", "Pine Nuts", "Parmesan", "Garlic", "Olive Oil"],
        "hints": ["Wheat shapes", "Sweet green herb", "Small creamy seeds", "Hard cheese", "Pungent clove", "Liquid fat"]
    },
    {
        "id": 22,
        "name": "Chicken Noodle Soup",
        "image": "https://images.unsplash.com/photo-1547592166-23acbe3a624b?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Chicken", "Egg Noodles", "Carrots", "Celery", "Onion", "Chicken Broth"],
        "hints": ["Poultry meat", "Ribbon pasta", "Orange root", "Green crunchy stalk", "White savory bulb", "Golden liquid"]
    },
    {
        "id": 23,
        "name": "Fish and Chips",
        "image": "https://images.unsplash.com/photo-1579208575657-c529684e8883?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["White Fish", "Potatoes", "Flour", "Beer", "Tartar Sauce"],
        "hints": ["Cod or Haddock", "Starchy tuber", "Batter base", "Fizzy alcohol", "Creamy dip"]
    },
    {
        "id": 24,
        "name": "Beef Tacos",
        "image": "https://images.unsplash.com/photo-1613514785940-daed07799d9b?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Ground Beef", "Taco Shells", "Lettuce", "Cheese", "Salsa"],
        "hints": ["Minced red meat", "Crunchy corn boat", "Shredded green", "Shredded dairy", "Spicy tomato sauce"]
    },
    {
        "id": 25,
        "name": "Shakshuka",
        "image": "https://images.unsplash.com/photo-1590412200988-a436970781fa?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Eggs", "Tomatoes", "Bell Pepper", "Onion", "Cumin", "Paprika"],
        "hints": ["Poached protein", "Red sauce base", "Red crunchy veg", "Sauté starter", "Warm spice", "Red mild powder"]
    },
    {
        "id": 26,
        "name": "Caprese Salad",
        "image": "https://images.unsplash.com/photo-1529312266912-b33cf6227e2f?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Mozzarella", "Tomato", "Basil", "Balsamic Glaze", "Olive Oil"],
        "hints": ["Soft cheese ball", "Red slices", "Green aromatic leaf", "Sweet dark vinegar", "Drizzle fat"]
    },
    {
        "id": 27,
        "name": "Gnocchi",
        "image": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Potatoes", "Flour", "Egg", "Salt"],
        "hints": ["Mashed tuber", "White powder", "Binding yolk", "Flavor crystals"]
    },
    {
        "id": 28,
        "name": "Vegetable Stir Fry",
        "image": "https://images.unsplash.com/photo-1527515545081-5db817172677?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Broccoli", "Carrots", "Snap Peas", "Soy Sauce", "Ginger", "Garlic"],
        "hints": ["Mini trees", "Orange sticks", "Green pods", "Salty dark sauce", "Spicy root", "Pungent clove"]
    },
    {
        "id": 29,
        "name": "Lasagna",
        "image": "https://images.unsplash.com/photo-1574868233965-2748b6c167b6?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Lasagna Noodles", "Ground Beef", "Tomato Sauce", "Ricotta", "Mozzarella", "Parmesan"],
        "hints": ["Wide pasta sheets", "Meat layer", "Red layer", "Creamy cheese layer", "Melty top", "Sprinkle cheese"]
    },
    {
        "id": 30,
        "name": "Hummus",
        "image": "https://images.unsplash.com/photo-1637949385162-e416fb15b2ce?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Chickpeas", "Tahini", "Lemon Juice", "Garlic", "Olive Oil", "Cumin"],
        "hints": ["Blending bean", "Sesame paste", "Citrus acid", "Flavor bulb", "Smooth fat", "Earthy spice"]
    },
    {
        "id": 31,
        "name": "Pho",
        "image": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Rice Noodles", "Beef Broth", "Beef Slices", "Bean Sprouts", "Basil", "Star Anise"],
        "hints": ["Soup strings", "Simmered liquid", "Thin meat", "Crunchy garnish", "Herbal garnish", "Licorice spice"]
    },
    {
        "id": 32,
        "name": "Fried Rice",
        "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Cooked Rice", "Eggs", "Peas", "Carrots", "Soy Sauce", "Green Onion"],
        "hints": ["Leftover grain", "Scramble bits", "Green dots", "Orange cubes", "Brown seasoning", "Green tube garnish"]
    },
    {
        "id": 33,
        "name": "Gazpacho",
        "image": "https://images.unsplash.com/photo-1598000456637-b844976cf455?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Tomatoes", "Cucumber", "Bell Pepper", "Onion", "Garlic", "Sherry Vinegar"],
        "hints": ["Ripe red fruit", "Cool veg", "Green crunch", "Sharp bulb", "Spicy bulb", "Spanish acid"]
    },
    {
        "id": 34,
        "name": "Brownies",
        "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Chocolate", "Butter", "Sugar", "Eggs", "Flour", "Cocoa Powder"],
        "hints": ["Dark melting bar", "Fatty base", "Sweetener", "Structure builder", "Wheat base", "Bitter dust"]
    },
    {
        "id": 35,
        "name": "Omelette",
        "image": "https://images.unsplash.com/photo-1510614528947-90db32631235?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Eggs", "Cheese", "Ham", "Peppers", "Butter", "Salt"],
        "hints": ["Whisked protein", "Melty filling", "Pink meat", "Veggie crunch", "Pan grease", "Seasoning"]
    },
    {
        "id": 36,
        "name": "Chicken Curry",
        "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Chicken", "Coconut Milk", "Curry Powder", "Onion", "Ginger", "Garlic"],
        "hints": ["Poultry pieces", "Tropical cream", "Yellow spice mix", "Sauté base", "Spicy root", "White cloves"]
    },
    {
        "id": 37,
        "name": "Cheesecake",
        "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Cream Cheese", "Graham Crackers", "Sugar", "Butter", "Vanilla"],
        "hints": ["Smooth cheese block", "Crust ingredient", "Sweet things", "Crust binder", "Extract flavor"]
    },
    {
        "id": 38,
        "name": "Miso Soup",
        "image": "https://images.unsplash.com/photo-1547592166-23acbe3a624b?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Miso Paste", "Dashi", "Tofu", "Wakame", "Green Onion"],
        "hints": ["Fermented bean paste", "Fish stock", "Soy cubes", "Seaweed bits", "Scallion garnish"]
    },
    {
        "id": 39,
        "name": "Cobb Salad",
        "image": "https://images.unsplash.com/photo-1512852939750-1347028163f7?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Lettuce", "Chicken", "Bacon", "Hard Boiled Eggs", "Avocado", "Blue Cheese"],
        "hints": ["Green bed", "Grilled bird", "Crispy pork", "Yellow yolk spheres", "Creamy green fruit", "Funky cheese crumble"]
    },
    {
        "id": 40,
        "name": "Deviled Eggs",
        "image": "https://images.unsplash.com/photo-1595055620959-19b6a18288b4?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Eggs", "Mayonnaise", "Mustard", "Paprika", "Vinegar"],
        "hints": ["Boiled whites", "Creamy emulsion", "Yellow tang", "Red dust", "Acid splash"]
    },
    {
        "id": 41,
        "name": "Egg Salad",
        "image": "https://images.unsplash.com/photo-1541014741259-de529411b96a?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Eggs", "Mayonnaise", "Mustard", "Celery", "Green Onion"],
        "hints": ["Chopped boiled", "Sandwich binder", "Tangy yellow", "Crunchy bits", "Onion bits"]
    },
    {
        "id": 42,
        "name": "Banana Bread",
        "image": "https://images.unsplash.com/photo-1603532648955-46d6cf405813?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Bananas", "Flour", "Sugar", "Butter", "Eggs", "Baking Soda"],
        "hints": ["Ripe spotted fruit", "Loaf base", "Sweet", "Moist fat", "Binder", "Riser"]
    },
    {
        "id": 43,
        "name": "Beef Stew",
        "image": "https://images.unsplash.com/photo-1534939561126-855f8665ed09?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Beef Chuck", "Potatoes", "Carrots", "Beef Broth", "Red Wine", "Thyme"],
        "hints": ["Tough meat cubes", "Root chunks", "Orange chunks", "Brown liquid", "Rich alcohol", "Tiny leaves"]
    },
    {
        "id": 44,
        "name": "Quesadilla",
        "image": "https://images.unsplash.com/photo-1618040996337-56904b7850b9?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Tortilla", "Cheese", "Chicken", "Salsa", "Sour Cream"],
        "hints": ["Flour wrapper", "Melting glue", "Filling meat", "Dip", "White cool dip"]
    },
    {
        "id": 45,
        "name": "Smoothie Bowl",
        "image": "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Frozen Berries", "Banana", "Yogurt", "Granola", "Honey"],
        "hints": ["Icy fruits", "Thickener fruit", "Creamy base", "Crunchy topping", "Bee syrup"]
    },
    {
        "id": 46,
        "name": "Hot Dog",
        "image": "https://images.unsplash.com/photo-1627054248849-df632128713d?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Sausage", "Bun", "Ketchup", "Mustard", "Relish"],
        "hints": ["Meat tube", "Bread holder", "Red sauce", "Yellow sauce", "Pickled bits"]
    },
    {
        "id": 47,
        "name": "Chili Con Carne",
        "image": "https://images.unsplash.com/photo-1549419134-22b9b2229e61?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Ground Beef", "Kidney Beans", "Tomatoes", "Chili Powder", "Onion"],
        "hints": ["Minced meat", "Red legumes", "Sauce base", "Spicy dust", "Sauté veg"]
    },
    {
        "id": 48,
        "name": "Tiramisu",
        "image": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Ladyfingers", "Mascarpone", "Coffee", "Cocoa Powder", "Eggs", "Sugar"],
        "hints": ["Dry biscuits", "Creamy Italian cheese", "Espresso soak", "Dusting on top", "Custard base", "Sweetness"]
    },
    {
        "id": 49,
        "name": "Bruschetta",
        "image": "https://images.unsplash.com/photo-1572695157363-bc31c5598db4?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Baguette", "Tomatoes", "Basil", "Garlic", "Olive Oil", "Balsamic Vinegar"],
        "hints": ["Toasted slices", "Diced red fruit", "Green herb garnish", "Rubbed flavor", "Drizzle", "Dark splash"]
    },
    {
        "id": 50,
        "name": "Lemonade",
        "image": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&q=80&w=800",
        "ingredients": ["Lemons", "Sugar", "Water", "Ice", "Mint"],
        "hints": ["Sour yellow fruit", "Sweetener", "Hydration", "Cold cubes", "Garnish leaf"]
    }
]

with open('backend/data/recipes.json', 'w') as f:
    json.dump(recipes, f, indent=4)

print("Generated recipes!")
