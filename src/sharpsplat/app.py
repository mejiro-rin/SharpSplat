# SharpSplat app
from __future__ import annotations
import logging, shutil, subprocess, threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import gradio as gr

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
UPLOADS_DIR = BASE_DIR / "uploads"
VIEWER_DIR = BASE_DIR / "viewer"
for d in [OUTPUTS_DIR, UPLOADS_DIR]:
    d.mkdir(exist_ok=True)

VIEWER_PORT = 8860


class _H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


def start_viewer(port):
    global VIEWER_PORT
    VIEWER_PORT = port
    s = HTTPServer(("", port), _H)
    s.RequestHandlerClass.directory = str(BASE_DIR)
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    logger.info("viewer on port %d", port)


def run_sharp_predict(image_paths, progress=gr.Progress()):
    results = []
    for i, src in enumerate(progress.tqdm(image_paths)):
        sp = Path(src); stem = sp.stem
        dest = UPLOADS_DIR / sp.name
        shutil.copy2(sp, dest)
        try:
            subprocess.run(["sharp","predict","-i",str(dest),"-o",str(OUTPUTS_DIR),"--device","default","--no-render"], check=True, capture_output=True, text=True, timeout=600)
            ply = OUTPUTS_DIR / f"{stem}.ply"
            results.append({"name":stem,"image":str(dest),"ply":str(ply) if ply.exists() else None,"status":"done"})
        except subprocess.TimeoutExpired:
            results.append({"name":stem,"image":str(dest),"ply":None,"status":"timeout"})
        except subprocess.CalledProcessError:
            results.append({"name":stem,"image":str(dest),"ply":None,"status":"failed"})
        except FileNotFoundError:
            return results, [], "<div style=color:red>sharp not found</div>"
    choices = [r['name'] for r in results if r.get('ply') and Path(r['ply']).exists()]
    return results, choices, _build_html(results)


def _build_html(results):
    cards = ''
    for r in results:
        cls = 'done' if r['status']=='done' else 'fail'
        txt = 'done' if r['status']=='done' else r['status']
        cards += '<div class=card>'
        cards += '<img src=/file=' + r['image'] + ' class=thumb />'
        cards += '<div class=info><div class=name>' + r['name'] + '</div>'
        cards += '<div class="badge ' + cls + '">' + txt + '</div></div></div>'
    style = '.grid{display:flex;flex-direction:column;gap:8px}.card{display:flex;align-items:center;gap:12px;padding:10px;border:1px solid #ddd;border-radius:8px}.thumb{width:90px;height:60px;object-fit:cover;border-radius:4px}.info{flex:1}.name{font-weight:600}.badge{font-size:12px;padding:2px 8px;border-radius:4px;display:inline-block}.badge.done{background:#d4edda;color:#155724}.badge.fail{background:#f8d7da;color:#721c24}'
    return '<div class=grid>' + cards + '</div><style>' + style + '</style>'


def scan_existing_results():
    return sorted([p.stem for p in OUTPUTS_DIR.glob("*.ply")])


def open_viewer(ply_name):
    if not ply_name:
        return '<p style=color:#999>Select a result first</p>'
    url = "http://localhost:" + str(VIEWER_PORT) + "/viewer/?file=outputs/" + ply_name + ".ply"
    return "<iframe src=\"" + url + "\" style=width:100%;height:75vh;border:none;border-radius:8px></iframe>"


with gr.Blocks(title="SharpSplat") as _app:
    gr.HTML("<h2>SharpSplat</h2><p style=color:#666>SHARP 3D Gaussian Splatting</p>")
    with gr.Tabs():
        with gr.Tab("Process"):
            v = gr.File(label="Images",file_count="multiple",file_types=["image"])
            b = gr.Button("Start",variant="primary")
            h = gr.HTML("<p style=color:#999;padding:20px>Upload images and click Start</p>")
            s = gr.State([])
            dd_state = gr.State([])
            _app.load(fn=scan_existing_results, outputs=[dd_state])
            b.click(fn=run_sharp_predict,inputs=[v],outputs=[s,dd_state,h])
        with gr.Tab("3D Viewer"):
            dd = gr.Dropdown(label="Select result",choices=[],interactive=True)
            dd_state.change(fn=lambda x: gr.update(choices=x),inputs=[dd_state],outputs=[dd])
            view_btn = gr.Button("View in 3D",variant="primary")
            iframe = gr.HTML('<p style=color:#999;padding:20px>Select a result and click View in 3D</p>')
            dd.change(fn=open_viewer,inputs=[dd],outputs=[iframe])
            view_btn.click(fn=open_viewer,inputs=[dd],outputs=[iframe])


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--port',type=int,default=7860)
    p.add_argument('--share',action='store_true')
    a = p.parse_args()
    start_viewer(a.port + 1)
    _app.queue()
    print(f"SharpSplat -> http://localhost:{a.port}")
    _app.launch(server_port=a.port,share=a.share)
