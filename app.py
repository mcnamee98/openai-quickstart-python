import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import psycopg2
import json
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")



# app = Flask(__name__)
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="JohnMcNamee",
    user="JohnMcNamee",
    # password="your-database-password"
)
cur = conn.cursor()

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

        result = completion.choices[0].message.content

        # Insert data into the database
        insert_query = """
            INSERT INTO api_calls (input_data, output_data, timestamp)
            VALUES (%s, %s, now())
        """

        insert_query = """
            INSERT INTO api_calls (input_data, output_data, timestamp)
            VALUES (%s, %s, now())
        """
        input_data = {
            "Keywords": keywords,
            "Target Audience": audience,
            "Article Length": length
        }
        cur.execute(insert_query, (json.dumps(input_data), json.dumps(result),))
        conn.commit()

        # input_data = f'{{"Keywords": "{keywords}", "Target Audience": "{audience}", "Article Length": "{length}"}}'
        # result_db = result
        # cur.execute(insert_query, (input_data, result_db))
        # conn.commit()
        # cur.execute(insert_query, (f"Keywords: {keywords}, Target Audience: {audience}, Article Length: {length}", result))
        # conn.commit()

        return render_template("index.html", result=result, keywords=keywords, audience=audience, length=length)

    result = request.args.get("result")
    return render_template("index.html", result=result)


# def generate_prompt(animal):
#     return """Suggest three names for an animal that is a superhero.
#
# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(
#         animal.capitalize()
#     )
#
# def gen_article(keywords, audience, length):
#     return """"You are a helpful writing assistant. You will be given a handful of keywords,
#     a target audience, and an article length. Please write the article to be Search Engine Optimized."
# """.format(
#         audience.capitalize()
#     )
