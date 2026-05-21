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
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>SECURE_FUND_v2.0</title>
    <style>
        body { background: #000; color: #0ff; font-family: 'Courier New', monospace; margin: 0; overflow-x: hidden; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.3; }
        .glitch-container { margin-top: 50px; text-align: center; }
        .glitch { font-size: 3rem; font-weight: bold; text-transform: uppercase; position: relative; text-shadow: 0.05em 0 0 #f05, -0.025em -0.05em 0 #0ff; animation: glitch 1s infinite; }
        @keyframes glitch { 0% { transform: translate(0); } 20% { transform: translate(-2px, 2px); } 40% { transform: translate(-2px, -2px); } 100% { transform: translate(0); } }
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 40px; margin-top: 50px; z-index: 1; }
        .card { background: rgba(10, 10, 10, 0.9); border: 2px solid #0ff; padding: 25px; border-radius: 10px; width: 300px; text-align: center; transition: 0.4s; box-shadow: 0 0 20px rgba(0, 255, 255, 0.2); }
        .card:hover { transform: scale(1.05); border-color: #f05; box-shadow: 0 0 30px #f05; }
        .qr-box { background: #fff; padding: 10px; border-radius: 5px; margin: 20px 0; }
        .qr-box img { width: 100%; border: 2px solid #000; }
        .addr { font-size: 0.7rem; word-break: break-all; color: #888; background: #000; padding: 10px; border: 1px dashed #333; }
        .btn { margin-top: 20px; background: none; border: 1px solid #0ff; color: #0ff; padding: 12px; cursor: pointer; width: 100%; text-transform: uppercase; font-weight: bold; transition: 0.3s; }
        .btn:hover { background: #0ff; color: #000; }
        .footer { margin-top: 50px; color: #444; font-size: 0.8rem; padding: 20px; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="glitch-container">
        <div class="glitch">SYSTEM_OVERRIDE</div>
        <p style="letter-spacing: 5px; color: #f05;">// ANONYMOUS_HELP_IRAN //</p>
    </div>

    <div class="container">
        {% for w in W %}
        <div class="card">
            <h2 style="margin:0;">{{ w.n }}</h2>
            <div class="qr-box"><img src="data:image/png;base64,{{ q(w.a) }}"></div>
            <div class="addr" id="a-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn" onclick="copy('a-{{ loop.index }}')">Copy Address</button>
        </div>
        {% endfor %}
    </div>

    <div class="footer">ENCRYPTED_CONNECTION_STABLE_2024</div>

    <script>
        // Matrix Effect
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const letters = '0123456789ABCDEFHIJKLMNOPRSTUVWXYZ';
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < drops.length; i++) {
                const text = letters.charAt(Math.floor(Math.random() * letters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 33);

        function copy(id) {
            const t = document.getElementById(id).innerText;
            navigator.clipboard.writeText(t);
            alert('Адрес скопирован в буфер!');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, q=get_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
