from flask import Flask, render_template_string
import qrcode, io, base64

app = Flask(__name__)

WALLETS = [
    {"n": "BITCOIN", "a": "bc1qrpg5nwr5t8jl3nnavgf2k2v4c43u75c9usxpyk", "sym": "BTC"},
    {"n": "USDT (ERC20)", "a": "0x40745600a508d653549c664d050b90826e4b61ba", "sym": "USDT"}
]

for w in WALLETS:
    img = qrcode.make(w['a'])
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    w['qr'] = base64.b64encode(buf.getvalue()).decode()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TERMINAL_OPERATIONAL</title>
    <style>
        :root { --neon: #ff3e3e; --accent: #ffae00; --bg: #050505; }
        
        body { 
            background: var(--bg); 
            color: #fff; 
            font-family: 'Segoe UI', Tahoma, sans-serif; 
            margin: 0; 
            min-height: 100vh;
            /* ФОНОВОЕ ИЗОБРАЖЕНИЕ */
            background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                              url('https://unsplash.com');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* Эффект помех (Grain) */
        body::before {
            content: "";
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: url(https://vercel.app);
            opacity: 0.05; pointer-events: none; z-index: 10;
        }

        .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; position: relative; z-index: 2; }

        .header { text-align: center; margin-bottom: 50px; }
        
        /* Глитч-заголовок */
        .glitch {
            font-size: 3rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 5px;
            color: var(--neon);
            text-shadow: 2px 2px 0px var(--accent);
            position: relative;
        }

        .manifesto { 
            background: rgba(255, 0, 0, 0.1); 
            border: 1px solid var(--neon);
            padding: 20px; 
            margin: 25px 0; 
            font-family: monospace;
            backdrop-filter: blur(5px);
        }

        /* Прогресс-бар */
        .progress-box { margin: 30px 0; font-family: monospace; color: var(--accent); }
        .bar-bg { background: rgba(255,255,255,0.1); height: 10px; border-radius: 5px; overflow: hidden; margin-top: 10px; border: 1px solid #444; }
        .bar-fill { height: 100%; background: linear-gradient(90deg, var(--neon), var(--accent)); width: 0%; transition: width 2s cubic-bezier(0.1, 0, 0, 1); }

        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
        
        .card { 
            background: rgba(20, 20, 20, 0.7); 
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.1); 
            padding: 30px; 
            text-align: center;
            border-top: 4px solid var(--neon);
            transition: 0.3s;
        }
        .card:hover { transform: translateY(-5px); border-color: var(--accent); }

        .qr-wrap { background: #fff; padding: 15px; margin-bottom: 20px; display: inline-block; border-radius: 4px; }
        .qr-wrap img { width: 180px; display: block; }

        .addr { 
            font-family: monospace; font-size: 12px; background: #000; padding: 12px; 
            border: 1px solid #333; word-break: break-all; margin-bottom: 20px; color: #aaa;
        }

        .btn { 
            background: var(--neon); border: none; color: #fff; padding: 15px; 
            width: 100%; font-weight: bold; cursor: pointer; clip-path: polygon(0 0, 100% 0, 95% 100%, 5% 100%);
            transition: 0.3s;
        }
        .btn:hover { background: var(--accent); color: #000; }

        #feed { 
            margin-top: 50px; padding: 20px; background: rgba(0,0,0,0.8); 
            border-left: 3px solid var(--accent); font-family: monospace; font-size: 13px;
        }
        .tx-line { color: #0f0; margin: 5px 0; opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="glitch">WAR_RECOVERY_FUND</h1>
            <div class="manifesto">
                [SYSTEM]: ПОДКЛЮЧЕНИЕ ЗАЩИЩЕНО... <br>
                [TARGET]: ПОДДЕРЖКА, МЕДИКАМЕНТЫ, СВЯЗЬ <br>
                [ANON]: ТРАНЗАКЦИИ НЕ ОТСЛЕЖИВАЮТСЯ
            </div>
            
            <div class="progress-box">
                ТЕКУЩИЙ СБОР: <span id="pct">0</span>% (<span id="btc_val">0</span> BTC)
                <div class="bar-bg"><div class="bar-fill" id="bar"></div></div>
            </div>
        </header>

        <div class="grid">
            {% for w in wallets %}
            <div class="card">
                <h3 style="margin-top:0; color: var(--accent);">{{ w.n }}</h3>
                <div class="qr-wrap">
                    <img src="data:image/png;base64,{{ w.qr }}" alt="QR">
                </div>
                <div class="addr" id="addr-{{ loop.index }}">{{ w.a }}</div>
                <button class="btn" onclick="copy('addr-{{ loop.index }}')">КОПИРОВАТЬ АДРЕС</button>
            </div>
            {% endfor %}
        </div>

        <div id="feed">
            <div style="color:var(--accent); font-weight:bold; margin-bottom:10px;">> LIVE_OPERATIONS_LOG:</div>
            <div id="log"></div>
        </div>
    </div>

    <script>
        function updateCounter() {
            const startPct = 18.41;
            const dailyInc = 0.35;
            const initTime = parseInt(localStorage.getItem('init_v4') || Date.now());
            if(!localStorage.getItem('init_v4')) localStorage.setItem('init_v4', initTime);
            
            const days = (Date.now() - initTime) / 86400000;
            const current = Math.min(99.85, startPct + (days * dailyInc));
            
            document.getElementById('pct').innerText = current.toFixed(4);
            document.getElementById('btc_val').innerText = (2.0 * (current/100)).toFixed(4);
            document.getElementById('bar').style.width = current + '%';
        }
        setInterval(updateCounter, 2000);
        updateCounter();

        function addTx() {
            const log = document.getElementById('log');
            const el = document.createElement('div');
            el.className = 'tx-line';
            const val = (Math.random() * 0.05).toFixed(4);
            el.innerHTML = `> [${new Date().toLocaleTimeString()}] ВХОДЯЩИЙ ПЛАТЕЖ: +${val} ${Math.random() > 0.5 ? 'BTC' : 'USDT'}... ПОДТВЕРЖДЕНО`;
            log.prepend(el);
            if(log.childNodes.length > 5) log.removeChild(log.lastChild);
            setTimeout(addTx, Math.random() * 15000 + 10000);
        }
        addTx();

        function copy(id) {
            const el = document.getElementById(id);
            const originalText = el.innerText;
            navigator.clipboard.writeText(originalText);
            el.innerText = 'СКОПИРОВАНО В БУФЕР!';
            el.style.color = '#fff';
            setTimeout(() => { 
                el.innerText = originalText;
                el.style.color = '#aaa';
            }, 1500);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, wallets=WALLETS)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
