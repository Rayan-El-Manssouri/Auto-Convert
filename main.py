import json
import re
from typing import List, Dict
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTAnno, LTTextBox
from pdfminer.layout import LTTextBoxHorizontal
from typing import Dict, List
import re
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTChar


def extract_text_coords_font_from_pdf(pdf_path: str) -> Dict[str, List[Dict[str, str]]]:
    page_data = []
    for page_layout in extract_pages(pdf_path):
        height = page_layout.height
        page_objects = []
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                for line in element:
                    line_text = ""
                    for word in line:
                        if isinstance(word, LTChar):
                            font_size = word.size
                            font_name = clean_font_name(word.fontname)
                            text = word.get_text().strip()
                            if text:
                                text = clean_text(text)
                                line_text += text
                                x, y = word.bbox[0], height - word.bbox[3]
                                page_objects.append(
                                    {'text': text, 'font_name': font_name, 'font_size': font_size, 'x': x, 'y': y})
                    if line_text:
                        line_text = clean_text(line_text)
                        x, y = line.bbox[0], height - line.bbox[3]
                        page_objects.append(
                            {'text': line_text, 'font_name': font_name, 'font_size': font_size, 'x': x, 'y': y})
        if page_objects:
            page_data.append({'text_objects': page_objects})
    return {'pages': page_data}


def clean_text(text: str) -> str:
    text = re.sub(r'[\n\t]+', ' ', text)
    text = re.sub(r'[ ]+', ' ', text)
    text = text.encode('utf-8', 'ignore').decode('utf-8')
    return text


def clean_font_name(font_name: str) -> str:
    font_name = font_name.split('+')[-1]
    font_name = font_name.replace(' ', '')
    return font_name


def format_text(text: str) -> str:
    return text.replace('\n', '\\n').replace("'", "\\'")


def generate_react_component(json_data: Dict[str, List[Dict[str, str]]]) -> str:
    component = f"""
import React from 'react';
import {{ PDFViewer, Document, Page, Text }} from '@react-pdf/renderer';

const PdfComponent = () => (
    <PDFViewer style={{ {{width: '100%', height: '100vh', border: 'none', position: 'fixed' }} }}>
"""
    for page in json_data['pages']:
        component += f"        <Document>\n"
        component += f"        <Page size=\"A4\">\n"
        for text_obj in page['text_objects']:
            component += f"            <Text style={{  {{ position: 'absolute', left: {text_obj['x']}, top: {text_obj['y']}, fontSize: {text_obj['font_size']} }} }}>"
            component += f"                {format_text(text_obj['text'])}"
            component += f"            </Text>\n"
        component += f"        </Page>\n"
        component += f"        </Document>\n"

    component += f"""    </PDFViewer>
);

export default PdfComponent;
"""

    return component


pdf_path = 'example.pdf'
json_path = 'example.json'
react_component_path = 'PdfComponent.js'

# extract text and font information from the PDF file
pdf_data = extract_text_coords_font_from_pdf(pdf_path)

# write extracted data to a JSON file
with open(json_path, 'w') as f:
    json.dump(pdf_data, f, indent=4)

# generate a React component that renders the PDF
react_component = generate_react_component(pdf_data)

# write the React component to a file
with open(react_component_path, 'w') as f:
    f.write(react_component)
