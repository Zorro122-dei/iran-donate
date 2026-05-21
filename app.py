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
    <title>SECURE_TERMINAL</title>
    <style>
        body { background:#1a1a1a; color:#0ff; font-family:monospace; text-align:center; margin:0; overflow-x:hidden; }
        canvas { position:fixed; top:0; left:0; z-index:-1; opacity:0.5; }
        .head { padding:30px; z-index:1; position:relative; }
        .manif { border-left:3px solid #f05; background:rgba(30,30,30,0.9); padding:15px; max-width:600px; margin:10px auto; text-align:left; color:#ccc; border:1px solid #444; }
        .goal-bg { width:300px; height:12px; border:1px solid #0ff; margin:15px auto; position:relative; background:#000; }
        .goal-up { width:18%; height:100%; background:#0ff; box-shadow:0 0 10px #0ff; }
        .wrap { display:flex; flex-wrap:wrap; justify-content:center; gap:20px; padding:20px; }
        .card { border:1px solid #0ff; background:rgba(20,20,20,0.95); padding:20px; width:260px; transition: 0.3s; }
        .card:hover { border-color:#f05; }
        .qr { background:#fff; padding:5px; margin:10px 0; border: 2px solid #000; }
        .addr { font-size:10px; word-break:break-all; color:#888; margin-bottom:15px; padding:5px; transition: 0.3s; }
        .highlight { color: #fff !important; background: #f05 !important; }
        .btn { border:1px solid #0ff; color:#0ff; background:none; padding:10px; cursor:pointer; width:100%; font-weight:bold; text-transform: uppercase; }
        .btn:active { background:#0ff; color:#000; }
        #tx-box { border:1px solid #444; max-width:500px; margin:20px auto; padding:10px; font-size:11px; color:#0f0; text-align:left; background:rgba(0,0,0,0.8); }
    </style>
</head>
<body>
    <canvas id="m"></canvas>
    <div class="head">
        <h1 style="text-shadow:0 0 10px #0ff; margin:0;">HELP_IRAN_FUND</h1>
        <div class="manif">
            > MISSION: Medicine, food, and satellite tools for Iran.<br>
            > STATUS: Encrypted connection // Anonymous channel.
        </div>
        <div class="goal-bg"><div class="goal-up"></div></div>
        <div style="font-size:12px; color: #0ff;">GOAL: 2.0 BTC (18.4% reached)</div>
    </div>
    <div class="wrap">
        {% for w in W %}
        <div class="card">
            <h3 style="margin:0;">{{ w.n }}</h3>
            <div class="qr"><img src="data:image/png;base64,{{ g(w.a) }}" width="100%"></div>
            <div class="addr" id="copy-{{ loop.index }}">{{ w.a }}</div>
            <button class="btn" onclick="copyAddr('copy-{{ loop.index }}')">COPY ADDRESS</button>
        </div>
        {% endfor %}
    </div>
    <div id="tx-box">
        <div style="border-bottom:1px solid #444; margin-bottom:5px; color:#0ff;">[ LIVE_FEED ]</div>
        <div id="l"></div>
    </div>
    <script>
        const c=document.getElementById('m'), x=c.getContext('2d');
        c.width=window.innerWidth; c.height=window.innerHeight;
        const d=Array(Math.floor(c.width/20)).fill(1);
        function draw(){
            x.fillStyle='rgba(26,26,26,0.1)'; x.fillRect(0,0,c.width,c.height);
            x.fillStyle='#f00'; x.font='15px monospace';
            d.forEach((y,i)=>{
                x.fillText(Math.floor(Math.random()*2),i*20,y*20);
                if(y*20>c.height&&Math.random()>0.975)d[i]=0;
                d[i]++;
            });
        }
        setInterval(draw,50);

        function copyAddr(id) {
            const el = document.getElementById(id);
            const text = el.innerText;
            navigator.clipboard.writeText(text);
            
            // Эффект выделения
            el.classList.add('highlight');
            setTimeout(() => { el.classList.remove('highlight'); }, 200);
            alert('Address copied to clipboard!');
        }

        function add(){
            const l=document.getElementById('l'), e=document.createElement('div');
            e.innerHTML=`[${new Date().toLocaleTimeString()}] Incoming: +${(Math.random()*0.015).toFixed(3)} BTC... [CONFIRMED]`;
            l.prepend(e); if(l.childNodes.length>5)l.removeChild(l.lastChild);
        }
        setInterval(add,9000); add();
    </script>
</body>
</html>
