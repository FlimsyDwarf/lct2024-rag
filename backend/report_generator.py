import models.rag as RAG
from data_parser import get_info_from_template, create_final_report, make_single_query

from tqdm import tqdm
import os

TEMPLATE_KEYWORD = "блок"
DATA_PATH = "./data"
TEMPLATE_NAME = "shablon.docx"
REPORT_NAME = "report.docx"


class ReportGenerator:

    def __init__(self, web_search, user_sources, date_range, suffix, amount_of_links):
        self.pipeline = RAG.Pipeline(
            web_search, user_sources, date_range, suffix, amount_of_links)
        self.suffix = suffix

    def generate_report(self):
        # разбиение на блоки и подпункты
        heading, main_topic, blocks = get_info_from_template(
            os.path.join(DATA_PATH, self.suffix, TEMPLATE_NAME), TEMPLATE_KEYWORD)

        # вызов пайплайна для каждого подпункта каждого блока
        reports = dict()
        for block_name, block_queries in tqdm(blocks.items(), desc="Block", postfix="\n"):

            print("---" * 4, "||  Блок  ||", "---" * 4)
            print(block_name)
            print('\t', end='')
            print(*block_queries, sep='\n\t')
            print("---" * 12)

            reports[block_name] = dict()
            for sub_query in tqdm(block_queries, desc="SubQuery", postfix="\n"):
                reports[block_name][sub_query] = self.pipeline.generate_block(
                    make_single_query(main_topic, block_name, sub_query, TEMPLATE_KEYWORD))

        # сохранение в папку output
        create_final_report(os.path.join(DATA_PATH, self.suffix + REPORT_NAME), heading,
                            main_topic, reports, TEMPLATE_KEYWORD)


if __name__ == '__main__':
    rg = ReportGenerator(True, '', '', '', 5)
    rg.generate_report()
