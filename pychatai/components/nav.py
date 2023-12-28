"""This module defines the navbar component."""

import reflex as rx

from reflex_gptp import styles
from reflex_gptp.state import State


def navbar(sidebar: rx.Component) -> rx.Component:
    """The navbar component."""
    return rx.vstack(
        rx.box(
            rx.hstack(
                rx.icon(
                    tag="hamburger",
                    mr=4,
                    on_click=State.toggle_drawer,
                    cursor="pointer",
                ),
                rx.tablet_and_desktop(
                    rx.hstack(rx.image(src="favicon.ico", width="2em", height="2em"), rx.heading("PyChatAI"))
                ),
                rx.spacer(),
                rx.hstack(
                    rx.cond(
                        State.convo_has_messages,
                        rx.tooltip(
                            rx.image(src=f"{State.current_provider}.ico", height="16px", background="white"),
                            label=f"Provider: {State.current_provider}; Model: {State.current_model}",
                        ),
                    ),
                    rx.tooltip(
                        rx.editable(
                            rx.editable_preview(),
                            rx.editable_input(text_align="center"),
                            placeholder=State.current_convo_name,
                            on_submit=State.change_convo_name,
                        ),
                        label="Click to change conversation name",
                    ),
                ),
                rx.spacer(),
                rx.button(rx.icon(tag="add"), on_click=State.handle_new_convo_click),
                rx.color_mode_button(rx.color_mode_icon(), float="right"),
            ),
        ),
        rx.drawer(
            rx.mobile_only(
                rx.drawer_overlay(
                    rx.drawer_content(
                        rx.icon(
                            tag="close",
                            position="absolute",
                            margin_left="1em",
                            margin_top="1em",
                            z_index="999",
                            on_click=State.toggle_drawer,
                            _hover={
                                "cursor": "pointer",
                                "color": styles.accent_color,
                            },
                        ),
                        sidebar,
                        width="100%",
                        # bg="rgba(255,255,255, 0.97)",
                    ),
                    bg="rgba(255,255,255, 0.5)",
                )
            ),
            placement="left",
            block_scroll_on_mount=False,
            is_open=State.drawer_open,
            on_close=State.toggle_drawer,
            bg="rgba(255,255,255, 0.5)",
        ),  # type: ignore
        position="sticky",
        align_items="stretch",
        top="0",
        left="0",
        p="4",
        margin_bottom="1",
        width="100%",
        bg="blackAlpha.300",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_bottom=f"1px solid {styles.border_color}",
    )
