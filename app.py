import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":

        keywords = request.form["keywords"]
        audience = request.form["audience"]
        length = request.form['length']

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful writing assistant."
                                              "You will be given a handful of keywords, a target audience, and an article length."
                                              "Please write an article which is Search Engine Optimized."},

                {"role": "user", "content": "Keywords:" + keywords +
                                            "Target Audience" + audience +
                                            "Article Length" + length}

            ]
        )

        return redirect(url_for("index", result=completion.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

def gen_article(keywords, audience, length):
    return """"You are a helpful writing assistant. You will be given a handful of keywords, 
    a target audience, and an article length. Please write the article to be Search Engine Optimized."
""".format(
        audience.capitalize()
    )
