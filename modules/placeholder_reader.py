import re
from docx import Document

def get_placeholders(doc_path):

    doc = Document(doc_path)

    placeholders = []
    seen = set()

    pattern = r"{{(.*?)}}"

    def add_placeholders(text):
        matches = re.findall(pattern, text)

        for match in matches:
            field = match.strip()

            if field not in seen:
                seen.add(field)
                placeholders.append(field)

    # Read placeholders from paragraphs
    for para in doc.paragraphs:
        add_placeholders(para.text)

    # Read placeholders from tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                add_placeholders(cell.text)

    return placeholders