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
    <title>AIR_STRIKE_TERMINAL</title>
    <style>
        body { 
            margin: 0; padding: 0; background: #0a0a0a; color: #fff; 
            font-family: 'Courier New', monospace; text-align: center;
            overflow-x: hidden; min-height: 100vh;
        }

        /* РИСУЕМ РАКЕТЫ ЧЕРЕЗ CSS */
        .rocket {
            position: fixed; width: 2px; height: 150px;
            background: linear-gradient(to top, transparent, #f05, #ff0);
            filter: blur(1px); z-index: 0; opacity: 0.8;
        }
        .rocket::before {
            content: ''; position: absolute; top: 0; left: -2px;
            width: 6px; height: 6px; background: #fff; border-radius: 50%;
            box-shadow: 0 0 15px #fff, 0 0 30px #f05;
        }
        
        /* Ракета слева */
        .r-left { left: 10%; bottom: -200px; animation: launch 4s infinite ease-in; }
        /* Ракета справа */
        .r-right { right: 15%; bottom: -300px; animation: launch 6s infinite ease-in 1s; }
        /* Ракета по центру */
        .r-mid { left: 50%; bottom: -250px; animation: launch 5s infinite ease-in 2s; }

        @keyframes launch {
            0% { transform: translateY(0) scaleY(1); opacity: 0; }
            10% { opacity: 1; }
            100% { transform: translateY(-120vh) scaleY(2); opacity: 0; }
        }

        .head { padding: 40px 20px; position: relative; z-index: 2; }
        
        .manif { 
            border: 1px solid #f05; background: rgba(0,0,0,0.9); 
            padding: 20px; max-width: 600px; margin: 20px auto; text-align: left; 
            box-shadow: 0 0 30px rgba(255, 0, 85, 0.2);
        }

        .goal-bg { 
            width: 300px; height: 12px; border: 1px solid #0ff; 
            margin: 20px auto; position: relative; background: #000;
        }
        .goal-up { height: 100%; background: #0ff; box-shadow: 0 0 20px #0ff; width: 0%; transition: width 2s; }

        .wrap { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; padding: 20px; position: relative; z-index: 2; }
        
        .card { 
            background: rgba(20,20,20,0.95); border: 1px solid #333; 
            padding: 25px; width: 260px; border-top: 4px solid #f05;
        }

        .qr { background: #fff; padding: 10px; margin: 15px 0; }
        .qr img { width: 100%; display: block; }

        .addr { 
            font-size: 10px; word-break: break-all; color: #666; 
            margin-bottom: 20px; padding: 10px; background: #000; border: 1px solid #222;
        }

        .btn { 
            border: 1px solid #0ff; color: #0ff; background: transparent; 
            padding: 12px; cursor: pointer; width: 100%; font-weight: bold; 
            text-transform: uppercase; transition: 0.3s;
        }
        .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 20px #0ff; }

        #tx-box { 
            border: 1px solid #444; max-width: 550px; margin: 40px auto; 
            padding: 15px; font-size: 11px; color: #0f0; text-align: left; 
            background: rgba(0,0,0,0.95); position: relative; z-index: 2;
        }
    </style>
</head>
<body>
    <!-- Анимированные ракеты -->
    <div class="rocket r-left"></div>
    <div class="rocket r-mid"></div>
    <div class="rocket r-right"></div>

    <div class="head">
        <h1 style="text-shadow: 0 0 15px #f05; margin: 0; font-size: 2.5rem;">AIR_STRIKE_FUND</h1>
        <div class="manif">
            > [STATUS]: BALLISTIC_SYSTEMS_ONLINE<br>
            > [SECTOR]: SECURED_ANONYMOUS_LINK<br>
            > [LOG]: WAITING_FOR_INCOMING_DATA...
        </div>
        <div class="goal-bg"><div id="f" class="goal-up"></div></div>
        <div style="font-size:14px; color:#0ff;">TOTAL_PROGRESS: <span id="p">18.4100</span>%</div>
    </div>

    <div class="wrap">
        {% for w in W %}
        <div class="card">
            <h3 style="margin:0; color:#0ff;">{{ w.n }}</h3>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}"></div>
            <div class="addr" id="cp-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn" onclick="copyIt('cp-{{ loop.index }}')">COPY_ADDRESS</button>
        </div>
        {% endfor %}
    </div>

    <div id="tx-box">
        <div style="color: #f05; font-weight: bold; margin-bottom: 5px;">[ DATA_STREAM ]</div>
        <div id="l"></div>
    </div>

    <script>
        function startLiveSystem() {
            const baseValue = 18.4100;
            const growthDaily = 0.35;
            let startKey = 'iran_fund_v15';
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
            if(l.childNodes.length > 5) l.removeChild(l.lastChild);
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
