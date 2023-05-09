from text.font import format_text
from typing import List, Dict


segments = []
seen = set()
processed_pages = set()  # ensemble pour stocker les numéros de page traités
from pdfminer.high_level import extract_pages
from maths.math_utils import calculate_border_radius
from pdfminer.layout import (
    LTCurve,
)
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
output_dir = config.get("paths", "output_dir")


for page_layout in extract_pages("example.pdf"):
    print("   - Traitement de la page en cours !")
    page_number = page_layout.pageid  # obtenir le numéro de page actuel
    if page_number in processed_pages:
        continue  # passer à la page suivante si la page a déjà été traitée
    processed_pages.add(
        page_number
    )  # ajouter le numéro de la page actuelle à l'ensemble des pages traitées

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
                "borderColor": element.stroking_color,
                "borderWidth": element.linewidth,
                "border_radius": border_radius,
            }

            # Vérifier si la courbe a déjà été ajoutée en comparant les coordonnées des points de contrôle
            coords = frozenset((p["x"], p["y"]) for p in segment["points_de_controle"])

            if coords not in seen:
                # Ajouter le dictionnaire à la liste des segments de courbe et stocker les coordonnées dans l'ensemble
                segments.append(segment)
                seen.add(coords)

# Générer le code pour chaque vue
page_code = ""
page_height = page_layout.height  # obtenir la hauteur de la page actuelle
for segment in segments:
    view_code = (
        "<div style={{  position: 'absolute', top: %f, left: %f, width: %f, height: %f, color: 'rgb%s', backgroundColor: '%s', zIndex: 1, borderWidth: %f, borderRadius: %f, padding: 0  }} />"
        % (
            page_height - segment["points"][1]["y"],  # inverser la valeur du top
            segment["points"][0]["x"],
            segment["points"][1]["x"] - segment["points"][0]["x"],
            segment["points"][1]["y"] - segment["points"][0]["y"],
            segment["borderColor"],  # couleur de la bordure
            "transparent",  # couleur de fond
            segment["borderWidth"],  # texte
            segment["border_radius"],
        )
    )

    page_code += f"            <div>%s </div>\n" % view_code


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

{font_registers_str}

const PdfComponent = () => (
    <PDFViewer style={{ {{  width: '100%', height: '100vh', border: 'none', position: 'fixed' }}  }}>
"""
    for page in json_data["pages"]:
        component += f"        <Document>\n"
        component += f'        <Page size="A4">\n'
        for text_obj in page["text_objects"]:
            component += f"            <Text style={{  {{ position: 'absolute', left: {text_obj['x'] + 10}, top: {text_obj['y']}, zIndex: 2, fontSize: {text_obj['font_size']}, fontFamily: '{text_obj['font_name']}' }} }}> {format_text(text_obj['text'])}  </Text>\n"
        component += f"        {page_code}\n"
        component += f"        </Page>\n"
        component += f"        </Document>\n"

    component += f"""    </PDFViewer>
);

export default PdfComponent;
"""

    print("Génération du code terminé !")
    print("Le fichier est dans le répertoir :", output_dir )
    return component
