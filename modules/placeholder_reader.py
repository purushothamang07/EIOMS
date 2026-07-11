import re
from docx import Document

def get_placeholders(doc_path):

    doc = Document(doc_path)

    placeholders = set()

    pattern = r"{{(.*?)}}"

    for para in doc.paragraphs:

        matches = re.findall(pattern, para.text)

        for m in matches:
            placeholders.add(m.strip())

    for table in doc.tables:

        for row in table.rows:

            for cell in row.cells:

                matches = re.findall(pattern, cell.text)

                for m in matches:
                    placeholders.add(m.strip())

    return sorted(placeholders)