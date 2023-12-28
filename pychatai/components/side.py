"""Sidebar component."""

import reflex as rx
from reflex.style import color_mode

from reflex_gptp import styles
from reflex_gptp.state import UUID, State


def convo_link(convo_key_name: tuple[UUID, str]) -> rx.Component:
    """A link to a conversation."""
    key = convo_key_name[0]
    name = convo_key_name[1]
    return rx.hstack(
        rx.text(
            name,
            on_click=lambda: State.handle_convo_link_click(key),  # type: ignore
            cursor="pointer",
            margin_top="0px",
        ),
        rx.spacer(),
        rx.icon(
            tag="delete",
            mr=4,
            on_click=lambda: State.delete_convo(key),  # type: ignore
            cursor="pointer",
        ),
        border_top="1px solid #eee",
    )


def sidebar() -> rx.Component:
    """The sidebar component."""
    return rx.vstack(
        rx.heading("Conversations", size="lg"),
        rx.vstack(rx.foreach(State.convo_keys_names, convo_link), flex="1", overflow_y="auto", align_items="stretch"),
        rx.hstack(
            rx.button("Set API key", on_click=State.toggle_api_key_modal, width="100%"),
            rx.button(rx.icon(tag="delete", on_click=State.delete_convos)),
        ),
        align_items="stretch",
        flex_direction="column",
        display="flex",
        flex="1",
        padding="2em 1em 0 1em",
        height="100%",
        spacing="0",
    )


def sidebar_wrapper(sb: rx.Component) -> rx.Component:
    """The sidebar wrapper component, used on large screens."""
    return rx.box(
        sb,
        width="80",
        bg=rx.cond(color_mode == "light", styles.bg_light_color, styles.bg_dark_color),
        shadow=styles.shadow_light,
        position="fixed",
        left=rx.cond(State.drawer_open, 0, "-80"),
        display="flex",
        height="100%",
        transition="all 0.2s ease-in-out",
    )
