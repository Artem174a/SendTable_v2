import os

from database import Database
from html_creator import HtmlBuilder, HTML_VIEW
from mail import Mailing
from storage import CompileDataFrame, FileTypes

SENDER_EMAIL = 'artem174a@yandex.ru'
SENDER_PASSWORD = 'lfmijajpyogsgjzu'
DEFAULT_HTML_VIEW = 'default.html'
CONNECTION_DICT = {
    'user': 'admin_bi',
    'password': '0sdJJ@dfkjnd(',
    'host': 'rc1b-pvn8micwa381zshn.mdb.yandexcloud.net',
    'port': '6432',
    'database': 'gulliver_bi'
}


def create_html():
    with open(os.path.join(HTML_VIEW, DEFAULT_HTML_VIEW), 'r') as file:
        html_builder = HtmlBuilder(file.read())

    html_content = html_builder \
        .set_title("A Simple Responsive HTML Email") \
        .set_body_head_title("Your Head Title") \
        .set_body_middle_text("Your Middle Text Here") \
        .set_body_bottom_text("Your Bottom Text Here") \
        .build()

    return html_content


if __name__ == "__main__":
    # Получаем данные
    dataframe = Database(CONNECTION_DICT).enquiry(
        scheme='raw_data_layer',
        table_name='test',
        query='default.sql'
    )

    # Сохраняем данные в файл
    dataframe_saver = CompileDataFrame(data_frame=dataframe, filename='test_file')
    excel_filepath = dataframe_saver.create_file(FileTypes.EXCEL_FILE)  # Сохраняем данные в excel

    # Другие форматы
    # csv_filepath = dataframe_saver.create_file(FileTypes.CSV_FILE)  # Сохраняем данные в csv
    # hdf_filepath = dataframe_saver.create_file(FileTypes.H5_FILE)  # Сохраняем данные в hdf
    # json_filepath = dataframe_saver.create_file(FileTypes.JSON_FILE)  # Сохраняем данные в json
    # parquet_filepath = dataframe_saver.create_file(FileTypes.PARQUET_FILE)  # Сохраняем данные в parquet

    # print(f'{csv_filepath =}\n{excel_filepath =}\n{hdf_filepath =}\n{json_filepath =}\n{parquet_filepath =}')

    # Отправляем на почту
    # mail_app = Mailing(SENDER_EMAIL, SENDER_PASSWORD)
    # mail_app.run_mailing(
    #     subject="Тема",
    #     body="Отправка файла",
    #     recipients=['artem174a@yandex.ru'],
    #     file_path=excel_filepath,
    #     html_message=create_html()
    # )
