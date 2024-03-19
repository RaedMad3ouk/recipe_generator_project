from flask import Blueprint, render_template, request, redirect, url_for
import requests
from urllib.parse import unquote

views = Blueprint('views', __name__)
generate_bp = Blueprint('generate', __name__)

API_KEY = '269b4c5840c44b08af5ff4c655834664'


@views.route('/')
def home():
    return render_template('home.html')


@generate_bp.route('/generate_recipe', methods=['GET', 'POST'])
def generate_recipe():
    if request.method == 'POST':
        query = request.form.get('search_query', '')
        recipes = search_recipes(query)
        return render_template('recipe.html', recipes=recipes, search_query=query)

    elif request.method == 'GET':
        search_query = request.args.get('search_query', '')
        decoded_search_query = unquote(search_query)
        recipes = search_recipes(decoded_search_query)
        return render_template('recipe.html', recipes=recipes, search_query=decoded_search_query)



def search_recipes(query):
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    return []


@generate_bp.route('/generate_recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    search_query = request.args.get('search_query', '')
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    return "Recipe not found", 404
