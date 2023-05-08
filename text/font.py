def clean_font_name(font_name: str) -> str:
    font_name = font_name.split("+")[-1]
    font_name = font_name.replace(" ", "")
    return font_name


def format_text(text: str) -> str:
    return text.replace("\n", "\\n").replace("'", "\\'")
