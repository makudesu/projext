from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projectx.sqlite3'
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column('project_id', db.Integer, primary_key = True)
    title = db.Column(db.String(140), unique = True)
    desc = db.Column(db.String(140))
    done = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<Project %r>' % self.title


class Task(db.Model):
    id = db.Column('task_id', db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
    done = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<Task %r>' % self.title


class Todo(db.Model):
    id = db.Column('todo_id', db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'))
    done = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<Todo %r>' % self.title

class Issue(db.Model):
    id = db.Column('issue_id', db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'))
    done = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<Issue %r>' % self.title


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/project/")
@app.route("/project/<project>")
def project(project=None):
    if project is None:
        return "No project selected"
    projects = Project.query.filter_by(id=project)
    tasks = Task.query.filter_by(project_id=project)
    task = []
    project = {}
    for data in projects:
        project['title'] = data.title

    for todo in tasks:
        task.append({'title':todo.title, 'status':todo.done})
    return render_template('project.html', project=project, task=task)


@app.route("/task/")
@app.route("/task/<task>")
def task(task=None):
    if task is None:
        return "No task selected"
    task = Task.query.all()
    return render_template('task.html', task=task)


@app.route("/todo/")
@app.route("/todo/<todo>")
def todo(todo=None):
    if todo is None:
        return "No todo selected"
    todo = Todo.query.all()
    return render_template('todo.html', todo=todo)


@app.route("/issue/")
@app.route("/issue/<issue>")
def issue(issue=None):
    if issue is None:
        return "No issue selected"
    issue = Issue.query.all()
    return render_template('issue.html', issue=issue)


if __name__ == "__main__":
    app.run()
    db.create_all()


