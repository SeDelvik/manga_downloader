from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, redirect

from img_set_creator import *

app = Flask(__name__)

manga_url = ''
select_all = False


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
    except:
        return redirect('/',code=301)
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("volumes.html")
    global select_all
    element = template.render(elements=volumes_url, select_all=select_all)
    select_all = False
    return element


@app.route('/volumes', methods=['POST'])
def volume_post():
    if request.form.get('select_all'):
        global select_all
        select_all = True
        return redirect("/volumes", code=301)
    return redirect("/", code=301)


if __name__ == "__main__":
    app.run(debug=True)

# @app.route('/calc/', methods=['GET', 'POST'])
# def calc():
#     if request.method == 'POST':
#         a = int(request.form['a'])
#         b = int(request.form['b'])
#         result = a + b
#         return f'{a} + {b} = {result}'
#     return f'Был получен {request.method} запрос.'
