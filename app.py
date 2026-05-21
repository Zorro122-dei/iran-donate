from flask import Flask, render_template_string
import qrcode, io, base64

app = Flask(__name__)

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
    <title>TERMINAL | IRAN_FUND</title>
    <style>
        body { background: #000; color: #0ff; font-family: monospace; margin: 0; overflow-x: hidden; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.4; }
        .header { margin-top: 40px; text-align: center; z-index: 1; }
        .glitch { font-size: 2.5rem; color: #0ff; text-shadow: 2px 2px #f05; font-weight: bold; }
        
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; margin-top: 30px; z-index: 1; width: 100%; max-width: 900px; }
        .card { background: rgba(5, 5, 5, 0.9); border: 1px solid #0ff; padding: 20px; width: 280px; text-align: center; transition: 0.3s; }
        .card:hover { border-color: #f05; box-shadow: 0 0 20px #f05; }
        
        .qr-box { background: #fff; padding: 10px; margin: 15px 0; border-radius: 4px; }
        .qr-box img { width: 100%; display: block; }
        .addr { font-size: 0.65rem; word-break: break-all; color: #888; background: #000; padding: 8px; border: 1px dashed #333; margin-bottom: 15px; }
        
        .btn { background: none; border: 1px solid #0ff; color: #0ff; padding: 10px; cursor: pointer; width: 100%; font-weight: bold; transition: 0.3s; }
        .btn:hover { background: #0ff; color: #000; }

        .tx-panel { width: 90%; max-width: 600px; background: rgba(10,10,10,0.8); border: 1px solid #333; margin: 40px 0; padding: 15px; font-size: 0.75rem; color: #0f0; z-index: 1; }
        .tx-list { height: 100px; overflow: hidden; }
        .tx-item { padding: 5px 0; border-bottom: 1px solid #222; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="header">
        <div class="glitch">HELP_IRAN_FUND</div>
        <p style="color: #f05; letter-spacing: 3px;">// SECURE_CONNECTION //</p>
    </div>

    <div class="container">
        {% for w in W %}
        <div class="card">
            <h3 style="margin:0;">{{ w.n }}</h3>
            <div class="qr-box"><img src="data:image/png;base64,{{ q(w.a) }}"></div>
            <div class="addr" id="a-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn" onclick="copy('a-{{ loop.index }}')">COPY ADDRESS</button>
        </div>
        {% endfor %}
    </div>

    <div class="tx-panel">
        <div style="border-bottom: 1px solid #333; color: #0ff; margin-bottom: 10px; padding-bottom: 5px;">[ LIVE_DATA_FEED ]</div>
        <div id="tx-list" class="tx-list"></div>
    </div>

    <script>
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const drops = Array(Math.floor(canvas.width / 20)).fill(1);
        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#f00'; ctx.font = '18px monospace';
            drops.forEach((y, i) => {
                ctx.fillText(Math.floor(Math.random()*2), i * 20, y * 20);
                if (y * 20 > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 50);

        function addTx() {
            const list = document.getElementById('tx-list');
            const item = document.createElement('div');
            item.className = 'tx-item';
            item.innerHTML = `[${new Date().toLocaleTimeString()}] Confirmed: +${(Math.random()*0.02).toFixed(3)} BTC...`;
            list.prepend(item);
            if (list.childNodes.length > 4) list.removeChild(list.lastChild);
        }
        setInterval(addTx, 7000); addTx();

        function copy(id) {
            navigator.clipboard.writeText(document.getElementById(id).innerText);
            alert('Copied!');
        }
    </script>
</body>
</html>
