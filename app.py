from flask import Flask, render_template_string
import qrcode, io, base64, random

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
    <title>RED_TERMINAL | IRAN_FUND</title>
    <style>
        body { background: #000; color: #ff0000; font-family: 'Courier New', monospace; margin: 0; overflow-x: hidden; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.6; } /* Яркая матрица */
        .header { margin-top: 40px; text-align: center; max-width: 800px; padding: 0 20px; z-index: 1; }
        .glitch { font-size: 2.5rem; font-weight: bold; text-transform: uppercase; color: #ff0000; text-shadow: 2px 2px #550000; animation: glitch 1s infinite; }
        @keyframes glitch { 0% { transform: skew(0deg); } 20% { transform: skew(-1deg); } 40% { transform: skew(1.5deg); } 100% { transform: skew(0deg); } }
        
        .manifesto { background: rgba(20, 0, 0, 0.9); border: 1px solid #ff0000; padding: 20px; margin: 30px 0; font-size: 0.9rem; line-height: 1.5; color: #ff6666; text-align: left; box-shadow: 0 0 15px #ff0000; }
        
        .goal-container { width: 100%; max-width: 640px; margin: 20px 0; text-align: left; }
        .goal-bar { width: 100%; height: 18px; background: #200; border: 2px solid #ff0000; position: relative; border-radius: 5px; overflow: hidden; }
        .goal-fill { width: 21%; height: 100%; background: #ff0000; box-shadow: 0 0 20px #ff0000; }
        .goal-text { display: flex; justify-content: space-between; font-size: 0.85rem; margin-top: 8px; color: #ff0000; font-weight: bold; }

        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; z-index: 1; margin-top: 20px; }
        .card { background: rgba(0, 0, 0, 0.9); border: 2px solid #ff0000; padding: 20px; width: 280px; text-align: center; transition: 0.3s; }
        .card:hover { transform: scale(1.02); box-shadow: 0 0 30px #ff0000; }
        .qr-box { background: #fff; padding: 10px; margin: 15px 0; border: 2px solid #ff0000; }
        .qr-box img { width: 100%; }
        .addr { font-size: 0.65rem; word-break: break-all; color: #ff9999; background: #100; padding: 10px; border: 1px dashed #ff0000; }
        .btn { margin-top: 15px; background: #ff0000; border: none; color: #000; padding: 12px; cursor: pointer; width: 100%; font-weight: bold; text-transform: uppercase; }
        .btn:hover { background: #cc0000; color: #fff; }

        /* Панель транзакций (ЯРКАЯ) */
        .tx-panel { width: 100%; max-width: 640px; background: rgba(20,0,0,0.95); border: 2px solid #ff0000; margin: 40px 0; padding: 15px; font-size: 0.8rem; color: #ff0000; z-index: 1; box-shadow: 0 0 20px #ff0000; }
        .tx-list { height: 150px; overflow: hidden; position: relative; }
        .tx-item { padding: 8px 0; border-bottom: 1px solid #400; animation: slideUp 0.4s ease-out; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .tx-amt { color: #fff; font-weight: bold; text-shadow: 0 0 5px #ff0000; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="header">
        <div class="glitch">RED_CHANNEL_IRAN</div>
        <div class="manifesto">
            > ATTENTION: Secured connection established.<br>
            > MISSION: Medicine, food, and communication for Iran.<br>
            > PROTOCOL: Full anonymity. Zero tracking.
        </div>
        
        <div class="goal-container">
            <div class="goal-bar"><div class="goal-fill"></div></div>
            <div class="goal-text">
                <span>GOAL: 2.0 BTC (Humanitarian Aid)</span>
                <span>21.4% COMPLETED</span>
            </div>
        </div>
    </div>

    <div class="container">
        {% for w in W %}
        <div class="card">
            <h3 style="margin:0;">{{ w.n }}</h3>
            <div class="qr-box"><img src="data:image/png;base64,{{ q(w.a) }}"></div>
            <div class="addr" id="a-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn" onclick="copy('a-{{ loop.index }}')">COPY ADDR</button>
        </div>
        {% endfor %}
    </div>

    <div class="tx-panel">
        <div style="border-bottom: 2px solid #ff0000; padding-bottom: 5px; margin-bottom: 10px; font-weight: bold;">[!] LIVE_INCOMING_DATA</div>
        <div class="tx-list" id="tx-list"></div>
    </div>

    <p style="margin: 40px 0; color: #600; font-size: 0.7rem;">STATUS: ENCRYPTED // NO_DATA_RETAINED</p>

    <script>
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const letters = '01';
        const fontSize = 18;
        const drops = Array(Math.floor(canvas.width / fontSize)).fill(1);
        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#ff0000'; // КРАСНЫЙ ЦВЕТ
            ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < drops.length; i++) {
                const text = letters.charAt(Math.floor(Math.random() * letters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 40);

        const txList = document.getElementById('tx-list');
        const amounts = ["0.008 BTC", "0.015 BTC", "12.00 USDT", "240.00 USDT", "0.004 BTC", "95.00 USDT"];
        
        function addTx() {
            const id = Math.random().toString(16).substring(2, 8).toUpperCase();
            const amt = amounts[Math.floor(Math.random() * amounts.length)];
            const item = document.createElement('div');
            item.className = 'tx-item';
            item.innerHTML = `[${new Date().toLocaleTimeString()}] <span style="color:#ff6666">PID_${id}</span> confirmed: <span class="tx-amt">+${amt}</span>`;
            txList.prepend(item);
            if (txList.childNodes.length > 5) txList.removeChild(txList.lastChild);
        }
        setInterval(addTx, 6000); // Чаще - каждые 6 секунд
        addTx(); addTx();

        function copy(id) {
            const t = document.getElementById(id).innerText;
            navigator.clipboard.writeText(t);
            alert('Copied to encrypted clipboard.');
        }
    </script>
</body>
</html>
