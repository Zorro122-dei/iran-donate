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
    <title>AIR_STRIKE_LIVE</title>
    <style>
        body { 
            margin: 0; 
            padding: 0;
            color: #fff; 
            font-family: 'Courier New', monospace; 
            text-align: center;
            min-height: 100vh;
            /* ФОН С РАКЕТАМИ */
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), 
                        url('https://pixabay.com');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }
        
        .overlay-fx {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: repeating-linear-gradient(0deg, rgba(0,0,0,0.1) 0px, rgba(0,0,0,0.1) 1px, transparent 2px);
            pointer-events: none; z-index: 5;
        }

        .head { padding: 40px 20px; position: relative; z-index: 2; }
        
        .manif { 
            border: 1px solid #f05; 
            background: rgba(10,10,10,0.9); 
            padding: 20px; 
            max-width: 650px; 
            margin: 20px auto; 
            text-align: left; 
            box-shadow: 0 0 20px rgba(255, 0, 85, 0.4);
        }

        .goal-bg { 
            width: 320px; height: 14px; border: 1px solid #0ff; 
            margin: 20px auto; position: relative; background: #000;
        }
        .goal-up { height: 100%; background: #0ff; box-shadow: 0 0 20px #0ff; width: 0%; transition: width 2s ease-in-out; }

        .wrap { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; padding: 20px; position: relative; z-index: 2; }
        
        .card { 
            background: rgba(0,0,0,0.95); 
            border: 1px solid #333; 
            padding: 30px; 
            width: 280px; 
            border-top: 4px solid #f05;
        }

        .qr { background: #fff; padding: 10px; margin: 15px 0; }
        .qr img { width: 100%; display: block; }

        .addr { 
            font-size: 10px; word-break: break-all; color: #666; 
            margin-bottom: 20px; padding: 10px; background: #050505; border: 1px solid #222;
        }

        .btn { 
            border: 1px solid #0ff; color: #0ff; background: transparent; 
            padding: 14px; cursor: pointer; width: 100%; font-weight: bold; 
            text-transform: uppercase; transition: 0.3s;
        }
        .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 20px #0ff; }

        #tx-box { 
            border: 1px solid #444; max-width: 600px; margin: 50px auto; 
            padding: 20px; font-size: 11px; color: #0f0; text-align: left; 
            background: rgba(0,0,0,0.9); position: relative; z-index: 2;
        }
    </style>
</head>
<body>
    <div class="overlay-fx"></div>
    <div class="head">
        <h1 style="text-shadow: 0 0 15px #f05; margin: 0; font-size: 3rem;">AIR_STRIKE_FUND</h1>
        <div class="manif">
            > [STATUS]: ROCKET_SYSTEMS_READY<br>
            > [SECTOR]: ALL_FRONT_LINES<br>
            > [ENCRYPTION]: MILITARY_GRADE_SECURED
        </div>
        <div class="goal-bg"><div id="f" class="goal-up"></div></div>
        <div style="font-size:14px; color:#0ff;">COLLECTION_PROGRESS: <span id="p">18.4100</span>%</div>
    </div>

    <div class="wrap">
        {% for w in W %}
        <div class="card">
            <h2 style="margin:0; color:#0ff; font-size: 18px;">{{ w.n }}</h2>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}"></div>
            <div class="addr" id="cp-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn" onclick="copyIt('cp-{{ loop.index }}')">COPY_ADDRESS</button>
        </div>
        {% endfor %}
    </div>

    <div id="tx-box">
        <div style="color: #f05; font-weight: bold; margin-bottom: 10px;">[ SATELLITE_LINK_ACTIVE ]</div>
        <div id="l"></div>
    </div>

    <script>
        function startLiveSystem() {
            const baseValue = 18.4100;
            const growthDaily = 0.35;
            let startKey = 'iran_fund_v10';
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
            e.innerHTML=`> [${new Date().toLocaleTimeString()}] INCOMING: +${amount} BTC... DONE`;
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
            el.style.color = "#fff";
            setTimeout(() => { 
                el.innerText = old; 
                el.style.color = "#666"; 
            }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, g=g_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
