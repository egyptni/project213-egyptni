import os
from flask import Flask, render_template, request, jsonify
from Logic.MarkovChains import Chains

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home_page.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/_background_process", methods=["GET", "POST"])
def background_process():
    # Получение информации из html
    order = float(request.args.get("order"))
    file_path1 = os.path.join(os.path.dirname(__file__), 'VisualExamples/poems Lermontov_clean.txt')
    chains = Chains(order=int(order),
                    filename=file_path1,
                    length=50)
    output = chains.getPoem(rest=False)
    return jsonify(result=output)


@app.route("/api/v1/poem", methods=["GET"])
def api_all():
    try:
        if "order" in request.args:
            order = int(request.args["order"])
        else:
            return "Ошибка: Степень последовательности не указана. Пожалуйста укажите 'order' в api запросе. "
        file_path2 = os.path.join(os.path.dirname(__file__), 'VisualExamples/poems Lermontov_clean.txt')
        chains = Chains(order=order,
                        filename=file_path2,
                        length=50)
        output = chains.getPoem(rest=True)
        return jsonify(result=output)
    except:
        pass


if __name__ == "__main__":
    app.run(debug=False)
