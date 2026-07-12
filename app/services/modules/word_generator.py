from docxtpl import DocxTemplate

def generate_word(template_path, output_path, data):

    doc = DocxTemplate(template_path)

    doc.render(data)

    doc.save(output_path)