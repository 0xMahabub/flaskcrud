from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# setting database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Todo ' + str(self.id)


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return render_template('pages/index.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('pages/about.html')



@app.route('/contact', methods=['GET'])
def contact():
    return render_template('pages/contact.html')

# @app.route('/test/<name>', methods=['GET'])
# def test(name):
#     return render_template('pages/test.html', context=name)


# Create or Read TODO's
@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        req_todo = request.form['todo']
        newTodo = Todo(todo=req_todo)
        db.session.add(newTodo)
        db.session.commit()
        return redirect('/todo')

    else:
        all_todos = Todo.query.order_by(Todo.created_at).all()
        return render_template('pages/todo.html', todos=all_todos)



# Update Todo
@app.route('/todo/edit/<int:id>', methods=['GET', 'POST'])
def update_todo(id):
    # find todo
    findingTodo = Todo.query.get(id)

    if (findingTodo == None):
        return render_template('pages/404.html', msg="Error 404! Todo couldn't be found!")


    if (request.method == 'POST'):
        findingTodo.todo = request.form['todo']
        db.session.commit()
        return redirect('/todo')
    
    else:
        return render_template('pages/todo_edit.html', todo=findingTodo)


# Delete a Todo
@app.route('/todo/del/<int:id>', methods=['GET'])
def delete(id):
    findingTodo = Todo.query.get(id)

    if (findingTodo == None):
        return render_template('pages/404.html', msg="Error 404! Todo couldn't be found!")
    else:
        db.session.delete(findingTodo)
        db.session.commit()
        return redirect('/todo')





if __name__ == "__main__":
    app.run(debug=True)
