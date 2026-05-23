from flask import Flask, render_template_string
import qrcode, io, base64, datetime

app = Flask(__name__)

# --- РЕКВИЗИТЫ ---
W = [
    {"n": "BITCOIN", "a": "bc1qrpg5nwr5t8jl3nnavgf2k2v4c43u75c9usxpyk"},
    {"n": "USDT (ERC20)", "a": "0x40745600a508d653549c664d050b90826e4b61ba"}
]

# --- НАСТРОЙКИ (Скорость возвращена на 0.35) ---
BASE_VALUE = 18.4100  
GROWTH_PER_DAY = 0.35  
START_TIME_TS = 1779538200 # Таймштамп запуска (23.05.2026 15:10)

def g_qr(t):
    img = qrcode.make(t)
    b = io.BytesIO()
    img.save(b, "PNG")
    return base64.b64encode(b.getvalue()).decode()

H = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TERMINAL_OPERATIONAL</title>
    <style>
        body { margin:0; padding:0; background:radial-gradient(circle, #3a3a3a 0%, #1a1a1a 100%); color:#eee; font-family:monospace; text-align:center; min-height:100vh; display:flex; flex-direction:column; align-items:center; overflow-x:hidden; }
        .ground-hole { position:fixed; bottom:-60px; width:140%; height:200px; background:radial-gradient(ellipse at center, #050505 0%, #1a1a1a 70%); border-radius:50% 50% 0 0; z-index:1; box-shadow:inset 0 30px 60px #000; }
        .rocket-box { position:fixed; top:120px; width:45px; height:300px; z-index:1; }
        .rocket-body { width:40px; height:200px; background:linear-gradient(90deg, #333 0%, #666 50%, #222 100%); border-radius:50% 50% 10px 10px; position:relative; border:1px solid #111; }
        .rocket-nose { position:absolute; top:-35px; left:0; width:40px; height:50px; background:linear-gradient(90deg, #800 0%, #f33 50%, #600 100%); border-radius:50% 50% 20% 20%; }
        .wing { position:absolute; bottom:10px; width:22px; height:35px; background:#222; border:1px solid #000; }
        .w-left { left:-18px; clip-path:polygon(100% 0, 0 100%, 100% 100%); }
        .w-right { right:-18px; clip-path:polygon(0 0, 0 100%, 100% 100%); }
        .r-pos-l { left:6%; transform:rotate(10deg); }
        .r-pos-r { right:6%; transform:rotate(-10deg); }
        .head { padding:30px; position:relative; z-index:5; }
        .manif { border-left:4px solid #f05; background:rgba(0,0,0,0.8); padding:15px; margin:20px auto; text-align:left; font-size:13px; border:1px solid #333; max-width:600px; }
        
        .goal-bg { width:300px; height:12px; border:1px solid #0ff; margin:15px auto; background:#000; overflow:hidden; position:relative; }
        #bar { height:100%; background:#0ff; box-shadow:0 0 15px #0ff; width:0%; transition: width 0.5s ease-in-out; }
        
        .wrap { display:flex; flex-wrap:wrap; justify-content:center; gap:30px; padding:20px; position:relative; z-index:5; }
        .card { background:#111; border:1px solid #444; padding:25px; width:260px; transition:0.3s; cursor:pointer; }
        .card:hover { border-color:#0ff; transform:translateY(-8px); box-shadow:0 0 30px rgba(0,255,255,0.3); }
        .qr { background:#fff; padding:8px; margin:15px 0; }
        .qr img { width:100%; display:block; }
        .addr { font-size:9px; word-break:break-all; color:#666; background:#000; padding:8px; margin-bottom:15px; transition:0.2s; }
        .addr.active { color:#fff; background:#f05; }
        .btn { border:1px solid #0ff; color:#0ff; background:transparent; padding:12px; width:100%; font-weight:bold; pointer-events:none; }
        #tx-box { border:1px solid #333; width:500px; margin:20px auto 100px auto; padding:15px; font-size:11px; color:#0f0; text-align:left; background:rgba(0,0,0,0.9); position:relative; z-index:5; }
    </style>
</head>
<body>
    <div class="rocket-box r-pos-l"><div class="rocket-nose"></div><div class="rocket-body"><div class="wing w-left"></div><div class="wing w-right"></div></div></div>
    <div class="rocket-box r-pos-r"><div class="rocket-nose"></div><div class="rocket-body"><div class="wing w-right"></div></div></div>
    <div class="ground-hole"></div>

    <div class="head">
        <h1 style="text-shadow:0 0 15px #f05; margin:0; color:#f05;">HELP_FUND_TERMINAL</h1>
        <div class="manif">
            > MISSION: Medicine, food, and satellite tools for recovery.<br>
            > STATUS: Encrypted connection // Anonymous channel.
        </div>
        <div class="goal-bg"><div id="bar"></div></div>
        <div style="font-size:12px; color:#0ff;">GOAL: 2.0 BTC (<span id="pct_text">18.4100</span>% reached)</div>
    </div>

    <div class="wrap">
        {% for w in W %}
        <div class="card" onclick="copyIt('cp-{{ loop.index }}')">
            <h3 style="margin:0; color:#0ff;">{{ w.n }}</h3>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}"></div>
            <div class="addr" id="cp-{{ loop.index }}">{{ w.a }}</div>
            <div class="btn">CLICK TO COPY</div>
        </div>
        {% endfor %}
    </div>

    <div id="tx-box">
        <div style="border-bottom:1px solid #444; margin-bottom:10px; color:#0ff;">[ LIVE_DATA_STREAM ]</div>
        <div id="l"></div>
    </div>

    <script>
        const base = {{ base }};
        const growth = {{ growth }};
        const start = {{ start }};

        function update() {
            const now = Math.floor(Date.now() / 1000);
            const diffDays = (now - start) / 86400;
            let current = base + (diffDays * growth);
            if (current > 99.85) current = 99.85;

            document.getElementById('bar').style.width = current + '%';
            document.getElementById('pct_text').innerText = current.toFixed(4);
        }
        setInterval(update, 1000);
        update();

        function addTx(){
            const l=document.getElementById('l'), e=document.createElement('div');
            e.innerHTML=`> [${new Date().toLocaleTimeString()}] Incoming confirmed: +${(Math.random()*0.01).toFixed(4)} BTC...`;
            l.prepend(e); 
            if(l.childNodes.length > 5) l.removeChild(l.lastChild);
            setTimeout(addTx, Math.random() * 15000 + 10000);
        }
        setTimeout(addTx, 2000);

        function copyIt(id) {
            const el = document.getElementById(id);
            const textArea = document.createElement("textarea");
            textArea.value = el.innerText;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand("copy");
            document.body.removeChild(textArea);
            el.classList.add('active');
            setTimeout(() => { el.classList.remove('active'); }, 300);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(H, W=W, g=g_qr, base=BASE_VALUE, growth=GROWTH_PER_DAY, start=START_TIME_TS)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
