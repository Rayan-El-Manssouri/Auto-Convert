from message_terminal.message import color_text_terminal

color_text_terminal("Chargement en cours...", "red", 0.01)


import json
import os
from text.extract import extract_text_coords_font_from_pdf
from generateReactComponent.reactComponentGenerator import generate_react_component
import configparser


config = configparser.ConfigParser()
config.read("config.ini")
pdf_path = config.get("paths", "pdf_path")
json_path = config.get("paths", "json_path")
react_component_path = config.get("paths", "react_component_path")
output_dir = config.get("paths", "output_dir")
pdf_data = extract_text_coords_font_from_pdf(pdf_path)
react_component = generate_react_component(pdf_data)


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(os.path.join(output_dir, "pdf_data.json"), "w", encoding="utf-8") as f:
    json.dump(pdf_data, f, ensure_ascii=False, indent=4)


with open(os.path.join(output_dir, "react_component.js"), "w", encoding="utf-8") as f:
    f.write(react_component)
