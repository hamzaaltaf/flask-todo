from flask import Flask, render_template, request, url_for, redirect, flash
from pymongo import MongoClient
from flask_cors import CORS
from bson.objectid import ObjectId
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SelectField, PasswordField, SubmitField


app = Flask(__name__)
app.config['SECRET_KEY'] = "adskbajnbkabk7821"
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos
movies = db.movies
csrf = CSRFProtect(app)
CORS(app)


@app.route('/')
def index():
	return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/home', methods = ['GET'])
def home():
	return "Hey I am home page"

""" 
    This function grabs the list of movies from the mongoDB collection 
    and passes on to the view under the name of movies
"""
@app.route('/list_movies')
def list_movies():
    movies_list = list(movies.find({}, {'name': 1, 'plot': 1, 'genre': 1, '_id': 1}))
    result = []
    for movie in movies_list:
        result.append({"id": str(movie["_id"]), "plot": movie["plot"], "genre": movie["genre"], "name": movie["name"]})
    if movies_list:
        return render_template("movies/index.html", movies = result)
    else:
        return render_template("movies/index.html", movies = None)


"""
    This function is to show the form to create movies
"""
@app.route('/new_movie', methods=["GET", "POST"])
def new_movie():
    form  = MovieForm()
    print("WE ARE IN REQUEST", request)
    if request.method == "POST":
        form  = MovieForm(request.form)
        print("WE ARE IN POST", form.validate_on_submit())
        if form.validate_on_submit():
            new_movie = movies.insert_one({"name": form.name.data, "plot": form.plot.data, "genre": form.genre.data})
            if new_movie.inserted_id:
                print("RECORD CREATED")
                return redirect(url_for('list_movies'))
            else:
                flash("Data is invalid")
                return redirect(url_for('new_movie'))
        else:
            print(form.errors)
            flash(form.errors)
            return redirect(url_for('new_movie'))
    else:
        return render_template('movies/new.html', form=form)

@app.route("/edit_movie/<string:id>", methods=["GET", "POST"])
def edit_movie(id):
    movie = movies.find_one({"_id": ObjectId(id)})
    print("HERE IS MOVIE", request)
    if request.method == "POST" and request.form['_method'] == 'PUT':
        form = MovieForm(request.form)
        movie = movies.find_one_and_update({"_id": ObjectId(id)},
            {'$set': {"name": form.name.data, "plot": form.plot.data, "genre": form.genre.data}})
        if movie:
            flash(["Movie has been updated successfully"])
            return redirect(url_for('list_movies'))
        else:
            flash(movie.errors)
            return render_template("movies/edit.html", form=form)
    else:
        if movie:
            form = MovieForm()
            form.name.data = movie.get('name')
            form.plot.data = movie.get('plot')
            form.genre.data = movie.get('genre')
            print("HERE IS FORM", form)
            return render_template("movies/edit.html", form=form)
            
        else:
            flash("Invalid ID")
    
@app.route("/delete_movie/<string:id>", methods = ["DELETE", "GET"])
def delete_movie(id):
    movie = movies.find_one_and_delete({"_id": ObjectId(id)})
    if movie:
        flash("Movie has been deleted successfully")
    else:
        flash("Movie was not deleted")
    return redirect(url_for('list_movies'))


@app.route('/api/v1/create_post', methods = ['POST'])
def create_post():
    print("I AM INSIDE THE CREATE POST", request.json)
    data = request.json
    if request.method == "POST":
        todo = todos.insert_one({"title": data['title'], "description": data['description']})
        if todo.inserted_id:
            return {"success": True}
        else:
            return {"success": False}
        
		
@app.route('/api/v1/list_todos', methods = ['GET'])
def list_todos():
    all_todos = list(todos.find({}, {'_id': 1, 'title': 1, 'description': 1}))
    result = []
    for todo in all_todos:
        result.append({"id": str(todo['_id']), 'title': todo['title'], 'description': todo['description']})
    # result = all_todos.map(lambda item: {id: item['_id'], 'title': item['title'], 'description': item['description']}, all_todos)
    print("here is what I am sending abck to the user", result)
    return {"success": True, "todos": result}
		

@app.route('/api/v1/delete_todo', methods = ["DELETE"])
def delete_todo():
    if request.method == "DELETE":
        data = request.get_json()
        todo_id = data.get('id')
        todo  = todos.find_one_and_delete({'_id': ObjectId(todo_id)})
        if todo:
            return {"success": True}
        else:
            return {"success": False}


class MovieForm(FlaskForm):
    name = StringField(label = 'Movie Name...')
    plot = StringField(label = 'Plot...')
    genre = StringField(label = 'Genre...')
    submit = SubmitField(label='Create Movie')


if __name__ == '__main__':
	app.run(debug=True)
	

# in order to change the data type of the input use float(input())
# by default python taks the input in form of string

