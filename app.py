from flask import Flask, render_template_string
import qrcode, io, base64

app = Flask(__name__)

W = [
    {"n": "BITCOIN", "a": "bc1qrpg5nwr5t8jl3nnavgf2k2v4c43u75c9usxpyk"},
    {"n": "USDT (ERC20)", "a": "0x40745600a508d653549c664d050b90826e4b61ba"}
]

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
    <title>MILITARY_SECURE_TERMINAL</title>
    <style>
        body { 
            margin: 0; padding: 0; 
            background: radial-gradient(circle, #3a3a3a 0%, #1a1a1a 100%); 
            color: #eee; font-family: 'Courier New', monospace; 
            text-align: center; overflow-x: hidden; min-height: 100vh;
            display: flex; flex-direction: column; align-items: center;
        }

        /* ДЕКОР: ДЫРА И РАКЕТЫ */
        .ground-hole {
            position: fixed; bottom: -60px; width: 140%; height: 200px;
            background: radial-gradient(ellipse at center, #050505 0%, #1a1a1a 70%);
            border-radius: 50% 50% 0 0; z-index: 1; border-top: 3px solid #111;
            box-shadow: inset 0 30px 60px #000;
        }
        .rocket-box { position: fixed; top: 120px; width: 45px; height: 300px; z-index: 1; }
        .rocket-body {
            width: 40px; height: 200px;
            background: linear-gradient(90deg, #333 0%, #666 50%, #222 100%);
            border-radius: 50% 50% 10px 10px; position: relative; border: 1px solid #111;
        }
        .rocket-nose {
            position: absolute; top: -35px; left: 0; width: 40px; height: 50px;
            background: linear-gradient(90deg, #800 0%, #f33 50%, #600 100%);
            border-radius: 50% 50% 20% 20%;
        }
        .wing { position: absolute; bottom: 10px; width: 22px; height: 35px; background: #222; border: 1px solid #000; }
        .w-left { left: -18px; clip-path: polygon(100% 0, 0 100%, 100% 100%); }
        .w-right { right: -18px; clip-path: polygon(0 0, 0 100%, 100% 100%); }
        .r-pos-l { left: 6%; transform: rotate(10deg); }
        .r-pos-r { right: 6%; transform: rotate(-10deg); }

        /* КОНТЕНТ */
        .head { padding: 30px; position: relative; z-index: 5; max-width: 700px; }
        .manif { 
            border-left: 4px solid #f05; background: rgba(0,0,0,0.85); 
            padding: 15px; margin: 20px auto; text-align: left; 
            color: #ccc; border: 1px solid #333; font-size: 13px;
        }

        /* ПРОГРЕСС-БАР */
        .goal-bg { 
            width: 300px; height: 12px; border: 1px solid #0ff; 
            margin: 15px auto; position: relative; background: #000; overflow: hidden; 
        }
        .goal-up { height: 100%; background: #0ff; box-shadow: 0 0 15px #0ff; width: 0%; transition: width 1s linear; }

        .wrap { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; padding: 20px; position: relative; z-index: 5; }
        
        .card { 
            background: #111; border: 1px solid #444; 
            padding: 25px; width: 260px; transition: all 0.3s ease; cursor: pointer;
        }
        .card:hover { 
            border-color: #0ff; transform: translateY(-8px);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
        }

        .qr { background: #fff; padding: 8px; margin: 15px 0; }
        .qr img { width: 100%; display: block; }
        .addr { font-size: 9px; word-break: break-all; color: #666; background: #000; padding: 8px; margin-bottom: 15px; }

        .btn { 
            border: 1px solid #0ff; color: #0ff; background: transparent; 
            padding: 12px; width: 100%; font-weight: bold; cursor: pointer;
        }
        .btn:hover { background: #0ff; color: #000; }

        #tx-box { 
            border: 1px solid #333; width: 500px; margin: 20px auto 100px auto;
            padding: 15px; font-size: 11px; color: #0f0; text-align: left; 
            background: rgba(0,0,0,0.9); position: relative; z-index: 5;
        }
    </style>
</head>
<body>
    <div class="rocket-box r-pos-l"><div class="rocket-nose"></div><div class="rocket-body"><div class="wing w-left"></div><div class="wing w-right"></div></div></div>
    <div class="rocket-box r-pos-r"><div class="rocket-nose"></div><div class="rocket-body"><div class="wing w-left"></div><div class="wing w-right"></div></div></div>
    <div class="ground-hole"></div>

    <div class="head">
        <h1 style="text-shadow:0 0 15px #f05; margin:0; color:#f05;">HELP_FUND_TERMINAL</h1>
        <div class="manif">
            > MISSION: Medicine, food, and satellite tools for recovery.<br>
            > STATUS: Encrypted connection // Anonymous channel.
        </div>
        <div class="goal-bg"><div id="f" class="goal-up"></div></div>
        <div style="font-size:12px; color:#0ff;">GOAL: 2.0 BTC (<span id="p">18.4100</span>% reached)</div>
    </div>

    <div class="wrap">
        {% for w in W %}
        <div class="card" onclick="copyIt('cp-{{ loop.index }}')">
            <h3 style="margin:0; color:#0ff;">{{ w.n }}</h3>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}"></div>
            <div class="addr" id="cp-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn">COPY ADDRESS</button>
        </div>
        {% endfor %}
    </div>

    <div id="tx-box">
        <div style="border-bottom:1px solid #444; margin-bottom:10px; color:#0ff;">[ LIVE_DATA_STREAM ]</div>
        <div id="l"></div>
    </div>

    <script>
        function startLiveSystem() {
            const baseValue = 18.4100;
            const growthDaily = 0.35;
            let startKey = 'iran_fund_final_v5';
            let startTime = localStorage.getItem(startKey) || Date.now();
            localStorage.setItem(startKey, startTime);

            function update() {
                const diffDays = (Date.now() - parseInt(startTime)) / 86400000;
                let current = Math.min(99.85, baseValue + (diffDays * growthDaily));
                document.getElementById('p').innerText = current.toFixed(4);
                document.getElementById('f').style.width = current + '%';
            }
            setInterval(update, 1000); update();
        }
        startLiveSystem();

        function addTx(){
            const l=document.getElementById('l'), e=document.createElement('div');
            e.innerHTML=`> [${new Date().toLocaleTimeString()}] Incoming confirmed: +${(Math.random()*0.01).toFixed(4)} BTC...`;
            l.prepend(e); 
            if(l.childNodes.length > 5) l.removeChild(l.lastChild);
            setTimeout(addTx, Math.random() * 20000 + 25000);
        }
        setTimeout(addTx, 2000);

        function copyIt(id) {
            const el = document.getElementById(id);
            navigator.clipboard.writeText(el.innerText);
            alert("Адрес успешно скопирован!");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, g=g_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
