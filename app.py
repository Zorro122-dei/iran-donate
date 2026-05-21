
from flask import Flask, render_template_string
import qrcode, io, base64
app = Flask(__name__)
W = [{"n": "BITCOIN", "a": "bc1qrpg5nwr5t8jl3nnavgf2k2v4c43u75c9usxpyk"},
     {"n": "USDT (ERC20)", "a": "0x40745600a508d653549c664d050b90826e4b61ba"}]
def get_qr(t):
    qr = qrcode.make(t)
    b = io.BytesIO()
    qr.save(b, "PNG")
    return base64.b64encode(b.getvalue()).decode()
H = """
<body style="background:#050505;color:#0ff;font-family:monospace;text-align:center;padding:50px">
<h1 style="text-shadow:0 0 10px #0ff">HELP_IRAN_FUND</h1>
<p style="color:#f05">// SECURE ANONYMOUS SYSTEM //</p>
{% for w in W %}
<div style="border:1px solid #0ff;margin:20px auto;padding:20px;max-width:400px;box-shadow:0 0 15px #0ff">
<h3>{{w.n}}</h3>
<img src="data:image/png;base64,{{q(w.a)}}" width="220" style="border:10px solid #fff">
<p style="word-break:break-all;font-size:12px;margin:15px 0">{{w.a}}</p>
<button onclick="navigator.clipboard.writeText('{{w.a}}');alert('Скопировано!')" style="background:none;border:1px solid #f05;color:#f05;padding:10px;cursor:pointer;width:100%">КОПИРОВАТЬ АДРЕС</button>
</div>
{% endfor %}
<p style="color:#333;margin-top:50px">NO_LOGS. NO_TRACE. 2024.</p>
</body>
"""
@app.route('/')
def i(): return render_template_string(H, W=W, q=get_qr)
if __name__ == "__main__": app.run(host='0.0.0.0', port=5000)
