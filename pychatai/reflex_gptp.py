"""The main app file for the app."""

import reflex as rx

from reflex_gptp import styles
from reflex_gptp.components.chat import chat_messages
from reflex_gptp.components.input import input_bar
from reflex_gptp.components.nav import navbar
from reflex_gptp.components.side import sidebar, sidebar_wrapper
from reflex_gptp.state import State
from rxconfig import config

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


def index() -> rx.Component:
    """The main page for the app."""
    sb = sidebar()
    return rx.fragment(
        rx.hstack(
            rx.tablet_and_desktop(sidebar_wrapper(sb)),
            rx.box(
                navbar(sb),
                chat_messages(),
                input_bar(),
                transition="all 0.2s ease-in-out",
                display="flex",
                flex="1",
                width="100%",
                flex_direction="column",
                align_items="stretch",
            ),
            pl=rx.cond(State.drawer_open, [0, 80, 80, 80, 80], "0"),
            transition="all 0.2s ease-in-out",
            min_h="100svh",
            align_items="stretch",
            spacing="0",
        ),
    )


# Add state and page to the app.
app = rx.App(
    style=styles.base_style,
    load_events={"index": [State.load_data]},
    stylesheets=[
        "styles.css",  # This path is relative to assets/
    ],
)
app.add_page(index, title="PyChatAI")
app.compile()
