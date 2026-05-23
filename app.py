from flask import Flask, render_template_string
import qrcode, io, base64

app = Flask(__name__)

# ТВОИ ДАННЫЕ
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
    <title>TERMINAL_STRIKE</title>
    <style>
        body { 
            margin: 0; 
            padding: 0;
            color: #eee; 
            font-family: 'Courier New', monospace; 
            text-align: center;
            min-height: 100vh;
            /* КАРТИНКА С РАКЕТОЙ НА ФОНЕ */
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), 
                        url('https://unsplash.com');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            overflow-x: hidden;
        }
        
        /* Эффект мерцания экрана */
        .overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            background-size: 100% 2px, 3px 100%;
            pointer-events: none; z-index: 10;
        }

        .head { padding: 40px 20px; position: relative; z-index: 1; }
        
        .manif { 
            border: 1px solid #f05; 
            background: rgba(0,0,0,0.8); 
            backdrop-filter: blur(10px);
            padding: 20px; 
            max-width: 650px; 
            margin: 20px auto; 
            text-align: left; 
            color: #fff;
            box-shadow: 0 0 30px rgba(255, 0, 85, 0.3);
        }

        .goal-bg { 
            width: 300px; height: 14px; border: 1px solid #0ff; 
            margin: 15px auto; position: relative; background: #000; overflow: hidden; 
        }
        .goal-up { height: 100%; background: #0ff; box-shadow: 0 0 15px #0ff; width: 0%; transition: width 1.5s ease-in-out; }

        .wrap { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; padding: 20px; position: relative; z-index: 1; }
        
        .card { 
            background: rgba(10,10,10,0.9); 
            border: 1px solid #444; 
            padding: 25px; 
            width: 280px; 
            border-top: 4px solid #f05;
            transition: 0.3s;
        }
        .card:hover { border-color: #0ff; box-shadow: 0 0 20px rgba(0,255,255,0.2); }

        .qr { background: #fff; padding: 10px; margin: 15px 0; }
        .qr img { width: 100%; display: block; }

        .addr { 
            font-size: 11px; word-break: break-all; color: #888; 
            margin-bottom: 20px; padding: 10px; background: #000; border: 1px dashed #333;
        }
        .highlight { color: #fff !important; background: #f05 !important; }

        .btn { 
            border: 1px solid #f05; color: #f05; background: none; 
            padding: 12px; cursor: pointer; width: 100%; font-weight: bold; 
            text-transform: uppercase; transition: 0.2s;
        }
        .btn:hover { background: #f05; color: #fff; box-shadow: 0 0 15px #f05; }

        #tx-box { 
            border: 1px solid #333; max-width: 600px; margin: 40px auto; 
            padding: 15px; font-size: 11px; color: #0f0; text-align: left; 
            background: rgba(0,0,0,0.9); position: relative; z-index: 1;
        }
    </style>
</head>
<body>
    <div class="overlay"></div>
    <div class="head">
        <h1 style="text-shadow: 0 0 20px #f05; margin: 0; font-size: 2.8rem;">OPERATION: RED_LINE</h1>
        <div class="manif">
            > [STATUS]: ACTIVE_INTERCEPTION<br>
            > [PAYLOAD]: MEDICINE & COMMS_GEAR<br>
            > [SECURITY]: MULTI-LAYER_ENCRYPTION
        </div>
        <div class="goal-bg"><div id="f" class="goal-up"></div></div>
        <div style="font-size:13px; color:#0ff;">TOTAL_COLLECTED: <span id="p">18.4100</span>%</div>
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
        <div style="border-bottom:1px solid #333; margin-bottom:10px; color:#f05;">[ NODE_TRAFFIC ]</div>
        <div id="l"></div>
    </div>

    <script>
        function startLiveSystem() {
            const baseValue = 18.4100;
            const growthDaily = 0.35;
            let startKey = 'iran_fund_start_v3';
            let startTime = localStorage.getItem(startKey) || Date.now();
            localStorage.setItem(startKey, startTime);

            function update() {
                const now = Date.now();
                const diffDays = (now - parseInt(startTime)) / 86400000;
                let current = baseValue + (diffDays * growthDaily);
                if (current > 99.85) current = 99.85;
                document.getElementById('p').innerText = current.toFixed(4);
                document.getElementById('f').style.width = current + '%';
            }
            setInterval(update, 1000);
            update();
        }
        startLiveSystem();

        function addTx(){
            const l=document.getElementById('l'), e=document.createElement('div');
            const amount = (Math.random() * 0.01 + 0.001).toFixed(4);
            e.innerHTML=`[${new Date().toLocaleTimeString()}] RECEIVED: +${amount} UNITS... OK`;
            l.prepend(e); 
            if(l.childNodes.length > 5) l.removeChild(l.lastChild);
            setTimeout(addTx, Math.random() * 20000 + 15000);
        }
        setTimeout(addTx, 2000);

        function copyIt(id) {
            const el = document.getElementById(id);
            navigator.clipboard.writeText(el.innerText);
            el.classList.add('highlight');
            setTimeout(() => { el.classList.remove('highlight'); }, 200);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, g=g_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
