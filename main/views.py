from flask import Flask, render_template, request, Blueprint
import json

main_blueprint = Blueprint('main_blueprint', __name__)


def load_info_from_json():
    """
    Загрузка информации о всех постах в файле post.json
    """
    with open("posts.json", "r") as file:
        posts_json = file.read()
        posts = json.loads(posts_json)
        return posts


def searching(word):
    """
    Отбирает посты, в которых есть искомый запрос
    """
    all_posts = load_info_from_json()
    searched_posts = []
    for post in all_posts:
        if word in post["content"]:
            searched_posts.append(post)
    return searched_posts


@main_blueprint.route("/")
def main_page():
    """
    Главная страница
    """
    return render_template("index.html")


@main_blueprint.route('/search')
def searching_page():
    """
    Cтраница поиска по запросу
    """
    search_word = request.args['s']
    info = searching(search_word)
    return render_template("post_list.html", search_request=search_word, searched_posts=info)


