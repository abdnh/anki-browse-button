import os
import sys
from typing import Any, Optional, Tuple

import aqt
from anki.cards import Card
from aqt import gui_hooks, mw
from aqt.browser.previewer import Previewer
from aqt.clayout import CardLayout
from aqt.qt import *
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

sys.path.append(os.path.join(os.path.dirname(__file__), "vendor"))

from .consts import consts

# Credit: https://www.svgrepo.com/svg/80989/book-with-magnifying-glass
SVG = """<svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
	 viewBox="0 0 26.064 26.064" xml:space="preserve">
<g>
	<path style="fill:#010002;" d="M19.27,23.146l-1.218-1.22c-0.555,0.253-1.146,0.419-1.75,0.49
		c-0.446,0.067-0.729,0.053-1.222,0.021l-0.059-0.004c-3.077-0.291-5.397-2.843-5.397-5.938c0.005-1.614,0.631-3.109,1.762-4.232
		c1.131-1.122,2.631-1.737,4.224-1.729c1.381,0.004,2.65,0.484,3.66,1.279V3.369c0-0.511-0.412-0.923-0.921-0.923L2.626,2.438
		c0-0.633,0.953-0.955,0.953-0.955h15.692c0.982,0,0.954,0.865,0.954,0.865v10.4c0.831,1.025,1.331,2.329,1.331,3.746
		c-0.002,0.865-0.184,1.699-0.531,2.464l0.654,0.656V0.866C21.678,0.175,20.812,0,20.812,0H3.406C0.809,0,0.809,2.405,0.809,2.405
		v22.156c0,0.509,0.412,0.923,0.923,0.923h16.617c0.51,0,0.921-0.414,0.921-0.923h1.414l-0.93-0.932L19.27,23.146z M5.347,5.875
		h9.53v1.803h-9.53V5.875z M25.004,24.611l-5.375-5.374c0.546-0.782,0.868-1.729,0.871-2.754c0.009-2.674-2.152-4.85-4.826-4.856
		c-2.673-0.012-4.85,2.15-4.859,4.824c-0.008,2.523,1.915,4.603,4.381,4.836h0.024c0.483,0.034,0.667,0.041,0.998-0.011
		c0.815-0.093,1.568-0.391,2.208-0.838l5.376,5.375c0.332,0.334,0.871,0.334,1.203,0.002C25.337,25.482,25.337,24.945,25.004,24.611
		z M15.646,20.099c-2.006-0.006-3.627-1.638-3.62-3.646c0.006-2.004,1.64-3.624,3.645-3.616c2.005,0.006,3.625,1.638,3.618,3.643
		C19.284,18.487,17.65,20.106,15.646,20.099z"/>
</g>
</svg>"""


def add_browse_button(text: str, card: Card, kind: str) -> str:
    html = ""
    if kind.endswith("Answer"):
        html = f"""<center><browse-button>{SVG}</browse-button></center>"""
    return text + html


def handle_js_msg(
    handled: Tuple[bool, Any], message: str, context: Any
) -> Tuple[bool, Any]:
    if message != "browse_button":
        return handled
    if mw.reviewer.card:
        aqt.dialogs.open("Browser", mw=mw, search=(f"cid:{mw.reviewer.card.id}",))
    return (True, None)


def add_js(web_content: WebContent, context: Optional[object]) -> None:
    if not isinstance(context, (Reviewer, Previewer, CardLayout)):
        return
    web_content.js.append(f"/_addons/{consts.module}/web/button.js")


gui_hooks.card_will_show.append(add_browse_button)
gui_hooks.webview_did_receive_js_message.append(handle_js_msg)
gui_hooks.webview_will_set_content.append(add_js)
mw.addonManager.setWebExports(__name__, r"web/.*")
