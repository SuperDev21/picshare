from sqlite3.dbapi2 import Cursor
from flask import Flask, render_template, g, request, redirect, send_from_directory, flash, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename
from werkzeug.utils import redirect


# variable declaration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}


app = Flask(__name__)
DATABASE = 'app.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# définir la taille max de l'images par 16 Mo
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


# function for to Connect to the Database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        return db


# function add file uploated to uploads folder
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


# #################### route sur index page 
# ************** route to display index.html as home page 
@app.route("/")
def index():
    db = get_db()
    # select all images 
    images = db.execute("SELECT img, id FROM images ORDER BY date DESC LIMIT 12")
    return render_template('index.html', all_images= images)


# ************** route to filter images by category
@app.route("/<name>")
def filtre(name):
    db = get_db()
    # select id from categories table 
    cursor = db.execute("SELECT id from categories WHERE name = (?)", [name])
    id_cat = cursor.fetchone()
    # select all images with same category
    cat_images = db.execute("SELECT img, id from images WHERE category_id = (?)\
                                order by date DESC  LIMIT 12", [id_cat[0]])
    return render_template('index.html', all_cat_images= cat_images)


################### routes of upload page
# function of allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ************** route to check the downloaded files
@app.route("/upload", methods=["GET" , "POST"])
def upload_file():
    if request.method == 'GET':
        return render_template("upload.html")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url,)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # check if the file exists and has the correct format
        if file and allowed_file(file.filename):
            # retrieve the form data
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            name = request.form.get('name')
            description = request.form.get('description')
            name_cat = request.form.get('name_cat')
            db = get_db()
            # select id from categories table
            cursor = db.execute("SELECT id from categories WHERE name = (?)", [name_cat])
            cat_id = cursor.fetchone()
            # insert a new image to images table
            cursor = db.execute("INSERT INTO images(name, img, description, category_id)\
                                Values (?, ?, ?, ?)",
                        [name, file.filename, description, cat_id[0]])
            db.commit()
            return redirect("/")
    return redirect('/upload')


# ####################################### page display.html
# ************** route for display image
@app.route("/display/<image_id>")
def display(image_id):
    db = get_db()
    # select data image from images table 
    cursor =  db.execute("SELECT * from images WHERE id = (?)", [image_id])
    images = []
    for image in cursor:
        images.append({"id": image[0], "name": image[1], "img": image[2],
                        "description": image[3], "date": image[4],
                        "vote": image[5], "category_id": image[6]})
    # select all comments with same id image
    comments = db.execute("SELECT * from comments WHERE image_id = (?) ORDER BY id DESC", [image_id])

    # ### compter les comments #### fais u paste ici meme
    count = db.execute("SELECT count(*) from comments WHERE image_id = ?", [image_id])
    comments_count = count.fetchone()
    return render_template('display.html', titre= image[1], date= image[4],
                            path= image[2], description= image[3], all_comments= comments,
                            id= image_id, count=comments_count[0])


# ************** route for add comments
@app.route("/display/<image_id>", methods=["POST"])
def add_comment(image_id):
    db = get_db()
    # recuperer les données du formulaire
    name = request.form.get('name')
    comment = request.form.get('comment')
    # recuperer id_categorie et id de la table images
    cursor = db.execute("SELECT  category_id from images WHERE id = (?)", [image_id])
    category_id = cursor.fetchone()
    # ajouter un nouveau commentaire
    cursor = db.execute("INSERT INTO comments(author, text, image_id, category_id)\
                            Values (?, ?, ?, ?)", [name, comment,
                            image_id, category_id[0]])

    db.commit()
    cursor =  db.execute("SELECT * from images WHERE id = (?)", [image_id])
    images = []
    for image in cursor:
        images.append({"id": image[0], "name": image[1], "img": image[2],
                        "description": image[3], "date": image[4],
                        "vote": image[5], "category_id": image[6]})
    comments = db.execute("SELECT * from comments WHERE image_id = (?) ORDER BY id DESC", [image_id])
    return render_template('display.html', titre= image[1], date= image[4],
                            path= image[2], description= image[3], all_comments= comments,
                            id= image_id)



# ************** route pour Next display gage 
@app.route("/next/<image_id>")
def next_display(image_id):
    db = get_db()
    cursor = db.execute("SELECT category_id from images WHERE id = (?)", [image_id])
    category_id = cursor.fetchone()
    print("cocococco", category_id)
    cursor = db.execute("SELECT * from images WHERE category_id = (?)", [category_id[0]])
    images_category = []
    new_image_id = []
    for img_category in cursor:
        images_category.append({"id": img_category[0], "name": img_category[1], "img": img_category[2],
                "description": img_category[3], "date": img_category[4],
                "vote": img_category[5], "category_id": img_category[6]})
        new_image_id.append(images_category[0])
    for index, val  in enumerate(len(new_image_id)) :
        if val == image_id:
            new_id = index + 1

    # return render_template('display.html', new= new_id)
    return redirect('/display/new_id')


# ####################################### page about.html
# ************** route for about page
@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
