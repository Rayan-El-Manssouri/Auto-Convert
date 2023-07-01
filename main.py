from message_terminal.message import color_text_terminal
color_text_terminal("Chargement en cours...", "red", 0.01)
color_text_terminal("Traitement des données du PDF...", "red", 0.01)
import json
import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
pdf_path = config.get("paths", "pdf_path")
output_dir = config.get("paths", "output_dir")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


from text.extract import extract_text_coords_font_from_pdf
pdf_data = extract_text_coords_font_from_pdf("example.pdf")
pdf_data_output_file = os.path.join(output_dir, "pdf_data.json")


with open(os.path.join(output_dir, "pdf_data.json"), "w", encoding="utf-8") as f:
    json.dump(pdf_data, f, ensure_ascii=False, indent=4)

from generateReactComponent.reactComponentGenerator import generate_react_component
react_component_path = config.get("paths", "react_component_path")


react_component = generate_react_component(pdf_data)

output_dir = config.get("paths", "output_dir")

config.read("config.ini")
react_component_path = config.get("paths", "react_component_path")

react_component = generate_react_component(pdf_data)
custom_view_dir = os.path.join(output_dir, "CustomView")

if not os.path.exists(custom_view_dir):
    os.makedirs(custom_view_dir)

view_component = """import React from 'react';
  const CustomView = ({ color,  left, top, widthView, heightView }) => {

  const width = widthView ? widthView : 10;
  const height = heightView ? heightView : 10;
  return (
    <div
      style={{
        width: width,
        height: height,
        borderWidth: 0.25,
        borderColor: color,
        backgroundColor: 'transparent',
        position: 'absolute',
        left: left,
        top: top,
        zIndex: 0,
      }}
    >
    </div>
  );
};

export default CustomView;

"""

text_component = """
import React from 'react';
import { Text as PDFText } from '@react-pdf/renderer';

const Text = ({ fontFamily, fontSize, left, top, text }) => (
  <PDFText
    style={{
      fontFamily: fontFamily,
      fontSize: fontSize,
      left: left,
      top: top,
      position: 'absolute',
      zIndex: 1,
    }}
  >
    {text}
  </PDFText>
);

export default Text;

"""

with open(os.path.join(output_dir, "Text.js"), "w", encoding="utf-8") as f:
    f.write(text_component)

with open(os.path.join(custom_view_dir, "CustomView.js"), "w", encoding="utf-8") as f:
    f.write(view_component)

with open(os.path.join(output_dir, "react_component.js"), "w", encoding="utf-8") as f:
    f.write(react_component)

" Suppression des fichiers temporaires "
os.remove(pdf_data_output_file)
color_text_terminal("Chargement terminé !", "green", 0.01)
