from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, redirect, send_file
from flask_cors import CORS

from data_file_creator import *

app = Flask(__name__)
CORS(app)

manga_url = ''
volumes_len = 0


@app.route('/', methods=['GET'])
def home_get():
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("home_page.html")

    return template.render(value=manga_url)


@app.route('/', methods=['POST'])
def home_post():
    global manga_url
    manga_url = request.form.get('url')
    return redirect("/volumes", code=301)


@app.route('/volumes', methods=['GET'])
def volume_get():
    try:
        volumes_url = get_chapter_list(manga_url)
        global volumes_len
        volumes_len = len(volumes_url)
    except ValueError:
        return redirect('/', code=301)
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("volumes.html")
    element = template.render(title_name=get_title_name(manga_url), src_img_url=get_image(manga_url),
                              elements=volumes_url)
    return element


@app.route('/volumes', methods=['POST'])
def volume_post():
    url_arr = []
    for i in range(volumes_len):
        url = request.form.get(f'{i}_name')
        if url:
            url_arr.append(url)
    archive_path = create_content(url_arr, manga_url.split('/')[-1])
    return send_file(archive_path)


if __name__ == "__main__":
    app.run(debug=True)
