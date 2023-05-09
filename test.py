import fitz

doc = fitz.open("example.pdf")
for page in doc:
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if block["type"] == 0:
            for line in block["lines"]:
                for span in line["spans"]:
                    color = fitz.utils.getColor(span["backgroundColor"])
                    print(span["text"], color)