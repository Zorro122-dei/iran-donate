from flask import Flask, render_template_string
import qrcode, io, base64

app = Flask(__name__)

# Твои данные
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
<html>
<head>
    <meta charset="UTF-8">
    <title>TERMINAL</title>
    <style>
        body { background: #000; color: #0ff; font-family: monospace; text-align: center; margin: 0; padding: 0; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.4; }
        .header { margin-top: 30px; }
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; padding: 20px; }
        .card { border: 1px solid #0ff; background: rgba(0,0,0,0.8); padding: 20px; width: 280px; }
        .qr { background: #fff; padding: 10px; margin: 10px 0; }
        .addr { font-size: 10px; word-break: break-all; color: #888; margin: 10px 0; }
        .btn { border: 1px solid #0ff; color: #0ff; background: none; padding: 10px; cursor: pointer; width: 100%; }
        .btn:hover { background: #0ff; color: #000; }
        #tx { border: 1px solid #333; max-width: 500px; margin: 20px auto; padding: 10px; font-size: 11px; color: #0f0; text-align: left; }
    </style>
</head>
<body>
    <canvas id="m"></canvas>
    <div class="header">
        <h1 style="text-shadow: 0 0 10px #0ff;">HELP_IRAN_FUND</h1>
        <p style="color: #f05;">// SECURE_ANONYMOUS_CONNECTION //</p>
    </div>
    <div class="container">
        {% for w in W %}
        <div class="card">
            <h3>{{ w.n }}</h3>
            <div class="qr"><img src="data:image/png;base64,{{ q(w.a) }}" width="100%"></div>
            <div class="addr">{{ w.a }}</div>
            <button class="btn" onclick="navigator.clipboard.writeText('{{ w.a }}');alert('Copied!')">COPY ADDRESS</button>
        </div>
        {% endfor %}
    </div>
    <div id="tx">
        <div style="border-bottom:1px solid #333; margin-bottom:5px; color:#0ff">[ LIVE_FEED ]</div>
        <div id="list"></div>
    </div>
    <script>
        const c = document.getElementById('m');
        const x = c.getContext('2d');
        c.width = window.innerWidth; c.height = window.innerHeight;
        const d = Array(Math.floor(c.width/20)).fill(1);
        function draw() {
            x.fillStyle = 'rgba(0,0,0,0.1)'; x.fillRect(0,0,c.width,c.height);
            x.fillStyle = '#f00'; x.font = '15px monospace';
            d.forEach((y, i) => {
                x.fillText(Math.floor(Math.random()*2), i*20, y*20);
                if(y*20 > c.height && Math.random() > 0.975) d[i] = 0;
                d[i]++;
            });
        }
        setInterval(draw, 50);
        function add() {
            const l = document.getElementById('list');
            const e = document.createElement('div');
            e.innerHTML = `[${new Date().toLocaleTimeString()}] Confirmed: +${(Math.random()*0.05).toFixed(3)} BTC...`;
            l.prepend(e);
            if(l.childNodes.length > 4) l.removeChild(l.lastChild);
        }
        setInterval(add, 8000); add();
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, q=get_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
