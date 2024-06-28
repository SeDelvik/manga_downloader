from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, redirect, send_file

from img_set_creator import *

app = Flask(__name__)

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
    element = template.render(elements=volumes_url)
    return element


@app.route('/volumes', methods=['POST'])
def volume_post():
    url_arr = []
    for i in range(volumes_len):
        url = request.form.get(f'{i}_name')
        if url:
            url_arr.append(url)
    print(url_arr)
    archive_path = create_archive(url_arr, manga_url.split('/')[-1])
    print('filepath', archive_path)
    return send_file(archive_path)


def create_archive(url_arr, output_file_name):
    for url_vol in url_arr:
        img_set = get_img_set(manga_url + '/' + '/'.join(url_vol.split('/')[2:]))
        get_pdf_file(str(url_vol.split('/')[-1]), img_set)
    archive_path = create_zip(output_file_name)
    drop_pdf_dir()
    return archive_path


if __name__ == "__main__":
    app.run(debug=True)
