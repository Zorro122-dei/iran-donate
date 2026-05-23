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
    <title>MILITARY_PAYMENT_TERMINAL</title>
    <style>
        body { 
            margin: 0; padding: 0; 
            background: radial-gradient(circle, #3a3a3a 0%, #1a1a1a 100%); 
            color: #eee; font-family: 'Segoe UI', monospace; 
            text-align: center; overflow: hidden; height: 100vh;
            display: flex; flex-direction: column; align-items: center;
        }

        /* ДЫРА В ЗЕМЛЕ (БОЛЕЕ РЕАЛИСТИЧНАЯ) */
        .ground-hole {
            position: fixed; bottom: -60px; width: 140%; height: 200px;
            background: radial-gradient(ellipse at center, #050505 0%, #1a1a1a 70%);
            border-radius: 50% 50% 0 0;
            z-index: 1; border-top: 3px solid #111;
            box-shadow: inset 0 30px 60px #000;
        }

        /* БОЛЕЕ ДЕТАЛЬНЫЕ РАКЕТЫ */
        .rocket-box {
            position: fixed; top: 100px; width: 60px; height: 300px; z-index: 1;
        }
        .rocket-body {
            width: 40px; height: 220px;
            background: linear-gradient(90deg, #333 0%, #666 50%, #222 100%);
            border-radius: 50% 50% 10px 10px;
            position: relative; border: 1px solid #111;
        }
        .rocket-nose {
            position: absolute; top: -40px; left: 0; width: 40px; height: 60px;
            background: linear-gradient(90deg, #800 0%, #f33 50%, #600 100%);
            border-radius: 50% 50% 20% 20%;
        }
        .wing {
            position: absolute; bottom: 10px; width: 25px; height: 40px;
            background: #222; border: 1px solid #000;
        }
        .w-left { left: -20px; clip-path: polygon(100% 0, 0 100%, 100% 100%); }
        .w-right { right: -20px; clip-path: polygon(0 0, 0 100%, 100% 100%); }
        
        .r-pos-l { left: 8%; transform: rotate(12deg); }
        .r-pos-r { right: 8%; transform: rotate(-12deg); }

        /* КОШЕЛЬКИ СО СВЕЧЕНИЕМ */
        .head { padding: 40px; position: relative; z-index: 5; }
        .wrap { display: flex; justify-content: center; gap: 40px; padding: 20px; position: relative; z-index: 5; }
        
        .card { 
            background: #111; border: 1px solid #444; 
            padding: 30px; width: 280px;
            transition: all 0.4s ease;
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        }
        /* ЭФФЕКТ СВЕЧЕНИЯ ПРИ НАВЕДЕНИИ */
        .card:hover { 
            border-color: #0ff;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.4), inset 0 0 10px rgba(0, 255, 255, 0.2);
            transform: translateY(-10px);
        }

        .qr { background: #fff; padding: 12px; margin-bottom: 20px; border-radius: 3px; }
        .qr img { width: 100%; display: block; }

        .addr { font-size: 10px; word-break: break-all; color: #666; background: #000; padding: 10px; margin-bottom: 20px; border-radius: 3px; }

        .btn { 
            border: 1px solid #0ff; color: #0ff; background: transparent; 
            padding: 12px; width: 100%; font-weight: bold; cursor: pointer;
            text-transform: uppercase; letter-spacing: 1px;
        }
        .btn:hover { background: #0ff; color: #000; }

        #tx-box { 
            border: 1px solid #333; width: 500px; margin-top: 30px;
            padding: 15px; font-size: 11px; color: #0f0; text-align: left; 
            background: rgba(0,0,0,0.8); position: relative; z-index: 5;
        }
    </style>
</head>
<body>
    <!-- РАКЕТА СЛЕВА -->
    <div class="rocket-box r-pos-l">
        <div class="rocket-nose"></div>
        <div class="rocket-body">
            <div class="wing w-left"></div>
            <div class="wing w-right"></div>
        </div>
    </div>

    <!-- РАКЕТА СПРАВА -->
    <div class="rocket-box r-pos-r">
        <div class="rocket-nose"></div>
        <div class="rocket-body">
            <div class="wing w-left"></div>
            <div class="wing w-right"></div>
        </div>
    </div>

    <div class="ground-hole"></div>

    <div class="head">
        <h1 style="margin:0; font-size: 2.5rem; letter-spacing: 5px; color: #f05; text-shadow: 2px 2px #000;">STRIKE_RELIEF_V2</h1>
        <div style="font-size:12px; color:#0ff; margin-top:15px; font-weight:bold;">
            GOAL: 2.0 BTC | <span id="p">18.4100</span>% REACHED
        </div>
    </div>

    <div class="wrap">
        {% for w in W %}
        <div class="card" onclick="copyIt('cp-{{ loop.index }}')">
            <h3 style="margin-top:0; color:#0ff;">{{ w.n }}</h3>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}"></div>
            <div class="addr" id="cp-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn">COPY ADDRESS</button>
        </div>
        {% endfor %}
    </div>

    <div id="tx-box">
        <div style="color: #444; border-bottom: 1px solid #222; padding-bottom: 5px; margin-bottom: 10px;">[ INCOMING_TRANSFERS_LOG ]</div>
        <div id="l"></div>
    </div>

    <script>
        function updateProgress() {
            const start = 18.4100;
            const growth = 0.35;
            let timeKey = 'strike_v2_start';
            let startTime = localStorage.getItem(timeKey) || Date.now();
            localStorage.setItem(timeKey, startTime);

            function run() {
                const diff = (Date.now() - parseInt(startTime)) / 86400000;
                let current = Math.min(99.85, start + (diff * growth));
                document.getElementById('p').innerText = current.toFixed(4);
            }
            setInterval(run, 1000); run();
        }
        updateProgress();

        function addTx(){
            const l=document.getElementById('l'), e=document.createElement('div');
            e.innerHTML=`> [${new Date().toLocaleTimeString()}] RECEIVED: +${(Math.random()*0.008).toFixed(4)} BTC`;
            l.prepend(e); 
            if(l.childNodes.length > 4) l.removeChild(l.lastChild);
            setTimeout(addTx, 12000);
        }
        addTx();

        function copyIt(id) {
            const el = document.getElementById(id);
            const text = (id.startsWith('cp')) ? el.innerText : document.getElementById(id).innerText;
            navigator.clipboard.writeText(text);
            alert("Адрес скопирован в буфер!");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, g=g_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
