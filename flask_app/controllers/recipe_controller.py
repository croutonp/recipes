from flask_app import app
from flask import flash, render_template, request, redirect, session
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

#############
# RECIPES PAGE
#############


@app.route("/recipes")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}

    logged_user = User.get_by_id(data)
    all_recipes = Recipe.get_all()
    return render_template(
        "recipes.html", logged_user=logged_user, all_recipes=all_recipes
    )


#####################
# CREATE RECIPE ROUTES
#####################


@app.route("/recipes/new")
def new_recipe():
    if "user_id" not in session:
        return redirect("/")
    return render_template("create_recipe.html")


@app.route("/recipes/create", methods=["POST"])
def create_recipe():
    if "user_id" not in session:
        return redirect("/")
    if not Recipe.is_valid(request.form):
        return redirect("/recipes/new")
    recipe_data = {**request.form, "user_id": session["user_id"]}
    Recipe.create(recipe_data)
    return redirect("/recipes")

###################
#EDIT RECIPE ROUTES
###################

@app.route("/recipes/edit/<int:id>")
def edit_recipe_form(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id}
    one_recipe = Recipe.get_one(data)

    if one_recipe.user_id != session["user_id"]:
        flash("Don't")
        return redirect("/recipes")
    return render_template("edit_recipe.html", one_recipe=one_recipe)


@app.route("/recipes/update/<int:id>", methods=["POST"])
def update_recipe(id):
    if "user_id" not in session:
        return redirect("/")
    if not Recipe.is_valid(request.form):
        return redirect(f"/recipes/edit/{id}")
    data = {**request.form, "id": id}

    one_recipe = Recipe.get_one(data)
    if one_recipe.user_id != session["user_id"]:
        flash("Don't")
        return redirect("/recipes")
    Recipe.update(data)
    return redirect("/recipes")

#####
#VIEW
#####


@app.route("/recipes/view/<int:id>")
def view_one_recipe(id):
    user_id = session["user_id"]
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id, "user_id": session["user_id"]}
    one_recipe = Recipe.get_one(data)
    logged_user = User.get_first_name_by_user_id(data)

    return render_template("view.html", one_recipe=one_recipe, logged_user=logged_user)

#######
#DELETE
#######


@app.route("/recipes/delete/<int:id>")
def delete_recipe(id):
    data = {"id": id}
    this_recipe = Recipe.get_one(data)
    if this_recipe.user_id != session["user_id"]:
        flash("Don't")
        return redirect("/recipes")
    Recipe.delete(data)
    return redirect("/recipes")
