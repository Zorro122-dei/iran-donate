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
    <title>SECURE_FUND</title>
    <style>
        body { background:#000; color:#0ff; font-family:monospace; text-align:center; margin:0; overflow-x:hidden; }
        canvas { position:fixed; top:0; left:0; z-index:-1; opacity:0.4; }
        .head { padding:30px; z-index:1; position:relative; }
        .manif { border-left:3px solid #f05; background:rgba(20,20,20,0.9); padding:15px; max-width:600px; margin:10px auto; text-align:left; color:#ccc; border:1px solid #333; }
        .goal-bg { width:300px; height:12px; border:1px solid #0ff; margin:15px auto; position:relative; }
        .goal-up { width:18%; height:100%; background:#0ff; box-shadow:0 0 10px #0ff; }
        .wrap { display:flex; flex-wrap:wrap; justify-content:center; gap:20px; padding:20px; }
        .card { border:1px solid #0ff; background:rgba(0,0,0,0.8); padding:20px; width:260px; }
        .qr { background:#fff; padding:5px; margin:10px 0; }
        .addr { font-size:10px; word-break:break-all; color:#666; margin-bottom:15px; }
        .btn { border:1px solid #0ff; color:#0ff; background:none; padding:10px; cursor:pointer; width:100%; font-weight:bold; }
        #tx-box { border:1px solid #333; max-width:500px; margin:20px auto; padding:10px; font-size:11px; color:#0f0; text-align:left; background:rgba(0,0,0,0.8); }
    </style>
</head>
<body>
    <canvas id="m"></canvas>
    <div class="head">
        <h1 style="text-shadow:0 0 10px #0ff; margin:0;">HELP_IRAN_FUND</h1>
        <div class="manif">
            > MISSION: Medicine, food, and communication for Iran.<br>
            > SECURITY: No logs. No tracking. Total anonymity.
        </div>
        <div class="goal-bg"><div class="goal-up"></div></div>
        <div style="font-size:12px;">GOAL: 2.0 BTC (18.4% reached)</div>
    </div>
    <div class="wrap">
        {% for w in W %}
        <div class="card">
            <h3>{{ w.n }}</h3>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}" width="100%"></div>
            <div class="addr">{{ w.a }}</div>
            <button class="btn" onclick="navigator.clipboard.writeText('{{ w.a }}');alert('Copied!')">COPY ADDRESS</button>
        </div>
        {% endfor %}
    </div>
    <div id="tx-box">
        <div style="border-bottom:1px solid #333; margin-bottom:5px; color:#0ff;">[ LIVE_DATA ]</div>
        <div id="l"></div>
    </div>
    <script>
        const c=document.getElementById('m'), x=c.getContext('2d');
        c.width=window.innerWidth; c.height=window.innerHeight;
        const d=Array(Math.floor(c.width/20)).fill(1);
        function draw(){
            x.fillStyle='rgba(0,0,0,0.1)'; x.fillRect(0,0,c.width,c.height);
            x.fillStyle='#f00'; x.font='15px monospace';
            d.forEach((y,i)=>{
                x.fillText(Math.floor(Math.random()*2),i*20,y*20);
                if(y*20>c.height&&Math.random()>0.975)d[i]=0;
                d[i]++;
            });
        }
        setInterval(draw,50);
        function add(){
            const l=document.getElementById('l'), e=document.createElement('div');
            e.innerHTML=`[${new Date().toLocaleTimeString()}] Confirmed: +${(Math.random()*0.02).toFixed(3)} BTC...`;
            l.prepend(e); if(l.childNodes.length>5)l.removeChild(l.lastChild);
        }
        setInterval(add,7000); add();
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(H, W=W, g=g_qr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
