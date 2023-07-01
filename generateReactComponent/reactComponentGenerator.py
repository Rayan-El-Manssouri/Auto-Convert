from text.font import format_text
from typing import List, Dict
from message_terminal.message import color_text_terminal
import json
import os
segments = []
seen = set()
processed_pages = set()

from pdfminer.high_level import extract_pages
from maths.math_utils import calculate_border_radius
from pdfminer.layout import (
    LTCurve,
)
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
output_dir = config.get("paths", "output_dir")
pdf_file = config.get("paths", "pdf_path")

for page_layout in extract_pages(pdf_file):
    

    page_number = page_layout.pageid
    if page_number in processed_pages:
        continue
    processed_pages.add(page_number)

    for element in page_layout:
        if isinstance(element, LTCurve):
            linewidth = element.linewidth
            border_radius = calculate_border_radius(element, scale_factor=0.1)
            segment = {
                "type": "courbe",
                "points": [
                    {"x": element.x0, "y": element.y0},
                    {"x": element.x1, "y": element.y1},
                ],
                "points_de_controle": [
                    {"x": element.pts[i], "y": element.pts[i + 1]}
                    for i in range(0, len(element.pts) - 1, 2)
                ],
                "borderWidth": element.linewidth,
                "border_radius": border_radius,
            }

            segments.append(segment)

page_code = ""
page_height = page_layout.height
for segment in segments:
    view_code = (
        "<CustomView color='%s' stateName='' left='%f' top='%f' text='' fontFamily='' fontSize='' valeur='' LeftText='' TopLeft='' widthView='%f' heightView='%f' />"
        % (
            "transparent",
            segment["points"][0]["x"],
            page_height - segment["points"][1]["y"],
            segment["points"][1]["x"] - segment["points"][0]["x"],
            segment["points"][1]["y"] - segment["points"][0]["y"],
        )
    )

    page_code += f"            {view_code}\n"



with open(f"{output_dir}/PdfCustomView.js", "a", encoding='utf-8') as f:
        f.write(
            """
    import React from 'react';
    import CustomView from './CustomView';
    const PdfCustomView = () => {
        return (
            <>
    """
        )
        f.write(page_code)
        f.write(
            """
            </>
        );
    };
    export default PdfCustomView;
    """
    )


page_text = ""
with open(f'{output_dir}/pdf_data.json', 'r', encoding='utf-8') as fichier:
    # Charger les données JSON dans un dictionnaire (ou une liste)
    data = json.load(fichier)

    pages = data["pages"]

    # On trie les informations du data pages, text_objects
    for page_data in pages:
        text_objects = page_data['text_objects']
        for text_object in page_data['text_objects']:
            # On récupère les informations du text_object
            text = text_object['text']
            font_name = text_object['font_name']
            font_size = text_object['font_size']
            left = text_object['x']
            top = text_object['y']
            # On formate le text
            text = format_text(text)
            # On crée le code JSX
            text_code = (
                "<Text fontFamily='%s' fontSize='%f' left='%f' top='%f'  text='%s' />"
                % (
                    font_name,
                    font_size,
                    left,
                    top,
                    text
                )
            )
            # On ajoute le code JSX à la page
            page_text += f"            {text_code}\n"
    
    
" On remplie le fichier PdfText avec les segments "
with open(f"{output_dir}/PdfText.js", "w", encoding='utf-8') as f:
    f.write(
        """
import React from 'react';
import Text from './Text';
const PdfText = () => {
    return (
        <>
"""

    )
    f.write(page_text)
    f.write(
        """
        </>
    );
};
export default PdfText;
"""
    )
def generate_react_component(json_data: Dict[str, List[Dict[str, str]]]) -> str:
    font_paths = {
        "Helvetica-Compressed": "./ttf/Helvetica-Compressed-Regular.ttf",
        "TimesNewRomanPS-BoldItalicMT": "./ttf/TimesNewRomanBoldItalic.ttf",
        "Arial-BoldMT": "./ttf/Arial-BoldMT.ttf",
        "Helvetica-Black": "./ttf/Helvetica-Black.ttf",
        "Webdings": "./ttf/Webdings.ttf",
        "Helvetica-Condensed-Bold": "./ttf/Helvetica-Condensed-Bold.ttf",
        "Helvetica-Narrow": "./ttf/Helvetica-Narrow.ttf",
        "SourceSansPro-Semibold": "./ttf/SourceSansPro-SemiBold.ttf",
        "SourceSansPro-Bold": "./ttf/SourceSansPro-Bold.ttf",
        "Wingdings-Regular": "./ttf/Wingdings-Regular.ttf",
        "Helvetica-Narrow-Bold": "./ttf/Helvetica-Narrow-Bold.ttf",
    }

    font_registers = [
        f"Font.register({{ family: '{font}', src: '{path}' }});"
        for font, path in font_paths.items()
    ]

    font_registers_str = "\n".join(font_registers)

    component = f"""
import React from 'react';
import {{ PDFViewer, Document, Page, Text }} from '@react-pdf/renderer';
import {{ Font }} from '@react-pdf/renderer';
import PdfCustomView from './PdfCustomView';
import PdfText from './PdfText';

{font_registers_str}

const PdfComponent = () => (
    <PDFViewer style={{ {{  width: '100%', height: '100vh', border: 'none', position: 'fixed' }}  }}>
"""
    for page in json_data["pages"]:
        component += f"        <Document>\n"
        component += f'        <Page size="A4">\n'
        component += f"            <PdfText />\n"
        component += f"            <PdfCustomView />\n"
        component += f"        </Page>\n"
        component += f"        </Document>\n"
    component += f"""    </PDFViewer>
);

export default PdfComponent;
"""

    return component
