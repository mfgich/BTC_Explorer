from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)


@app.route("/")
def home():
    return """<body style="background-color: rgb(240, 255, 255);
                width: 90%;
                height: auto;                
                margin: auto;
                margin-top: 10%;">
                <center>
                <h2>Klick das Bild um zur Suche zu gelangen</h2>
                <a href="/find"><img src="static/images/cat.jpg" width="300"/>
                </center>
                </body>
                """


@app.route("/find", methods=["GET", "POST"])
def find():

    if request.method == "POST":

        username = str(request.form["block_hash"])
        addr = str(request.form["btc_add"])

        url_hash = "https://blockchain.info/rawblock/"+username
        url_addr = "https://blockchain.info/rawaddr/"+addr

        block = requests.get(url_hash)
        btc_addr = requests.get(url_addr)

        dict_data = json.loads(block.text)
        dict_addr = json.loads(btc_addr.text)

        return """
                <body style="background-color: rgb(240, 255, 255);
                width: 90%;
                height: auto;
                margin: auto;">
                <center>
                <div>
                <h1>Blockchain Auszug</h1>
                <h2>Hash: {0}
                <br>
                Prv Hash: {1}
                <br>
                Nonce: {2}
                <br>
                Timestamp: {3}
                <br>
                Merkl Root: {4}
                <br>
                Size: {5}
                <br>
                Block Nr: {6}
                <br>
                </div>
                <div>
                <h1>Infos zu BTC Addresse</h1>
                <h2>Addresse: {7}
                <br>
                Eingehend: {8}
                <br>
                Ausgehend: {9}
                <br>
                Bestand: {10}
                </div>
                </center>
                </body>
                """.format(
            dict_data.get("hash"),
            dict_data.get("prev_block"),
            dict_data.get("nonce"),
            dict_data.get("time"),
            dict_data.get("mrkl_root"),
            dict_data.get("size"),
            dict_data.get("block_index"),
            dict_addr.get("address"),
            dict_addr.get("total_received"),
            dict_addr.get("total_sent"),
            dict_addr.get("final_balance")
        )

    return render_template("index.html")


app.run(debug=True)
