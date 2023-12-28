"""Module that contains the style definitions for the app."""

import reflex as rx

bg_dark_color = "#111"
bg_medium_color = "#222"

bg_light_color = "#fff"

border_color = "#fff3"

accent_light = "#058451"
accent_dark = "#03633c"
accent_color = f"linear-gradient(130deg, {accent_light} 20%, {accent_dark} 77.5%)"

icon_color = "#fff8"

text_light_color = "#fff"
shadow_light = "rgba(17, 12, 46, 0.15) 0px 48px 100px 0px;"
shadow = "rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;"

message_style = {
    "display": "inline-block",
    "p": "2",
    "border_radius": "xl",
    "max_w": "30em",
    "border_color": border_color,
    "border_width": "1px",
    "font_size": "md",
}

input_style = {
    "bg": bg_medium_color,
    "border_color": border_color,
    "border_width": "1px",
    "p": "4",
}

icon_style = {
    "font_size": "md",
    "color": icon_color,
    "_hover": {"color": text_light_color},
    "cursor": "pointer",
    "w": "8",
}

sidebar_style = {
    "border": "double 1px transparent;",
    "border_radius": "10px;",
    "background_image": f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accent_dark});",
    "background_origin": "border-box;",
    "background_clip": "padding-box, border-box;",
    "p": "2",
    "_hover": {
        "background_image": f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accent_light});",
    },
}

base_style = {
    rx.Avatar: {
        "shadow": shadow,
        "color": text_light_color,
        "bg": border_color,
    },
    rx.Button: {
        "shadow": shadow,
        # "color": text_light_color,
        "_hover": {
            "bg": accent_dark,
        },
    },
    rx.Menu: {
        "bg": bg_dark_color,
        "border": "red",
    },
    rx.MenuList: {
        "bg": bg_dark_color,
        "border": f"1.5px solid {bg_medium_color}",
    },
    rx.MenuDivider: {
        "border": f"1px solid {bg_medium_color}",
    },
    rx.MenuItem: {
        "bg": bg_dark_color,
        "color": text_light_color,
    },
    rx.DrawerContent: {
        "bg": bg_dark_color,
        "color": text_light_color,
        "opacity": "0.9",
    },
    rx.Hstack: {
        "justify_content": "space-between",
    },
}
