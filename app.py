from flask import Flask, render_template_string
import qrcode, io, base64

app = Flask(__name__)

# Твои кошельки
W = [
    {"n": "BITCOIN", "a": "bc1qrpg5nwr5t8jl3nnavgf2k2v4c43u75c9usxpyk"},
    {"n": "USDT (ERC20)", "a": "0x40745600a508d653549c664d050b90826e4b61ba"}
]

def get_qr(t):
    qr = qrcode.make(t)
    b = io.BytesIO()
    qr.save(b, "PNG")
    return base64.b64encode(b.getvalue()).decode()

H = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RED_TERMINAL</title>
    <style>
        body { background: #000; color: #f00; font-family: monospace; text-align: center; margin: 0; padding: 20px; overflow-x: hidden; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.5; }
        .card { border: 2px solid #f00; background: rgba(0,0,0,0.8); margin: 20px auto; padding: 20px; max-width: 350px; box-shadow: 0 0 20px #f00; }
        .qr { background: #fff; padding: 10px; margin: 15px 0; width: 200px; display: inline-block; }
        .addr { font-size: 10px; word-break: break-all; color: #ff9999; margin-bottom: 15px; }
        .btn { background: #f00; color: #000; border: none; padding: 10px; cursor: pointer; width: 100%; font-weight: bold; }
        .tx-box { border: 1px solid #f00; max-width: 500px; margin: 20px auto; padding: 10px; text-align: left; font-size: 12px; }
    </style>
</head>
<body>
    <canvas id="m"></canvas>
    <h1 style="text-shadow: 0 0 10px #f00;">SYSTEM_RED_CHANNEL</h1>
    <div style="border: 1px solid #f00; padding: 15px; max-width: 600px; margin: 0 auto; background: rgba(20,0,0,0.7);">
        > MISSION: Humanitarian Aid for Iran<br>
        > PROTOCOL: Full Anonymity Secured
    </div>

    <div style="margin: 20px 0;">
        <div style="width:300px; height:15px; border:1px solid #f00; margin: 0 auto; position: relative;">
            <div style="width: 21%; height: 100%; background: #f00; box-shadow: 0 0 10px #f00;"></div>
        </div>
        <div style="font-size: 12px; margin-top: 5px;">GOAL: 2.0 BTC (21% reached)</div>
    </div>

    {% for w in W %}
    <div class="card">
        <h3>{{ w.n }}</h3>
        <div class="qr"><img src="data:image/png;base64,{{ q(w.a) }}" width="200"></div>
        <div class="addr">{{ w.addr }}</div>
        <button class="btn" onclick="navigator.clipboard.writeText('{{ w.a }}');alert('Copied!')">COPY ADDRESS</button>
    </div>
    {% endfor %}

    <div class="tx-box">
        <div style="color:#f00; border-bottom: 1px solid #f00; margin-bottom: 5px;">[!] LIVE_DATA_FEED:</div>
        <div id="tx"></div>
    </div>

    <script>
        const c = document.getElementById('m');
        const x = c.getContext('2d');
        c.width = window.innerWidth; c.height = window.innerHeight;
        const drops = Array(Math.floor(c.width/20)).fill(1);
        function draw() {
            x.fillStyle = 'rgba(0,0,0,0.1)'; x.fillRect(0,0,c.width,c.height);
            x.fillStyle = '#f00'; x.font = '20px monospace';
            drops.forEach((y, i) => {
                x.fillText(Math.floor(Math.random()*2), i*20, y*20);
                if(y*20 > c.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 50);

        function addTx() {
            const list = document.getElementById('tx');
            const d = document.createElement('div');
            d.innerHTML = `[${new Date().toLocaleTimeString()}] Confirmed: +${(Math.random()*0.05).toFixed(3)} BTC...`;
            list.prepend(d);
            if(list.childNodes.length > 4) list.removeChild(list.lastChild);
        }
        setInterval(addTx, 5000); addTx();
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, q=get_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
