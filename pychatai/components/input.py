"""Input bar component."""

import reflex as rx
from reflex.components.forms.textarea import TextArea

from reflex_gptp import styles
from reflex_gptp.state import State


class GrowingTextArea(TextArea):
    """A textarea that grows as you type."""

    library = "../public/growing.js"
    tag = "GrowingTextarea"

    max_rows: rx.Var[int]
    line_height: rx.Var[int]
    should_focus: rx.Var[bool]


growing_text_area = GrowingTextArea.create


def input_bar() -> rx.Component:
    """The input bar component."""
    return rx.box(
        rx.cond(
            State.processing,
            rx.button(
                "Interrupt",
                bg="#fef2f2",
                color="#b91c1c",
                _hover={"bg": "#fca5a5"},
                border_radius="lg",
                on_click=State.interrupt_chat,
            ),
        ),
        rx.box(
            rx.form(
                rx.hstack(
                    growing_text_area(
                        placeholder="Type your message here",
                        id="input",
                        should_focus=State.input_should_focus,
                        on_blur=State.remove_focus,
                        p="2",
                        value=State.question,
                        on_change=State.set_question,
                        border="none",
                        focus_border_color="transparent",
                        _hover={"border_color": styles.accent_color},
                        is_disabled=State.processing,
                    ),
                    rx.button(
                        rx.cond(State.processing, rx.spinner(color="gray", size="sm"), rx.icon(tag="arrow_forward")),
                        type_="submit",
                        bg="transparent",
                        _hover={"bg": styles.accent_color},
                        is_disabled=State.processing | State.empty_question,
                    ),
                    align_items="flex-end",
                ),
                on_submit=State.handle_question_submit,
                width="100%",
            ),
            backdrop_filter="auto",
            backdrop_blur="lg",
            rounded="lg",
            shadow="lg",
            bg="blackAlpha.300",
        ),
        padding_x="2em",
        position="sticky",
        bottom="2",
        margin_top="2",
        left="0",
        width="100%",
    )
