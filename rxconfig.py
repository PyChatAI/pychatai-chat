"""The app config."""

import reflex as rx


class ReflexgptpConfig(rx.Config):
    """The app config class."""


config = ReflexgptpConfig(app_name="reflex_gptp")  # type: ignore
