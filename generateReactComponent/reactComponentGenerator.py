from text.font import format_text
from typing import List, Dict
import json

segments = []
seen = set()
processed_pages = set()

from pdfminer.high_level import extract_pages
from maths.math_utils import calculate_border_radius
from pdfminer.layout import LTCurve, LTPage
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
output_dir = config.get("paths", "output_dir")
pdf_file = config.get("paths", "pdf_path")


def get_pdf_orientation(pdf_file):
    # Obtenir les pages du PDF
    pages = list(extract_pages(pdf_file))

    if not pages:
        raise ValueError("Le document PDF ne contient aucune page.")

    # Obtenir la première page du PDF
    first_page = pages[0]

    # Vérifier si la page est une instance de LTPage (Layout Page)
    if not isinstance(first_page, LTPage):
        raise ValueError("La première page du PDF n'est pas valide.")

    # Obtenir la rotation de la page (0 pour portrait, 90 ou 270 pour paysage)
    rotation = first_page.rotate

    # Déterminer l'orientation
    if rotation in [0, 180]:
        return "portrait"
    elif rotation in [90, 270]:
        return "landscape"
    else:
        # On ne peut pas déterminer l'orientation du PDF
        raise ValueError(
            "L'orientation du PDF ne peut pas être déterminée. il doit être en portrait ou en paysage."
        )


orientation = get_pdf_orientation(pdf_file)


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
        "<CustomView color='%s' left='%f' top='%f' widthView='%f' heightView='%f' />"
        % (
            "transparent",
            segment["points"][0]["x"]- 13,
            page_height - segment["points"][1]["y"],
            segment["points"][1]["x"] - segment["points"][0]["x"],
            segment["points"][1]["y"] - segment["points"][0]["y"],
        )
    )

    page_code += f"            {view_code}\n"


page_text = ""
with open(f"{output_dir}/pdf_data.json", "r", encoding="utf-8") as fichier:
    # Charger les données JSON dans un dictionnaire (ou une liste)
    data = json.load(fichier)

    pages = data["pages"]

    # On trie les informations du data pages, text_objects
    for page_data in pages:
        text_objects = page_data["text_objects"]
        for text_object in page_data["text_objects"]:
            # On récupère les informations du text_object
            text = text_object["text"]
            font_name = text_object["font_name"]
            font_size = text_object["font_size"]
            left = text_object["x"]
            top = text_object["y"]
            # On formate le text
            text = format_text(text)
            # On crée le code JSX
            text_code = (
                "<Text fontFamily='%s' fontSize='%f' left='%f' top='%f'  text='%s' />"
                % (font_name, font_size, left, top, text)
            )
            # On ajoute le code JSX à la page
            page_text += f"            {text_code}\n"


" On remplie le fichier PdfText avec les segments "
with open(f"{output_dir}/PdfText.js", "w", encoding="utf-8") as f:
    f.write(
        """
import React from 'react'
import  Text  from './Text';
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

    with open(f"{output_dir}/PdfCustomView.js", "w", encoding="utf-8") as f:
        f.write(
            f"""
import React from 'react';
import CustomView from './CustomView/CustomView';
const PdfCustomView = () => {{
    return (
        <>
{page_code}
        </>
    );
}};
export default PdfCustomView;
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
import {{ PDFViewer, Document, Page }} from '@react-pdf/renderer';
import {{ Font }} from '@react-pdf/renderer';
import PdfCustomView from './PdfCustomView';
import PdfText from './PdfText';

{font_registers_str}

const PdfComponent = () => (
    <PDFViewer style={{ {{  width: '100%', height: '100vh', border: 'none', position: 'fixed' }}  }}>
"""
    for index, page in enumerate(json_data["pages"]):
        component += f"        <Document>\n"
        component += f'        <Page size="A4" orientation="{orientation}">\n'
        component += f"            <PdfText />\n"
        component += f"            <PdfCustomView />\n"
        component += f"        </Page>\n"
        component += f"        </Document>\n"
    component += f"""    </PDFViewer>
);

export default PdfComponent;
"""

    return component
