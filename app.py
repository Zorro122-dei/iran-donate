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
    <title>TERMINAL_STRIKE_V3</title>
    <style>
        body { 
            margin: 0; 
            padding: 0;
            color: #fff; 
            font-family: 'Courier New', monospace; 
            text-align: center;
            min-height: 100vh;
            /* КАРТИНКА С ЛЕТЯЩИМИ РАКЕТАМИ */
            background: radial-gradient(circle, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.9) 100%), 
                        url('https://unsplash.com');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            overflow-x: hidden;
        }
        
        .head { padding: 40px 20px; position: relative; z-index: 2; }
        
        .manif { 
            border-left: 5px solid #f05; 
            background: rgba(0,0,0,0.85); 
            backdrop-filter: blur(8px);
            padding: 20px; 
            max-width: 650px; 
            margin: 20px auto; 
            text-align: left; 
            font-size: 14px;
            box-shadow: 10px 10px 0px rgba(255, 0, 85, 0.2);
        }

        .goal-bg { 
            width: 320px; height: 12px; border: 1px solid #0ff; 
            margin: 20px auto; position: relative; background: #000;
        }
        .goal-up { height: 100%; background: #0ff; box-shadow: 0 0 20px #0ff; width: 0%; transition: width 2s ease-in-out; }

        .wrap { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; padding: 20px; position: relative; z-index: 2; }
        
        .card { 
            background: rgba(15,15,15,0.92); 
            border: 1px solid #333; 
            padding: 30px; 
            width: 280px; 
            border-bottom: 4px solid #f05;
            transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .card:hover { transform: scale(1.05); border-color: #0ff; }

        .qr { background: #fff; padding: 12px; margin: 20px 0; border-radius: 3px; }
        .qr img { width: 100%; display: block; }

        .addr { 
            font-size: 10px; word-break: break-all; color: #777; 
            margin-bottom: 20px; padding: 12px; background: #050505; border: 1px solid #222;
        }
        .highlight { color: #fff !important; background: #f05 !important; border-color: #fff; }

        .btn { 
            border: 2px solid #0ff; color: #0ff; background: transparent; 
            padding: 14px; cursor: pointer; width: 100%; font-weight: 900; 
            text-transform: uppercase; letter-spacing: 2px;
            transition: 0.3s;
        }
        .btn:hover { background: #0ff; color: #000; box-shadow: 0 0 30px rgba(0, 255, 255, 0.4); }

        #tx-box { 
            border: 1px solid #444; max-width: 600px; margin: 50px auto; 
            padding: 20px; font-size: 11px; color: #0f0; text-align: left; 
            background: rgba(0,0,0,0.95); position: relative; z-index: 2;
        }
    </style>
</head>
<body>
    <div class="head">
        <h1 style="text-shadow: 4px 4px 0px #f05; margin: 0; font-size: 3rem; font-weight: 900;">AIR_STRIKE_FUND</h1>
        <div class="manif">
            > [DATA]: INCOMING_REPORTS_VALIDATED<br>
            > [PRIORITY]: EMERGENCY_SUPPLIES_REQUIRED<br>
            > [LOG]: CONNECTION_ENCRYPTED_VIA_AES256
        </div>
        <div class="goal-bg"><div id="f" class="goal-up"></div></div>
        <div style="font-size:14px; color:#0ff; letter-spacing: 1px;">DEPLOYMENT_PROGRESS: <span id="p">18.4100</span>%</div>
    </div>

    <div class="wrap">
        {% for w in W %}
        <div class="card">
            <h2 style="margin:0; color:#0ff; font-size: 20px;">{{ w.n }}</h2>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}"></div>
            <div class="addr" id="cp-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn" onclick="copyIt('cp-{{ loop.index }}')">COPY_ADDR</button>
        </div>
        {% endfor %}
    </div>

    <div id="tx-box">
        <div style="border-bottom: 1px solid #0f0; padding-bottom: 5px; margin-bottom: 10px; font-weight: bold;">[ SAT_COMMS_FEED ]</div>
        <div id="l"></div>
    </div>

    <script>
        function startLiveSystem() {
            const baseValue = 18.4100;
            const growthDaily = 0.35;
            let startKey = 'iran_fund_v5';
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
            const amount = (Math.random() * 0.009 + 0.001).toFixed(4);
            e.style.padding = "2px 0";
            e.innerHTML=`<span style="color:#f05;">></span> [${new Date().toLocaleTimeString()}] VOLUNTEER_TRANSFER: <span style="color:#fff;">+${amount} BTC</span>... SUCCESS`;
            l.prepend(e); 
            if(l.childNodes.length > 6) l.removeChild(l.lastChild);
            setTimeout(addTx, Math.random() * 15000 + 10000);
        }
        setTimeout(addTx, 1500);

        function copyIt(id) {
            const el = document.getElementById(id);
            navigator.clipboard.writeText(el.innerText);
            el.classList.add('highlight');
            const original = el.innerText;
            el.innerText = "COPIED_TO_CLIPBOARD";
            setTimeout(() => { 
                el.classList.remove('highlight'); 
                el.innerText = original;
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
