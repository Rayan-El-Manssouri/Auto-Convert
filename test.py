from text.extract import extract_text_coords_font_from_pdf

pdf_path = "example.pdf"
pdf_data = extract_text_coords_font_from_pdf(pdf_path)
print(pdf_data)