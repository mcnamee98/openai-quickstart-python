import os

import openai
import psycopg2
import json
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

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

        insert_query = """
            INSERT INTO api_calls (input_data, output_data, timestamp)
            VALUES (%s, %s, now())
        """

        # insert_query = """
        #     INSERT INTO api_calls_revised_inputs (keywords, length, audience, output, timestamp )
        #     VALUES (%s, %s, %s, %s, now())
        # """

        input_data = {
            "Keywords": keywords,
            "Target Audience": audience,
            "Article Length": length
        }
        cur.execute(insert_query, (json.dumps(input_data), json.dumps(result),))

        # cur.execute(insert_query, (json.dumps(keywords), json.dumps(length), json.dumps(audience), json.dumps(result),))
        conn.commit()

        return render_template("index.html", result=result, keywords=keywords, audience=audience, length=length)

    result = request.args.get("result")
    return render_template("index.html", result=result)

@app.route("/previous-articles", methods=["GET"])
def previous_articles():
    # Fetch the data from the database (assuming you have a SELECT query)
    select_query = "SELECT input_data, timestamp FROM api_calls"
    cur.execute(select_query)
    previous_data = cur.fetchall()

    return render_template("previous_articles.html", previous_data=previous_data)

@app.route("/article/<timestamp>", methods=["GET"])
def article_detail(timestamp):
    select_query = "SELECT output_data FROM api_calls WHERE timestamp = %s"
    cur.execute(select_query, (timestamp,))
    article_content = cur.fetchone()

    return render_template("article_detail.html", article_content=article_content)
