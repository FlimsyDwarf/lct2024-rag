from docx import Document
from docx.shared import Pt, Inches


SUB_QUERY_SEPARATOR = '; '


def get_info_from_template(template_file, keyword):
    """
    Обрабатывает шаблон пользователя

    Args:
        template_file: путь к шаблону
        keyword: ключевое слово, по которому просиходит разбивка на блоки

    Returns: заголовок шаблона, главную тему отчета(из 2 строки) и
             разбиение файла на блоки в виде словаря:
             описание блока(первая его строка) -> все его подпункты одной строкой

    """

    template = Document(template_file)

    heading = template.paragraphs[0].text.strip()
    main_topic = template.paragraphs[1].text.strip()
    blocks = dict()

    block = ""
    block_name = ""
    for paragraph in template.paragraphs[2:]:
        paragraph = paragraph.text.lower().strip()

        if keyword in paragraph:
            if block:
                blocks[block_name] = block
            block_name = paragraph
            block = ""

        elif block_name:
            block += paragraph + SUB_QUERY_SEPARATOR

    blocks[block_name] = block

    return heading, main_topic, blocks


def create_final_report(output_file, heading, main_topic, blocks_names, reports):
    """
    Создает конечный файл, в котором будет сохранен результат работы программы

    Args:
        output_file: путь к конечному файлу, в котором будет сохранен результат
        heading: заголовок шаблона
        main_topic: главная тема отчета
        blocks_names: описания блоков
        reports: список сгенерированных ответов от модели на каждый блок

    """

    final_report = Document()

    style = final_report.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    heading = final_report.add_paragraph(heading)
    heading.runs[0].font.size = Pt(14)
    heading.runs[0].bold = True
    heading.alignment = 1

    heading = final_report.add_paragraph(main_topic)
    heading.runs[0].font.size = Pt(12)
    heading.alignment = 1

    for block_name, report in zip(blocks_names, reports):
        paragraph = final_report.add_paragraph(block_name)
        paragraph.runs[0].bold = True

        for sub_query, sub_report in report.items():
            paragraph = final_report.add_paragraph(f"{sub_query}: {sub_report}")
            paragraph.paragraph_format.left_indent = Inches(0.5)
            paragraph.style = 'List Bullet'

    final_report.save(output_file)
