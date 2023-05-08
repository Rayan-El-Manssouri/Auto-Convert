print("Chargement en cours...")
import json
from typing import List, Dict, Tuple
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTChar, LTCurve
from math import sqrt
from tqdm import tqdm

print("   - Chargement terminé !")

print("   - Toute les dépendance on bien été charger !")


def calculate_border_radius_v4(element, scale_factor=0.1):
    if not isinstance(element, LTCurve):
        return 0

    x0, y0 = element.x0, element.y0
    x1, y1 = element.x1, element.y1
    length = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    if len(element.pts) > 0:
        control_points = [list(p) for p in element.pts[2:]]

        if not control_points:
            return 0.0
        max_control_distance = max(
            sqrt((x0 - cx) ** 2 + (y0 - cy) ** 2) for cx, cy in control_points
        )
        border_radius = max_control_distance / 5
    else:
        border_radius = length / 2

    return border_radius * scale_factor


def calculate_curve_height(curve):
    if not isinstance(curve, LTCurve):
        return 0

    if len(curve.pts) < 2:
        return 0

    # trouver les coordonnées y des premiers et derniers points de contrôle
    y0 = curve.pts[0][1]
    y1 = curve.pts[-1][1]

    # calculer la hauteur de la courbe
    height = abs(y1 - y0)
    return height


segments = []
seen = set()
processed_pages = set()  # ensemble pour stocker les numéros de page traités


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
            height = calculate_curve_height(element)
            border_radius = calculate_border_radius_v4(element, scale_factor=0.1)
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

    page_code += "<div> %s </div>\n" % view_code


def extract_text_coords_font_from_pdf(
    pdf_path: str,
    special_chars_offsets: Dict[str, Tuple[float, float]] = None,
    block_offsets: Dict[str, Tuple[float, float]] = None,
) -> Dict[str, List[Dict[str, str]]]:
    page_data = []
    for page_layout in extract_pages(pdf_path):
        height = page_layout.height
        page_objects = []
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                for line in element:
                    line_text = ""
                    line_width = (
                        20  # Ajout d'une variable pour stocker la largeur de la ligne
                    )
                    for word in line:
                        if isinstance(word, LTChar):
                            font_size = word.size
                            font_name = clean_font_name(word.fontname)
                            text = word.get_text().strip()
                            if text:
                                text = clean_text(text)
                                if (
                                    special_chars_offsets is not None
                                    and text in special_chars_offsets
                                ):
                                    x_offset, y_offset = special_chars_offsets[text]
                                    x, y = (
                                        word.bbox[0] + x_offset,
                                        height
                                        - word.bbox[3]
                                        - word.height * font_size / 70
                                        + y_offset,
                                    )
                                else:
                                    x, y = (
                                        word.bbox[0],
                                        height
                                        - word.bbox[3]
                                        - word.height * font_size / 70,
                                    )

                                if (
                                    block_offsets is not None
                                    and line_text in block_offsets
                                ):
                                    x_offset, y_offset = block_offsets[line_text]
                                    x += x_offset
                                    y += y_offset

                                # Ajout de la largeur du mot à la largeur de la ligne
                                line_width += word.width * font_size / 70

                                x -= 13
                                page_objects.append(
                                    {
                                        "text": text,
                                        "font_name": font_name,
                                        "font_size": font_size,
                                        "x": x,
                                        "y": y,
                                    }
                                )
                                line_text += text
                    # Ajout de la condition pour ajuster la position des caractères spéciaux
                    if (
                        special_chars_offsets is not None
                        and line_text in special_chars_offsets
                    ):
                        x_offset, y_offset = special_chars_offsets[line_text]
                        for obj in page_objects[-len(line) :]:
                            obj["x"] -= line_width * x_offset
                            obj["y"] += y_offset

        if page_objects:
            page_data.append({"text_objects": page_objects})
    print("   - Extraction des données terminé !")
    return {"pages": page_data}


def clean_text(text: str) -> str:
    return text.replace("\n", "\\n").replace("'", "’")


def clean_font_name(font_name: str) -> str:
    font_name = font_name.split("+")[-1]
    font_name = font_name.replace(" ", "")
    return font_name


def format_text(text: str) -> str:
    return text.replace("\n", "\\n").replace("'", "\\'")


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
            component += f"            <Text style={{  {{ position: 'absolute', left: {text_obj['x'] + 10}, top: {text_obj['y']}, zIndex: 2, fontSize: {text_obj['font_size']}, fontFamily: '{text_obj['font_name']}' }} }}>"
            component += f"                {format_text(text_obj['text'])}"
            component += f"            </Text>\n"
            component += f"           "
        component += f"        {page_code}\n"
        component += f"        </Page>\n"
        component += f"        </Document>\n"

    component += f"""    </PDFViewer>
);

export default PdfComponent;
"""

    print("Génération du code terminé !")
    return component


pdf_path = "example.pdf"
json_path = "example.json"
react_component_path = "PdfComponent.js"

# extract text and font information from the PDF file
pdf_data = extract_text_coords_font_from_pdf(pdf_path)

# write extracted data to a JSON file with UTF-8 encoding
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(pdf_data, f, ensure_ascii=False, indent=4)

# generate a React component that renders the PDF
react_component = generate_react_component(pdf_data)

# write the React component to a file with UTF-8 encoding
with open(react_component_path, "w", encoding="utf-8") as f:
    f.write(react_component)
