from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from universe_create import GameOfLife

app = Flask(__name__)


@app.route("/")
def root():
    return render_template("main_page.html")


@app.route("/grid_size")
def choose_grid_size():
    return render_template('set_grid.html')


@app.route("/grid_size/size", methods=['POST'])
def set_size():
    rows = int(request.form.get('rows', 20))
    cols = int(request.form.get('cols', 20))
    GameOfLife(rows, cols)

    return redirect(url_for('simulation'))


@app.route("/game_dif")
def choose_game_dificulty():
    return render_template('game_dificulty.html')


@app.route("/game_dif/dificulty", methods=['POST'])
def game_dificulty():
    rows = int(request.form.get('rows', 20))
    cols = int(request.form.get('cols', 20))
    GameOfLife(rows, cols)

    world = GameOfLife()
    world.form_new_generation()

    return redirect(url_for('game'))


@app.route("/simulation")
def simulation():
    new_world = GameOfLife()
    return render_template("simulation.html", grid_size=new_world.world, counter=new_world.counter)


@app.route("/rules")
def rules():
    return render_template("rules.html")


@app.route("/rules/neighbors")
def neighbor_rules():
    return render_template('neighbor_rules.html')


@app.route("/game")
def game():
    new_world = GameOfLife()
    return render_template("game.html",
                           grid_size=new_world.world,
                           counter=new_world.counter,
                           mistakes=new_world.mistakes)


@app.route("/game/check", methods=['POST'])
def check_condition():
    user_matrix = request.form.get('matrix-data')
    world = GameOfLife()
    print("FORM:", request.form)

    if user_matrix:
        world.form_new_generation()
        user_matrix_list = json.loads(user_matrix)
        answer = world.check_condition(user_matrix_list)
        if answer == "Hello":
            raise ValueError("Значения не того типа")
        return redirect(url_for('game'))

    raise ValueError("Матрица не создалась")


@app.route("/other")
def something():
    return render_template("another_page.html")


@app.route('/api/get_grid')
def get_grid():
    new_world = GameOfLife()
    new_world.form_new_generation()
    matrix = new_world.world

    return jsonify({"grid": matrix, "counter": new_world.counter})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
