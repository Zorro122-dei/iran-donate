from flask import Flask, render_template_string
import qrcode, io, base64

app = Flask(__name__)

# ТВОИ ДАННЫЕ (БЕЗ ИЗМЕНЕНИЙ)
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
    <title>SECURE_TERMINAL</title>
    <style>
        body { 
            background: #050505; 
            color: #eee; 
            font-family: 'Courier New', monospace; 
            margin: 0; 
            text-align: center;
            /* КРАСИВЫЙ ФОН С РАКЕТАМИ/ТЕХНИКОЙ */
            background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                              url('https://unsplash.com');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        
        /* Эффект шума на фоне */
        body::after {
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: url(https://vercel.app);
            opacity: 0.03; pointer-events: none; z-index: 0;
        }

        .head { padding: 40px 20px; position: relative; z-index: 1; }
        
        .manif { 
            border-left: 4px solid #f05; 
            background: rgba(20,20,20,0.8); 
            backdrop-filter: blur(10px);
            padding: 20px; 
            max-width: 600px; 
            margin: 20px auto; 
            text-align: left; 
            color: #0ff; 
            border: 1px solid #333;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }

        .goal-bg { 
            width: 300px; height: 14px; border: 1px solid #0ff; 
            margin: 15px auto; position: relative; background: #000; overflow: hidden; 
            border-radius: 2px;
        }
        .goal-up { height: 100%; background: linear-gradient(90deg, #0ff, #f05); box-shadow: 0 0 15px #0ff; width: 0%; transition: width 1.5s ease-out; }

        .wrap { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; padding: 20px; position: relative; z-index: 1; }
        
        .card { 
            background: rgba(15,15,15,0.85); 
            backdrop-filter: blur(15px);
            border: 1px solid #444; 
            padding: 25px; 
            width: 280px; 
            transition: 0.3s;
            border-top: 3px solid #f05;
        }
        .card:hover { border-color: #0ff; transform: translateY(-5px); }

        .qr { background: #fff; padding: 10px; margin: 15px 0; border-radius: 2px; }
        .qr img { width: 100%; display: block; filter: contrast(110%); }

        .addr { 
            font-size: 11px; word-break: break-all; color: #888; 
            margin-bottom: 20px; padding: 10px; background: #000; border: 1px dashed #333;
        }
        .highlight { color: #fff !important; background: #f05 !important; border-style: solid; }

        .btn { 
            border: none; color: #fff; background: #f05; 
            padding: 15px; cursor: pointer; width: 100%; font-weight: bold; 
            text-transform: uppercase; letter-spacing: 1px;
            clip-path: polygon(10% 0, 100% 0, 90% 100%, 0% 100%);
            transition: 0.2s;
        }
        .btn:hover { background: #0ff; color: #000; }

        #tx-box { 
            border: 1px solid #333; max-width: 600px; margin: 40px auto; 
            padding: 15px; font-size: 12px; color: #0f0; text-align: left; 
            background: rgba(0,0,0,0.9); position: relative; z-index: 1;
        }
    </style>
</head>
<body>
    <div class="head">
        <h1 style="text-shadow: 0 0 15px #f05; margin: 0; font-size: 2.5rem; letter-spacing: 4px;">WAR_FUND_TERMINAL</h1>
        <div class="manif">
            > [SYSTEM]: ENC_CONNECTION_STABLE<br>
            > [OBJECTIVE]: MEDICAL & TACTICAL SUPPORT<br>
            > [INTEL]: ANONYMOUS DONATIONS ONLY
        </div>
        <div class="goal-bg"><div id="f" class="goal-up"></div></div>
        <div style="font-size:13px; color:#0ff; font-weight: bold;">PROGRESS: <span id="p">18.4100</span>% REACHED</div>
    </div>

    <div class="wrap">
        {% for w in W %}
        <div class="card">
            <h3 style="margin:0; color:#0ff;">{{ w.n }}</h3>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}"></div>
            <div class="addr" id="cp-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn" onclick="copyIt('cp-{{ loop.index }}')">COPY ADDRESS</button>
        </div>
        {% endfor %}
    </div>

    <div id="tx-box">
        <div style="border-bottom:1px solid #333; margin-bottom:10px; color:#f05; font-weight: bold;">[ LIVE_FEED_ESTABLISHED ]</div>
        <div id="l"></div>
    </div>

    <script>
        // --- ГЛАВНЫЙ СЧЕТЧИК (ТВОЯ ЛОГИКА) ---
        function startLiveSystem() {
            const baseValue = 18.4100;
            const growthDaily = 0.35;
            let startKey = 'iran_fund_start_v3';
            let startTime = localStorage.getItem(startKey);
            if (!startTime) {
                startTime = Date.now();
                localStorage.setItem(startKey, startTime);
            } else { startTime = parseInt(startTime); }

            function update() {
                const now = Date.now();
                const diffDays = (now - startTime) / 86400000;
                let current = baseValue + (diffDays * growthDaily);
                if (current > 99.85) current = 99.85;
                document.getElementById('p').innerText = current.toFixed(4);
                document.getElementById('f').style.width = current + '%';
            }
            setInterval(update, 1000);
            update();
        }
        startLiveSystem();

        // --- ЛЕНТА (ТВОЯ ЛОГИКА) ---
        function addTx(){
            const l=document.getElementById('l'), e=document.createElement('div');
            const amount = (Math.random() * 0.014 + 0.001).toFixed(3);
            e.style.marginBottom = "5px";
            e.innerHTML=`<span style="color:#555;">[${new Date().toLocaleTimeString()}]</span> Incoming: <span style="color:#0f0;">+${amount} BTC</span>... CONFIRMED`;
            l.prepend(e); 
            if(l.childNodes.length > 5) l.removeChild(l.lastChild);
            setTimeout(addTx, Math.floor(Math.random() * 20000 + 25000));
        }
        setTimeout(addTx, 2000);

        function copyIt(id) {
            const el = document.getElementById(id);
            navigator.clipboard.writeText(el.innerText);
            el.classList.add('highlight');
            const oldText = el.innerText;
            el.innerText = "COPIED TO BUFFER";
            setTimeout(() => { 
                el.classList.remove('highlight'); 
                el.innerText = oldText;
            }, 1200);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, g=g_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
