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
    <title>TERMINAL_STRIKE_ZONE</title>
    <style>
        body { 
            margin: 0; padding: 0; 
            background: #2c2c2c; /* Серый фон */
            color: #fff; font-family: 'Courier New', monospace; 
            text-align: center; overflow: hidden; height: 100vh;
            display: flex; flex-direction: column; align-items: center;
        }

        /* РИСУНОК ЗЕМЛИ С ДЫРКОЙ ВНИЗУ */
        .ground-hole {
            position: fixed; bottom: -50px; width: 120%; height: 150px;
            background: #111; border-radius: 50% 50% 0 0;
            border-top: 4px solid #000; z-index: 1;
            box-shadow: inset 0 20px 50px #000, 0 -10px 30px rgba(0,0,0,0.5);
        }

        /* РИСУНКИ РАКЕТ ПО БОКАМ */
        .side-rocket {
            position: fixed; top: 150px; width: 40px; height: 180px;
            background: #1a1a1a; border: 2px solid #000;
            border-radius: 50% 50% 5px 5px; z-index: 1;
        }
        .side-rocket::before { /* Носовая часть */
            content: ''; position: absolute; top: -30px; left: -2px;
            width: 40px; height: 40px; background: #c00; 
            border: 2px solid #000; border-radius: 50% 50% 0 0;
        }
        .side-rocket::after { /* Стабилизаторы */
            content: ''; position: absolute; bottom: 0; left: -10px;
            width: 56px; height: 20px; background: #333; border: 2px solid #000;
        }
        
        .r-left { left: 5%; transform: rotate(15deg); }
        .r-right { right: 5%; transform: rotate(-15deg); }

        .head { padding: 30px; position: relative; z-index: 2; }
        .manif { 
            background: rgba(0,0,0,0.7); border: 1px solid #444; 
            padding: 15px; max-width: 500px; margin: 10px auto; 
            text-align: left; font-size: 13px; color: #ccc;
        }

        .goal-bg { 
            width: 250px; height: 10px; border: 1px solid #0ff; 
            margin: 15px auto; background: #000; position: relative;
        }
        .goal-up { height: 100%; background: #0ff; width: 0%; transition: width 2s; }

        .wrap { display: flex; justify-content: center; gap: 20px; padding: 20px; position: relative; z-index: 2; }
        
        .card { 
            background: #1a1a1a; border: 2px solid #000; 
            padding: 20px; width: 240px; box-shadow: 5px 5px 0px #000;
        }

        .qr { background: #fff; padding: 8px; margin: 10px 0; border: 1px solid #000; }
        .qr img { width: 100%; display: block; }

        .addr { font-size: 9px; word-break: break-all; color: #888; background: #000; padding: 5px; margin-bottom: 15px; }

        .btn { 
            border: 1px solid #0ff; color: #0ff; background: #000; 
            padding: 10px; cursor: pointer; width: 100%; font-weight: bold; 
        }
        .btn:active { background: #0ff; color: #000; }

        #tx-box { 
            border: 1px solid #333; width: 450px; margin-top: 10px;
            padding: 10px; font-size: 10px; color: #0f0; text-align: left; 
            background: #000; position: relative; z-index: 2;
        }
    </style>
</head>
<body>
    <!-- Статичные элементы декора -->
    <div class="side-rocket r-left"></div>
    <div class="side-rocket r-right"></div>
    <div class="ground-hole"></div>

    <div class="head">
        <h1 style="margin: 0; color: #f05; text-transform: uppercase; letter-spacing: 2px;">Target_Zone_Fund</h1>
        <div class="manif">
            > MISSION: EMERGENCY_SUPPLY<br>
            > AREA: SECTOR_7_STRIKE<br>
            > STATUS: CONNECTION_SECURE
        </div>
        <div class="goal-bg"><div id="f" class="goal-up"></div></div>
        <div style="font-size:12px; color:#0ff;">PROGRESS: <span id="p">18.4100</span>%</div>
    </div>

    <div class="wrap">
        {% for w in W %}
        <div class="card">
            <h4 style="margin:0; color:#0ff;">{{ w.n }}</h4>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}"></div>
            <div class="addr" id="cp-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn" onclick="copyIt('cp-{{ loop.index }}')">COPY_ADDRESS</button>
        </div>
        {% endfor %}
    </div>

    <div id="tx-box">
        <div style="color: #444; border-bottom: 1px solid #222; margin-bottom: 5px;">[ LOG_STREAM ]</div>
        <div id="l"></div>
    </div>

    <script>
        // Твоя логика счетчика
        function startLiveSystem() {
            const baseValue = 18.4100;
            const growthDaily = 0.35;
            let startKey = 'iran_fund_vfinal';
            let startTime = localStorage.getItem(startKey) || Date.now();
            localStorage.setItem(startKey, startTime);

            function update() {
                const now = Date.now();
                const diffDays = (now - parseInt(startTime)) / 86400000;
                let current = Math.min(99.85, baseValue + (diffDays * growthDaily));
                document.getElementById('p').innerText = current.toFixed(4);
                document.getElementById('f').style.width = current + '%';
            }
            setInterval(update, 1000); update();
        }
        startLiveSystem();

        function addTx(){
            const l=document.getElementById('l'), e=document.createElement('div');
            e.innerHTML=`> [${new Date().toLocaleTimeString()}] RECEIVED: +${(Math.random()*0.01).toFixed(4)} BTC`;
            l.prepend(e); 
            if(l.childNodes.length > 3) l.removeChild(l.lastChild);
            setTimeout(addTx, 15000);
        }
        addTx();

        function copyIt(id) {
            const el = document.getElementById(id);
            navigator.clipboard.writeText(el.innerText);
            alert("Скопировано!");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, g=g_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
