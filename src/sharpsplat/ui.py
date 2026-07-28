from __future__ import annotations

from html import escape

import gradio as gr

from .predictor import SharpPredictor
from .repository import PredictionResult, ResultRepository
from .viewer import ViewerServer


class SharpSplatUI:
    def __init__(self, predictor: SharpPredictor, repository: ResultRepository, viewer: ViewerServer) -> None:
        self.predictor = predictor
        self.repository = repository
        self.viewer = viewer

    def scan_existing_results(self) -> list[str]:
        choices = self.repository.existing_result_names()
        return gr.update(choices=choices, value=choices[0] if choices else None)

    def run_predictions(self, image_paths, progress=gr.Progress()):
        try:
            results = self.predictor.predict_many(image_paths, progress=progress)
        except FileNotFoundError:
            return [], gr.update(choices=[], value=None), "<div style=color:red>sharp not found</div>"

        choices = [result.name for result in results if result.has_ply]
        return [result.to_dict() for result in results], gr.update(choices=choices, value=choices[0] if choices else None), self.render_results(results)

    def render_results(self, results: list[PredictionResult]) -> str:
        cards = []
        for result in results:
            badge_class = "done" if result.status == "done" else "fail"
            badge_text = "done" if result.status == "done" else result.status
            cards.append(
                "<div class=card>"
                f'<img src="/file={escape(str(result.image_path))}" class="thumb" />'
                '<div class="info">'
                f'<div class="name">{escape(result.name)}</div>'
                f'<div class="badge {badge_class}">{escape(badge_text)}</div>'
                "</div></div>"
            )

        style = (
            ".grid{display:flex;flex-direction:column;gap:8px}"
            ".card{display:flex;align-items:center;gap:12px;padding:10px;border:1px solid #ddd;border-radius:8px}"
            ".thumb{width:90px;height:60px;object-fit:cover;border-radius:4px}"
            ".info{flex:1}.name{font-weight:600}"
            ".badge{font-size:12px;padding:2px 8px;border-radius:4px;display:inline-block}"
            ".badge.done{background:#d4edda;color:#155724}.badge.fail{background:#f8d7da;color:#721c24}"
        )
        return "<div class=grid>" + "".join(cards) + "</div><style>" + style + "</style>"

    def open_viewer(self, ply_name: str | None) -> str:
        if not ply_name:
            return '<p style=color:#999>Select a result first</p>'
        url = self.viewer.viewer_url(ply_name)
        return f'<iframe src="{url}" style="width:100%;height:75vh;border:none;border-radius:8px"></iframe>'

    def build(self) -> gr.Blocks:
        with gr.Blocks(title="SharpSplat") as app:
            gr.HTML("<h2>SharpSplat</h2><p style=color:#666>SHARP 3D Gaussian Splatting</p>")
            result_dropdown = gr.Dropdown(label="Select result", choices=[], interactive=True)
            with gr.Tabs():
                with gr.Tab("3D Viewer"):
                    view = gr.Button("View in 3D", variant="primary")
                    iframe = gr.HTML('<p style=color:#999;padding:20px>Select a result and click View in 3D</p>')
                    result_dropdown.change(fn=self.open_viewer, inputs=[result_dropdown], outputs=[iframe])
                    view.click(fn=self.open_viewer, inputs=[result_dropdown], outputs=[iframe])
                with gr.Tab("Process"):
                    files = gr.File(label="Images", file_count="multiple", file_types=["image"])
                    start = gr.Button("Start", variant="primary")
                    html = gr.HTML("<p style=color:#999;padding:20px>Upload images and click Start</p>")
                    results_state = gr.State([])
                    app.load(fn=self.scan_existing_results, outputs=[result_dropdown])
                    start.click(
                        fn=self.run_predictions,
                        inputs=[files],
                        outputs=[results_state, result_dropdown, html],
                    )
        return app
