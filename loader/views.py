from flask import Flask, render_template, request, Blueprint
import json
from json import JSONDecodeError

loader_blueprint = Blueprint('loader_blueprint', __name__)


def is_filename_allowed(filename):
    """
    Проверка на допустимое расширение прикрепляемого файла
    """
    ALLOWED_EXTENSIONS = ('jpeg', 'jpg', 'png')
    extension = filename.split(".")[-1]
    if extension in ALLOWED_EXTENSIONS:
        return True
    return False


def load_info_from_json():
    """
    Получить все информацию обо всех постах, записанных в файле posts.json
    """
    with open("posts.json", "r") as file:
        try:
            posts_json = file.read()
            posts = json.loads(posts_json)
        except FileNotFoundError:\
            logging.exception("Ошибка доступа к файлу")
        except JSONDecodeError:\
            logging.exception("Файл не удается преобразовать")
        return posts


def save_post_info(post_info):
    """
    Получаем картинку и описание поста и дописываем эту информацию к уже имеющемуся перечню постов
    """
    all_posts = load_info_from_json()
    all_posts.append(post_info)
    with open("posts.json", "w") as file:
        json_all_posts = json.dumps(all_posts)
        file.write(json_all_posts)


@loader_blueprint.route('/GET/post')
def post_append_screen():
    """
    Страница добавления нового поста
    """
    return render_template("post_form.html")


@loader_blueprint.route('/POST/post', methods=['POST'])
def page_upload():
    """
    Страница после успешного добавления поста
    """
    picture = request.files.get("picture")
    if not picture:
        return "Ошибка загрузки. Скорее всего ты забыл картинку. Ай-яй-яй"
    content = request.form['content']
    filename = picture.filename
    if is_filename_allowed(filename):
        picture.save(f"./static/local/{filename}")
        post_info = {"pic":f"./static/local/{filename}", "content":content}
        save_post_info(post_info)
        return render_template("post_uploaded.html", content=content, filename=filename)
    else:
        return "Ошибка в расширении прикрепляемого файла. Поддерживаются расширения типов jpeg, jpg, png"




