from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return f'<h1>Hello, User</h1>'

@app.route('/all')
def see_all():
    conn = sqlite3.connect('blog.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()
    conn.commit()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/new', methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = str(datetime.date.today())
        if not title:
            return 'Sorry, you should insert title'
        if not description:
            return 'Sorry, you should insert description'
        conn = sqlite3.connect('blog.sqlite3')  # соединяюсь с БД
        cursor = conn.cursor()  # инициальзирую курсор
        values = (title, description, date)  # присваиваю переменной values значения для заполнения, чтобы потом их не писать
        cursor.execute("INSERT INTO  posts (title, description, date) VALUES ( ?, ?, ?)", values)  # передаю в курсор запрос к БД
        conn.commit()  # отправляю SQL запрос в БД
        conn.close()  # закрываю соединение
        return redirect('/all')
    else:
        return render_template('add.html')

@app.route('/fix', methods=['GET', 'POST'])
def fix_column():
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        description = request.form['description']
        conn = sqlite3.connect('blog.sqlite3')  # соединяюсь с БД
        cursor = conn.cursor()  # инициальзирую курсор
        values = (title, description, id)
        cursor.execute("UPDATE posts SET title=?, description=? WHERE id=?", values)  # передаю в курсор запрос к БД
        conn.commit()  # отправляю SQL запрос в БД
        conn.close()  # закрываю соединение
        return redirect('/all')
    else:
        return render_template('fix.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_column():
    if request.method == 'POST':
        id=request.form['id']
        conn = sqlite3.connect('blog.sqlite3')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id=?", id)
        conn.commit()
        conn.close()
        return redirect('/all')
    else:
        return render_template('delete.html')



if __name__ == '__main__':
    app.run(debug=True)