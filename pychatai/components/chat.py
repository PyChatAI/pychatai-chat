"""Component that displays the chat messages and a welcome message with some settings."""

from functools import partial

import reflex as rx

from reflex_gptp import styles
from reflex_gptp.state import Message, MessagePart, MessagePartType, Prompt, State
from reflex_gptp.utils import providers_models

custom_markdown = partial(
    rx.markdown,
    component_map={
        "p": lambda value: rx.Text.create(value),
    },
)


def extra_output_icon(mp: MessagePart) -> rx.Component:
    """An icon that opens a modal with extra output."""
    return rx.icon(
        tag="info_outline",
        color="blue",
        cursor="pointer",
        on_click=lambda: State.toggle_chat_modal(mp.id),  # type: ignore
    )


def extra_output_modal(mp: MessagePart) -> rx.Component:
    """A modal with extra output."""

    def toggle_fn():
        return State.toggle_chat_modal(mp.id)  # type: ignore

    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.hstack(
                        rx.text("Extra output"),
                        rx.spacer(),
                        rx.icon(tag="close", cursor="pointer", on_click=toggle_fn),
                    )
                ),
                rx.modal_body(
                    rx.cond(
                        mp.type == MessagePartType.AGENT_FINISH,
                        custom_markdown(mp.extra_output),
                        rx.cond(
                            mp.type == MessagePartType.TOOL_END,
                            custom_markdown(
                                f"Action input:\n```python\n{mp.extra_output}\n```\nAction output:\n```python\n{mp.extra_output1}\n```"
                            ),
                            custom_markdown(f"```python\n{mp.extra_output}\n```"),
                        ),
                    )
                ),
                rx.modal_footer(rx.button("Close", on_click=toggle_fn)),
            )
        ),
        on_overlay_click=toggle_fn,
        on_esc=toggle_fn,
        is_open=State.chat_modals_visible[mp.id],
    )


def chat_bubble_part(mp: MessagePart) -> rx.Component:
    """Component for a part of a message."""
    return rx.box(
        rx.cond(
            mp.type == MessagePartType.TOOL_START,
            rx.hstack(
                rx.text(f"Using tool {mp.text}"),
                rx.spinner(color="orange", size="sm"),
                extra_output_icon(mp),
            ),
            rx.cond(
                mp.type == MessagePartType.TOOL_END,
                rx.hstack(
                    rx.text(f"Tool {mp.text} finished."),
                    rx.icon(tag="check", color="green"),
                    extra_output_icon(mp),
                ),
                rx.cond(
                    mp.type == MessagePartType.AGENT_FINISH,
                    rx.hstack(
                        rx.box(custom_markdown(mp.text)),
                        rx.cond(mp.extra_output | mp.extra_output1, extra_output_icon(mp)),  # type: ignore
                    ),
                    rx.cond(
                        mp.type == MessagePartType.ERROR,
                        rx.hstack(
                            rx.icon(tag="warning_two"),
                            rx.text(f"Error: {mp.text}"),
                            color="red",
                        ),
                        rx.cond(
                            mp.type == MessagePartType.INTERRUPT, rx.text(f"🟧 {mp.text}"), custom_markdown(mp.text)
                        ),
                    ),
                ),
            ),
        ),
        extra_output_modal(mp),
    )


def chat_bubble(message: Message) -> rx.Component:
    """A chat bubble component."""
    return rx.box(
        rx.cond(
            message.is_loading,
            rx.skeleton_text(no_of_lines=2),
            rx.box(
                rx.cond(
                    message.own,
                    rx.hstack(
                        rx.text(message.parts[-1].text, text_align="right"),
                        rx.popover(
                            rx.popover_trigger(
                                rx.icon(
                                    tag="plus_square",
                                    cursor="pointer",
                                    align_self="flex-start",
                                    on_click=lambda: State.set_chat_popover_visible(message.id),  # type: ignore
                                ),
                            ),
                            rx.popover_content(
                                rx.popover_header("Tools"),
                                rx.popover_body(
                                    rx.vstack(
                                        rx.text(
                                            "Copy",
                                            cursor="pointer",
                                            on_click=lambda: State.copy_message(message),  # type: ignore
                                            _hover={"bg": styles.accent_light},
                                            width="100%",
                                            text_align="center",
                                        ),
                                        rx.text(
                                            "Regenerate",
                                            cursor="pointer",
                                            on_click=lambda: State.regenerate_response(message),  # type: ignore
                                            _hover={"bg": styles.accent_light},
                                            width="100%",
                                            text_align="center",
                                        ),
                                    )
                                ),
                                rx.popover_close_button(
                                    on_click=lambda: State.set_chat_popover_visible(message.id, False)  # type: ignore
                                ),
                            ),
                            is_lazy=True,
                            is_open=State.chat_popovers_visible[message.id],
                        ),  # type: ignore
                    ),
                    rx.hstack(
                        rx.box(
                            rx.foreach(message.parts, lambda mp: chat_bubble_part(mp)),  # type: ignore
                            overflow="auto",
                        ),
                        rx.popover(
                            rx.popover_trigger(
                                rx.icon(
                                    tag="plus_square",
                                    cursor="pointer",
                                    align_self="flex-start",
                                    on_click=lambda: State.set_chat_popover_visible(message.id, True),  # type: ignore
                                ),
                            ),
                            rx.popover_content(
                                rx.popover_header("Tools"),
                                rx.popover_body(
                                    rx.text(
                                        "Copy",
                                        cursor="pointer",
                                        on_click=lambda: State.copy_message(message),  # type: ignore
                                        _hover={"bg": styles.accent_light},
                                        width="100%",
                                        text_align="center",
                                    ),
                                ),
                                rx.popover_close_button(
                                    on_click=lambda: State.set_chat_popover_visible(message.id, False)  # type: ignore
                                ),
                            ),
                            is_lazy=True,
                            is_open=State.chat_popovers_visible[message.id],
                        ),  # type: ignore
                    ),
                ),
                bg=rx.cond(message.own, styles.accent_color, styles.border_color),
                shadow=styles.shadow_light,
                **styles.message_style,
            ),
        ),
        display="flex",
        justify_content=rx.cond(message.own, "flex-end", "flex-start"),
        margin_bottom="1",
    )


class AlwaysScrollToBottom(rx.Component):
    """A component that makes the list of messages always scroll to the bottom when it's already at the bottom."""

    library = "../public/scroll.js"
    tag = "AlwaysScrollToBottom"

    name: rx.Var[str]


always_scroll_to_bottom = AlwaysScrollToBottom.create


def model_modal() -> rx.Component:
    """A modal that allows the user to change the model."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.hstack(
                        rx.text("Model"), rx.icon(tag="close", cursor="pointer", on_click=State.toggle_model_modal)
                    )
                ),
                rx.modal_body(
                    rx.form(
                        rx.vstack(
                            rx.hstack(
                                rx.select(
                                    list(providers_models.keys()),
                                    id="provider",
                                    placeholder="Select a provider.",
                                    value=State.form_provider,
                                    is_required=True,
                                    on_change=State.handle_provider_change,
                                    color_schemes="twitter",
                                ),
                                rx.select(
                                    State.form_provider_models,
                                    id="name",
                                    placeholder="Select a model.",
                                    is_required=True,
                                    value=State.form_model,
                                    on_change=State.handle_model_change,
                                    color_schemes="twitter",
                                ),
                            ),
                            rx.button("Set", type_="submit"),
                        ),
                        on_submit=State.handle_model_submit,
                    )
                ),
            )
        ),
        is_open=State.show_model_modal,
        on_overlay_click=State.toggle_model_modal,
        on_esc=State.toggle_model_modal,
    )


def plugins_modal() -> rx.Component:
    """A modal that allows the user to enable/disable plugins."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.hstack(
                        rx.text("Plugins"), rx.icon(tag="close", cursor="pointer", on_click=State.toggle_plugins_modal)
                    )
                ),
                rx.modal_body(
                    rx.vstack(
                        rx.checkbox_group(
                            rx.foreach(
                                State.current_convo_plugins,
                                lambda x: rx.checkbox(
                                    x[0],
                                    is_checked=x[1],
                                    on_change=lambda val: State.toggle_plugin(x[0], val),  # type: ignore
                                ),
                            ),
                        ),
                        align_items="flex-start",
                    )
                ),
            )
        ),
        is_open=State.show_plugins_modal,
        on_overlay_click=State.toggle_plugins_modal,
        on_esc=State.toggle_plugins_modal,
    )


def prompt_accordion_item(p: Prompt) -> rx.Component:
    """An accordion item for a prompt."""
    return rx.accordion_item(
        rx.accordion_button(
            rx.heading(p.title, text_align="left", max_width="70%"),
            rx.accordion_icon(),
            rx.spacer(),
            rx.button("choose", on_click=lambda: State.set_prompt(p)),  # type: ignore
        ),
        rx.accordion_panel(rx.text(p.text)),
    )


def prompts_modal() -> rx.Component:
    """A modal that allows the user to choose a prompt."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.hstack(
                        rx.text("Prompts"), rx.icon(tag="close", cursor="pointer", on_click=State.toggle_prompts_modal)
                    )
                ),
                rx.modal_body(
                    rx.accordion(
                        rx.foreach(State.prompts, prompt_accordion_item),  # type: ignore
                        allow_multiple=True,
                        allow_toggle=True,
                        width="100%",
                    ),  # type: ignore
                    rx.link("Source", href="https://github.com/f/awesome-chatgpt-prompts", is_external=True),
                ),
            )
        ),
        is_open=State.show_prompts_modal,
        on_overlay_click=State.toggle_prompts_modal,
        on_esc=State.toggle_prompts_modal,
    )


def api_key_modal() -> rx.Component:
    """A modal that allows the user to set their API keys."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.hstack(
                        rx.text("Set your API keys"),
                        rx.icon(tag="close", cursor="pointer", on_click=State.toggle_api_key_modal),
                    )
                ),
                rx.modal_body(
                    rx.vstack(
                        rx.heading("OpenAI"),
                        rx.form(
                            rx.vstack(
                                rx.input(
                                    placeholder="API Key",
                                    id="api_key",
                                ),
                                rx.button("Set", type_="submit"),
                            ),
                            on_submit=lambda fd: State.handle_api_key_submit(fd, "openai"),  # type: ignore
                        ),
                        rx.heading("Anthropic"),
                        rx.form(
                            rx.vstack(
                                rx.input(
                                    placeholder="API Key",
                                    id="api_key",
                                ),
                                rx.button("Set", type_="submit"),
                            ),
                            on_submit=lambda fd: State.handle_api_key_submit(fd, "anthropic"),  # type: ignore
                        ),
                        align_items="normal",
                    )
                ),
                rx.modal_footer(rx.button("Close", on_click=State.toggle_api_key_modal)),
            )
        ),
        is_open=State.show_api_key_modal,
        on_overlay_click=State.toggle_api_key_modal,
        on_esc=State.toggle_api_key_modal,
    )


def chat_messages() -> rx.Component:
    """The chat messages component.

    If there are chat messages in the current conversation, it displays them.
    Otherwise, it displays a welcome message with settings for the user to change.
    These include the provider, model, and plugins.
    """
    return rx.box(
        rx.cond(
            State.convo_has_messages,
            rx.box(
                rx.foreach(State.current_convo_messages, chat_bubble),
                always_scroll_to_bottom(),
                display="flex",
                flex="1",
                flex_direction="column",
            ),
            rx.box(
                rx.button(
                    rx.vstack(
                        rx.text(State.current_provider),
                        rx.image(src=f"{State.current_provider}.ico", height="32px", background="white"),
                        align_items="center",
                    ),
                    height="fit-content",
                    padding="7px",
                    shadow="lg",
                    on_click=State.toggle_model_modal,
                ),
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.text("Plugins"),
                            rx.cond(State.n_enabled_plugins > 0, rx.badge(State.n_enabled_plugins)),
                        ),
                        height="fit-content",
                        padding="7px",
                        shadow="lg",
                        on_click=State.toggle_plugins_modal,
                    ),
                    rx.button(
                        "Prompts", height="fit-content", padding="7px", shadow="lg", on_click=State.toggle_prompts_modal
                    ),
                ),
                rx.text(
                    "Welcome! Start a conversation by typing a message.",
                    text_align=["center", "center", "left"],
                    width="auto",
                ),
                rx.cond(~State.have_api_key, rx.text("You haven't set an API key yet.")),
                model_modal(),
                plugins_modal(),
                prompts_modal(),
                gap="2",
                width="100%",
                display="flex",
                align_items="center",
                flex_direction="column",
                justify_content="center",
            ),
        ),
        api_key_modal(),
        py="8",
        display="flex",
        flex="1",
        width="100%",
        padding_x="4",
        padding_y="0",
        align_self="center",
        overflow="hidden",
    )
