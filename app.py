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
    <title>TERMINAL_WAR_ZONE</title>
    <style>
        body { 
            margin: 0; padding: 0; 
            background: radial-gradient(circle, #444 0%, #111 100%); 
            color: #fff; font-family: 'Courier New', monospace; 
            text-align: center; overflow-x: hidden; min-height: 100vh;
        }

        /* ЗЕМЛЯ ВНИЗУ (РАЗБИТАЯ) */
        .ground {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 80px;
            background: #000; z-index: 1;
            border-top: 2px solid #f05;
            box-shadow: 0 -10px 50px rgba(255, 0, 85, 0.6);
        }
        .cracks {
            position: absolute; width: 100%; height: 100%;
            background-image: linear-gradient(45deg, transparent 45%, #f20 48%, #f20 52%, transparent 55%);
            background-size: 50px 50px; opacity: 0.3;
        }

        /* РАКЕТЫ СВЕРХУ ВНИЗ */
        .rocket-down {
            position: fixed; width: 4px; height: 100px;
            background: linear-gradient(to bottom, transparent, #fff, #f05);
            z-index: 0; filter: blur(1px);
        }
        .rocket-down::after {
            content: ''; position: absolute; bottom: 0; left: -3px;
            width: 10px; height: 10px; background: #fff; border-radius: 50%;
            box-shadow: 0 0 20px #fff, 0 0 40px #f05;
        }

        .rd-1 { left: 10%; top: -150px; animation: fall 3s infinite linear; }
        .rd-2 { left: 20%; top: -150px; animation: fall 4.5s infinite linear 1s; }
        .rd-3 { right: 10%; top: -150px; animation: fall 3.5s infinite linear 0.5s; }
        .rd-4 { right: 25%; top: -150px; animation: fall 5s infinite linear 2s; }

        @keyframes fall {
            0% { transform: translateY(0) rotate(15deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(110vh) rotate(15deg); opacity: 0; }
        }

        .head { padding: 40px 20px; position: relative; z-index: 2; }
        .manif { 
            border: 1px solid #f05; background: rgba(0,0,0,0.9); 
            padding: 20px; max-width: 600px; margin: 20px auto; text-align: left; 
            box-shadow: 0 0 30px rgba(255, 0, 85, 0.3);
        }

        .goal-bg { 
            width: 300px; height: 12px; border: 1px solid #0ff; 
            margin: 20px auto; position: relative; background: #000;
        }
        .goal-up { height: 100%; background: #0ff; box-shadow: 0 0 20px #0ff; width: 0%; transition: width 2s; }

        .wrap { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; padding: 20px; position: relative; z-index: 2; margin-bottom: 100px; }
        
        .card { 
            background: rgba(15,15,15,0.95); border: 1px solid #333; 
            padding: 25px; width: 260px; border-bottom: 4px solid #f05;
            transition: 0.3s;
        }
        .card:hover { transform: translateY(-5px); border-color: #0ff; }

        .qr { background: #fff; padding: 10px; margin: 15px 0; }
        .qr img { width: 100%; display: block; }

        .addr { font-size: 10px; word-break: break-all; color: #555; margin-bottom: 20px; padding: 8px; background: #000; }

        .btn { 
            border: 1px solid #0ff; color: #0ff; background: transparent; 
            padding: 12px; cursor: pointer; width: 100%; font-weight: bold; 
            transition: 0.3s;
        }
        .btn:hover { background: #0ff; color: #000; }

        #tx-box { 
            border: 1px solid #444; max-width: 550px; margin: 20px auto; 
            padding: 15px; font-size: 11px; color: #0f0; text-align: left; 
            background: rgba(0,0,0,0.9); position: relative; z-index: 2;
        }
    </style>
</head>
<body>
    <div class="ground"><div class="cracks"></div></div>
    
    <div class="rocket-down rd-1"></div>
    <div class="rocket-down rd-2"></div>
    <div class="rocket-down rd-3"></div>
    <div class="rocket-down rd-4"></div>

    <div class="head">
        <h1 style="text-shadow: 0 0 15px #f05; margin: 0; font-size: 2.2rem;">AIR_STRIKE_RELIEF</h1>
        <div class="manif">
            > MISSION: EMERGENCY_SUPPLY_LINE<br>
            > STATUS: UNDER_BOMBARDMENT<br>
            > CHANNEL: ENCRYPTED_V4
        </div>
        <div class="goal-bg"><div id="f" class="goal-up"></div></div>
        <div style="font-size:13px; color:#0ff;">FUNDS_COLLECTED: <span id="p">18.4100</span>%</div>
    </div>

    <div class="wrap">
        {% for w in W %}
        <div class="card">
            <h3 style="margin:0; color:#0ff;">{{ w.n }}</h3>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}"></div>
            <div class="addr" id="cp-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn" onclick="copyIt('cp-{{ loop.index }}')">COPY_ADDR</button>
        </div>
        {% endfor %}
    </div>

    <div id="tx-box">
        <div style="color: #f05; font-weight: bold; font-size: 10px;">[ SATELLITE_FEED_INCOMING ]</div>
        <div id="l"></div>
    </div>

    <script>
        function startLiveSystem() {
            const baseValue = 18.4100;
            const growthDaily = 0.35;
            let startKey = 'iran_fund_v20';
            let startTime = localStorage.getItem(startKey) || Date.now();
            localStorage.setItem(startKey, startTime);

            function update() {
                const now = Date.now();
                const diffDays = (now - parseInt(startTime)) / 86400000;
                let current = Math.min(99.85, baseValue + (diffDays * growthDaily));
                document.getElementById('p').innerText = current.toFixed(4);
                document.getElementById('f').style.width = current + '%';
            }
            setInterval(update, 1000);
            update();
        }
        startLiveSystem();

        function addTx(){
            const l=document.getElementById('l'), e=document.createElement('div');
            const amount = (Math.random() * 0.01).toFixed(4);
            e.innerHTML=`> [${new Date().toLocaleTimeString()}] RECEIVED: +${amount} BTC... OK`;
            l.prepend(e); 
            if(l.childNodes.length > 4) l.removeChild(l.lastChild);
            setTimeout(addTx, Math.random() * 15000 + 10000);
        }
        setTimeout(addTx, 1500);

        function copyIt(id) {
            const el = document.getElementById(id);
            navigator.clipboard.writeText(el.innerText);
            const old = el.innerText;
            el.innerText = "COPIED!";
            setTimeout(() => { el.innerText = old; }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, g=g_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
