from flask import Blueprint

front = Blueprint ('front', __name__ , template_folder = 'templates')

@front.route('/')
def index():
    return "Hello from front"