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
    <title>TERMINAL | IRAN_FREEDOM_FUND</title>
    <style>
        body { background: #000; color: #0ff; font-family: 'Courier New', monospace; margin: 0; overflow-x: hidden; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.15; }
        .header { margin-top: 40px; text-align: center; max-width: 800px; padding: 0 20px; }
        .glitch { font-size: 2.5rem; font-weight: bold; text-transform: uppercase; color: #0ff; text-shadow: 2px 2px #f05; animation: glitch 1s infinite; }
        @keyframes glitch { 0% { transform: skew(0deg); } 20% { transform: skew(-1deg); } 40% { transform: skew(1deg); } 100% { transform: skew(0deg); } }
        
        .manifesto { background: rgba(10, 10, 10, 0.8); border-left: 3px solid #f05; padding: 20px; margin: 30px 0; font-size: 0.9rem; line-height: 1.5; color: #ccc; text-align: left; }
        
        .goal-container { width: 100%; max-width: 640px; margin: 20px 0; text-align: left; }
        .goal-bar { width: 100%; height: 15px; background: #111; border: 1px solid #0ff; position: relative; border-radius: 10px; overflow: hidden; }
        .goal-fill { width: 18%; height: 100%; background: linear-gradient(90deg, #0ff, #f05); box-shadow: 0 0 15px #0ff; }
        .goal-text { display: flex; justify-content: space-between; font-size: 0.8rem; margin-top: 8px; color: #0ff; }

        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; z-index: 1; margin-top: 20px; }
        .card { background: rgba(5, 5, 5, 0.9); border: 1px solid #0ff; padding: 20px; width: 280px; text-align: center; transition: 0.3s; }
        .card:hover { border-color: #f05; box-shadow: 0 0 20px rgba(255, 0, 85, 0.4); }
        .qr-box { background: #fff; padding: 10px; margin: 15px 0; }
        .qr-box img { width: 100%; }
        .addr { font-size: 0.65rem; word-break: break-all; color: #666; background: #000; padding: 10px; border: 1px dashed #333; }
        .btn { margin-top: 15px; background: none; border: 1px solid #0ff; color: #0ff; padding: 10px; cursor: pointer; width: 100%; font-weight: bold; }
        .btn:hover { background: #0ff; color: #000; }

        /* Секция транзакций */
        .tx-panel { width: 100%; max-width: 640px; background: rgba(10,10,10,0.9); border: 1px solid #333; margin-top: 40px; padding: 15px; font-size: 0.75rem; color: #0f0; }
        .tx-list { height: 120px; overflow: hidden; position: relative; }
        .tx-item { padding: 5px 0; border-bottom: 1px solid #222; animation: slideUp 0.5s ease-out; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .tx-id { color: #f05; }
        .tx-amt { color: #0ff; font-weight: bold; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="header">
        <div class="glitch">FREEDOM_FUND_IRAN</div>
        <div class="manifesto">
            > MISSION_OBJECTIVE: Providing essential support to the people of Iran.<br>
            > ALLOCATION: Medicine, satellite communication, and food supplies.<br>
            > SECURITY: No logs. No tracking. Total blockchain anonymity.
        </div>
        
        <div class="goal-container">
            <div class="goal-bar"><div class="goal-fill"></div></div>
            <div class="goal-text">
                <span>GOAL: 2.0 BTC (Humanitarian Aid)</span>
                <span>18.4% REACHED</span>
            </div>
        </div>
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

    <!-- Панель транзакций -->
    <div class="tx-panel">
        <div style="border-bottom: 1px solid #333; padding-bottom: 5px; margin-bottom: 10px; color: #0ff;">[ LIVE_TRANSACTION_FEED ]</div>
        <div class="tx-list" id="tx-list">
            <!-- Сюда скрипт будет добавлять строки -->
        </div>
    </div>

    <p style="margin: 40px 0; color: #222; font-size: 0.7rem;">STATUS: ENCRYPTED // NO_DATA_RETAINED</p>

    <script>
        // Matrix Effect
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const letters = '01';
        const fontSize = 16;
        const drops = Array(Math.floor(canvas.width / fontSize)).fill(1);
        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0F0'; ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < drops.length; i++) {
                const text = letters.charAt(Math.floor(Math.random() * letters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 33);

        // Fake Transactions
        const txList = document.getElementById('tx-list');
        const amounts = ["0.005 BTC", "0.012 BTC", "45.00 USDT", "120.50 USDT", "0.002 BTC", "80.00 USDT"];
        
        function addTx() {
            const id = Math.random().toString(16).substring(2, 10);
            const amt = amounts[Math.floor(Math.random() * amounts.length)];
            const item = document.createElement('div');
            item.className = 'tx-item';
            item.innerHTML = `[${new Date().toLocaleTimeString()}] <span class="tx-id">tx_${id}...</span> confirmed: <span class="tx-amt">+${amt}</span>`;
            txList.prepend(item);
            if (txList.childNodes.length > 5) txList.removeChild(txList.lastChild);
        }
        setInterval(addTx, 8000); // Новая транзакция каждые 8 секунд
        addTx(); addTx(); // Сразу пара штук

        function copy(id) {
            const t = document.getElementById(id).innerText;
            navigator.clipboard.writeText(t);
            alert('Address copied.');
        }
    </script>
</body>
</html>
