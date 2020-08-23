from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


"""Use it in this website https://www.bootstrapcdn.com/, https://getbootstrap.com/docs/4.5/examples/pricing/"""

app = Flask(__name__)#Передаёт файл(его имя) для запуска
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' #Подключаем базу данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #Передаём объект на основе класса Flask


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)#Создаём колонку в сущности
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')#Отслеживаем url главной странички(декоратор)
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()# Первая запись из базы данных
    return render_template('posts.html', articles=articles)

@app.route('/posts/<int:id>')
def post_details(id):
    article = Article.query.get(id)
    return render_template('post_details.html', article=article)

@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id) #Если запись по id не находится, то викидывается ошибка 404

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При удалении статьи произошла ошибка'
    return render_template('post_details.html', article=article)

@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts') #Возвращяем на главную страницу
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create_article.html')


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)

    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:

            db.session.commit()
            return redirect('/posts') #Возвращяем на главную страницу
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template('post_update.html', article=article)

# @app.route('/user/<string:name>/<int:id>') #Передача параметров в функцию
# def user(name, id):
#     return "User name: " + name + " user id: " + str(id)

if __name__ == "__main__": # Говорим, что файл основной
    app.run(debug=True) # Запуск сервера и даём возможность дебажить