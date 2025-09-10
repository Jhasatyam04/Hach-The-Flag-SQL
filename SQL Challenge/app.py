import mysql.connector
import os
from flask import Flask, render_template, request
import base64

app = Flask(__name__)

hacker_icon_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACABAMAAAAxE/oAAAAJ" \
                    "b3RhcmVjZXQgaWNvbiBvcmlnaW5hbCIgCiAgICAgICAgICAgICAgc3Ryb2tlPSJMaWdodEdyZWVu" \
                    "IiBzdHJva2Utd2lkdGg9IjIiICAKICAgICAgICAgICAgICAgZmlsbD0ibm9uZSI+PC9yZWN0Pgog" \
                    "ICAgICAgICAgICA8L2c+Cjwvc3ZnPgo="


@app.route('/', methods=['GET', 'POST'])
def home():
    results_html = ""

    if 'query' in request.args:
        user_query = request.args.get('query')
        
        db_config = {
            'host': 'db',
            'user': 'root',
            'password': 'password',
            'database': 'ctf_db'
        }
        
        try:
    
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            sql_query = f"SELECT title, description FROM challenges WHERE title = '{user_query}';"
            cursor.execute(sql_query)
            
            sql_union_query = f"SELECT part_order, data FROM flag_parts WHERE part_order = '{user_query}'"

            cursor.execute(sql_query)

            results = cursor.fetchall()
            if not results:
              
                sql_union_query = f"SELECT part_order, data FROM flag_parts WHERE part_order = '{user_query}'"
                cursor.execute(sql_union_query)
                results = cursor.fetchall()

            if results:
                results_html = "<div class='results-box'><pre>"
                for row in results:
                    results_html += f"Part Order: {row[0]}, Data: {row[1]}\n"
                results_html += "</pre></div>"
            else:
                results_html = "<div class='results-box'>No results found.</div>"

        except mysql.connector.Error as err:
            results_html = f"<div class='results-box' style='color: red;'>Database Error: {err}</div>"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SQL Injection CTF Challenge</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');
            
            body {{
                background: rgb(15, 15, 15);
                align-items: center;
                padding: 65px 55px;
                background-color: #000000;
                opacity: 0.8;
                background-image: linear-gradient(0deg, #000000 50%, #0e0e0e 50%);
                background-size: 10px 10px;
                text-align: center;
                font-family: "Space Mono", monospace;
                min-height: 100vh;
            }}

            h1, h2 {{
                color: lightgreen;
                font-size: 5rem;
            }}

            .hidden-text {{
                opacity: 0%;
                transition: opacity 0.5s ease-in-out;
            }}

            .hidden-text:hover {{
                opacity: 100%;
            }}

            .hacker-icon {{
                width: 120px;
                height: auto;
                margin-bottom: 20px;
                animation: glitch 1.5s infinite;
            }}

            @keyframes glitch {{
                0%, 100% {{ transform: translate(0, 0); }}
                50% {{ transform: translate(2px, -2px); }}
            }}

            .button {{
                display: inline-block;
                margin-top: 20px;
                padding: 12px 24px;
                font-size: 18px;
                font-weight: bold;
                text-decoration: none;
                color: black;
                background: lightgreen;
                border-radius: 5px;
                transition: 0.3s;
            }}

            .button:hover {{
                background: #0e8000;
                color: white;
            }}

            .clue-box {{
                margin-top: 20px;
                padding: 15px;
                background: rgba(0, 255, 0, 0.1);
                border-left: 5px solid lightgreen;
                font-style: italic;
                color: lightgreen;
            }}

            /* Styles for the new challenge interface */
            .container {{
                background-color: #1E1E1E;
                border-radius: 12px;
                padding: 40px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
                width: 100%;
                max-width: 600px;
                margin-top: 50px;
                display: none; /* Hidden by default */
            }}
            
            .container-visible {{
                display: block;
            }}
            
            h3 {{
                font-size: 2.5rem;
                font-weight: 700;
                text-align: center;
                margin-bottom: 2rem;
                color: #4CAF50;
            }}

            form {{
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
            }}

            input[type="text"] {{
                background-color: #2D2D2D;
                border: 1px solid #4CAF50;
                border-radius: 8px;
                padding: 1rem;
                color: #E0E0E0;
                outline: none;
                transition: border-color 0.3s;
            }}

            input[type="text"]:focus {{
                border-color: #81C784;
            }}

            .btn-submit {{
                background-color: #4CAF50;
                color: #121212;
                font-weight: 700;
                padding: 1rem;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.1s;
            }}

            .btn-submit:hover {{
                background-color: #81C784;
                transform: translateY(-2px);
            }}

            .results-box {{
                background-color: #2D2D2D;
                border-radius: 8px;
                margin-top: 2rem;
                padding: 1.5rem;
                white-space: pre-wrap;
                font-family: monospace;
                overflow-x: auto;
                border: 1px solid #333;
            }}
        </style>
    </head>
    <body>

        <div id="landing-page">
            <img class="hacker-icon" src="{hacker_icon_base64}" alt="Hacker Icon">
            <h1>SQL Injection CTF Challenge</h1>
            <h2 class="hidden-text">Can you break in?</h2>
            <p class="hidden-text">Find the right input to bypass the system and retrieve the flag.</p>

            <div class="clue-box">
                <p>💡 <span class="hint">Hint:</span> A single **'** is all you need to get started...</p>
            </div>

            <button class="button" onclick="showChallenge()">Start Hacking</button>
        </div>

        <div id="challenge-container" class="container">
            <h3 class="text-3xl font-bold text-center mb-6">CTF Challenge</h3>
            <p class="text-center text-gray-400 mb-6">Find the secret payload using the search bar below.</p>
            <form action="/" method="get">
                <input type="text" name="query" placeholder="Enter your query here..." class="w-full">
                <button type="submit" class="w-full btn-submit">Search</button>
            </form>
            {results_html}
        </div>

        <script>
            function showChallenge() {{
                document.getElementById('landing-page').style.display = 'none';
                document.getElementById('challenge-container').classList.add('container-visible');
            }}
            
            // This script handles the display logic based on whether a query was submitted
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('query')) {{
                showChallenge();
            }}
        </script>

    </body>
    </html>
    """

    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
