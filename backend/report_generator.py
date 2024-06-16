import models.rag as RAG
from data_parser import get_info_from_template, create_final_report

from tqdm import tqdm
import os


DATA_PATH = "./data"
TEMPLATE_KEYWORD = "блок"
TEMPLATE_NAME = "shablon.docx"
REPORT_NAME = "report.docx"


def make_single_query(main_topic, block_name, block_queries):
    return f"{main_topic}: {block_name}: {block_queries}"


class ReportGenerator:

    def __init__(self, web_search, user_sources, date_range, suffix):
        self.pipeline = RAG.Pipeline(
            web_search, user_sources, date_range, suffix)
        self.suffix = suffix

    def generate_report(self):
        # разбиение на блоки
        heading, main_topic, blocks = get_info_from_template(
            os.path.join(DATA_PATH, self.suffix, TEMPLATE_NAME), TEMPLATE_KEYWORD)

        # вызов пайплайна для каждого блока
        reports = list()
        for block_name, block_queries in tqdm(blocks.items()):
            reports.append(self.pipeline.generate_block(
                make_single_query(main_topic, block_name, block_queries)))

        # сохранение в папку output
        create_final_report(os.path.join(DATA_PATH, self.suffix + REPORT_NAME), heading,
                            main_topic, blocks.keys(), reports)
