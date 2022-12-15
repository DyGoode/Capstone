from flask import Blueprint, request, jsonify
from goode_grub.helpers import token_required
from goode_grub.models import db, Recipe, recipe_schema, recipes_schema


api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/getdata')
@token_required
def getdata():
    return { 'some' : 'value' }

 
@api.route('/recipes', methods = ['POST'])
@token_required
def create_recipe(current_user_token):
    title = request.json['title']
    cuisine = request.json['cuisine']
    course = request.json['course']
    servings = request.json['servings']
    user_token = current_user_token.token

    recipe = Recipe(title, cuisine, course, servings, user_token=user_token)

    db.session.add(recipe)
    db.session.commit()

    response = recipe_schema.dump(recipe)
    return jsonify(response)


@api.route('/recipes', methods = ['GET'])
@token_required
def get_recipes(current_user_token):
    owner = current_user_token.token #current_user_token == user
    recipes = Recipe.query.filter_by(user_token=owner).all()
    response = recipes_schema.dump(recipes)
    return jsonify(response)


@api.route('/recipes/<id>', methods = ['GET'])
@token_required
def get_recipe(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        recipe = Recipe.query.get(id)
        response = recipe_schema.dump(recipe)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


@api.route('/recipes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_recipe(current_user_token, id):
    recipe = Recipe.query.get(id)
    recipe.title = request.json['title']
    recipe.cuisine = request.json['cuisine']
    recipe.course = request.json['course']
    recipe.servings = request.json['servings']
    recipe.user_token = current_user_token.token

    db.session.commit()
    response = recipe_schema.dump(recipe)
    return jsonify(response)


@api.route('/recipes/<id>', methods = ['DELETE'])
@token_required
def delete_recipe(current_user_token, id):
    recipe = Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()
    response = recipe_schema.dump(recipe)
    return jsonify(response)
