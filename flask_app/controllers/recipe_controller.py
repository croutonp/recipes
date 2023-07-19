from flask_app import app
from flask import flash, render_template, request, redirect, session
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

@app.route('/recipes')
def dashboard():
    
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
        }
    
    logged_user = User.get_by_id(data)
    all_recipes = Recipe.get_all()
    return render_template('recipes.html',logged_user=logged_user, all_recipes=all_recipes)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create_recipe.html')

@app.route('/recipes/create', methods = ['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.is_valid(request.form):
        return redirect('/recipes/new')
    recipe_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Recipe.create(recipe_data)
    return redirect('/recipes')