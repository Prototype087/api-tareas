from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "base_tareas"
mysql = MySQL(app)

app.secret_key = "mysecretkey"

@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tareas ORDER BY id DESC")
    data = cur.fetchall()
    return render_template("index.html", tasks = data)

@app.route("/add_task", methods=["POST"])
def add_task():
    if request.method == "POST":
       names = request.form["name"]
       descriptions = request.form["description"]
       dates = request.form["date"]
       statuss = "Incompleto"

       cur = mysql.connection.cursor()
       cur.execute("INSERT INTO  tareas(TITULO, DESCRIPCION, FECHA_LIMITE, STATUS) VALUES (%s, %s, %s, %s)",(names, descriptions, dates, statuss ))
       mysql.connection.commit()
       flash("Task added")
       return redirect(url_for("Index"))

@app.route("/undone/<string:id>")
def undone(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tareas SET STATUS = 'Incompleta' WHERE id = {0}".format(id))
    mysql.connection.commit()
    flash("Updated")
    return redirect(url_for("Index"))


@app.route("/done/<string:id>")
def done(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tareas SET STATUS = 'Listo!' WHERE id = {0}".format(id))
    mysql.connection.commit()
    flash("Updated")
    return redirect(url_for("Index"))

    







if __name__ =="__main__":
    app.run(port =3000, debug = True)