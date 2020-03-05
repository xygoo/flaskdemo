from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os
app = Flask(__name__)

def get_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='xy528491',
        database='databasedemo'
        )
    return connection


@app.route('/')
def home():
    connection = get_connection()
        
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    sql = "SELECT * FROM Employee"
    cursor.execute(sql)
    return render_template("index.template.html", results=cursor)

@app.route("/albums-old")
def albums():
    connection = get_connection()
        
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT * FROM Album"
    
    # The results will be stored inside the cursor
    # after we do cursor.execute(sql)
    cursor.execute(sql)
    
    # we are passing the cursor to the template as the placeholder results
    return render_template('album.template.html', results=cursor)


@app.route('/combined')
def combined_table():
    # step 1 : Create the connection
    connection = get_connection()
        
    employeeCursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM Employee"
    employeeCursor.execute(sql)
    
    albumCursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM Album"
    albumCursor.execute(sql)
    
    return render_template("combined_table.template.html",
    employeeResults = employeeCursor, albumResults = albumCursor)

@app.route('/search')
def search():
    return render_template("search.template.html")
    
@app.route('/search', methods=['POST'])
def process_search():
    # try to retrieve out what the person has entered into the field
    artist = request.form['artist']
    album = request.form['album']
    
    # create connection
    connection = get_connection()
        
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    sql = """
        SELECT * FROM Album 
        INNER JOIN Artist ON Album.ArtistId = Artist.ArtistId
        WHERE Title LIKE '%{}%' AND Artist.Name LIKE '%{}%'
        
    """.format(album, artist)
    print(sql)

    cursor.execute(sql)
    
    # MAKE SURE TO COMMENT OUT THE TEST CODE
    # for each_result in cursor:
    #     print(each_result)
    return render_template("search_results.template.html", results=cursor)
    
@app.route('/new-album')
def show_new_album_form():
    connection = get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    sql = "SELECT * FROM Artist"
    cursor.execute(sql)
    
    return render_template("add_new_album.template.html", artists=cursor)
    
@app.route('/new-album', methods=['POST'])
def process_add_album():
    artist = request.form['artist']
    album = request.form['album']
    
    connection = get_connection();
    cursor = connection.cursor()
    
    sql = "SELECT MAX(AlbumId) FROM Album"
    cursor.execute(sql)
    
    max_id = cursor.fetchone()[0]
    next_id = max_id + 1
    
    # Inserting the new album

    sql = """
     INSERT INTO Album (AlbumId, Title, ArtistId)
     VALUES ({}, "{}", {})
    """.format(next_id, album, artist)
    
    cursor.execute(sql)
    
    # have to commit to save all changes!
    connection.commit()
    
    return "done"
    
# a route with one route parameter named "album_id"
#            edit-album/999 
@app.route('/edit-album/<album_id>')
def show_edit_album_form(album_id):
    connection = get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    #select all the artists
    artistCursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM Artist"
    artistCursor.execute(sql)
    
    
    sql = "SELECT * FROM Album WHERE AlbumId = {}".format(album_id)
    cursor.execute(sql)
    
    album = cursor.fetchone()
    
    return render_template('edit_album_form.template.html', album=album, artistCursor=artistCursor)

@app.route('/edit-album/<album_id>', methods=['POST'])
def process_edit_album(album_id):
    artist = request.form['artist']
    album = request.form['album']
    
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = """
    UPDATE Album SET Title = "{}", ArtistId = {}
    WHERE AlbumId = {}
    """.format(album, artist, album_id)
    
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return "done"


@app.route('/albums')    
def show_albums():
    connection = get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    sql = "SELECT * FROM Album INNER JOIN Artist ON Album.ArtistId = Artist.ArtistId"
    cursor.execute(sql)
    
    return render_template("show_all_albums.template.html", results=cursor)
    
@app.route('/album/<album_id>/tracks')
def show_album_details(album_id):
    connection = get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    sql = """
        SELECT Track.Name as TrackName, Composer, UnitPrice, Genre.Name as GenreName FROM Track 
        INNER JOIN Genre On Track.GenreId = Genre.GenreId
        WHERE AlbumId={}
    """.format(album_id)
    cursor.execute(sql)
    
    return render_template("show_tracks.template.html", results=cursor)
    
# "magic code" -- boilerplate
if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost', port=5000)