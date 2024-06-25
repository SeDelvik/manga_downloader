from jinja2 import Environment, FileSystemLoader

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_post():
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("test_template.html")

    return template.render(value="test_test")


@app.route('/', methods=['POST'])
def home_get():
    print('asd')
    return request.form.get('name')


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
