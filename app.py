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

        hash = str(request.form["block_hash"])
        addr = str(request.form["btc_add"])

        url_hash = "https://blockchain.info/rawblock/"+hash
        url_addr = "https://blockchain.info/rawaddr/"+addr
        if hash == "":
            pass
        else:
            block = requests.get(url_hash)
            dict_data = json.loads(block.text)
            return """
                <body style="background-color: rgb(240, 255, 255);
                width: 90%;
                height: auto;
                margin: auto;">
                <center>
                <article id= block>
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
                Merkle Root: {4}
                <br>
                Size: {5}
                <br>
                Block Nr: {6}
                <br>
                </div>
                </center>
                </article>
                </body>
                """.format(
            dict_data.get("hash"),
            dict_data.get("prev_block"),
            dict_data.get("nonce"),
            dict_data.get("time"),
            dict_data.get("mrkl_root"),
            dict_data.get("size"),
            dict_data.get("block_index")
            )
        if addr == "":
            pass
        else:
            btc_addr = requests.get(url_addr)
            dict_addr = json.loads(btc_addr.text)
            return """
                <body style="background-color: rgb(240, 255, 255);
                width: 90%;
                height: auto;
                margin: auto;">
                <center>
                <article id = wallet>
                <div>
                <h1>Infos zu BTC Addresse</h1>
                <h2>Addresse: {0}
                <br>
                Eingehend: {1}
                <br>
                Ausgehend: {2}
                <br>
                Bestand: {3}
                </div>
                </center>
                </article>
                </body>
                """.format(
            dict_addr.get("address"),
            dict_addr.get("total_received"),
            dict_addr.get("total_sent"),
            dict_addr.get("final_balance")   
            )

    return render_template("index.html")


app.run(debug=True)
