import os

from jinja2 import Template

HTML_VIEW = os.path.dirname(__file__)


class HtmlBuilder:
    """
    Класс для построения HTML-документа с использованием шаблонов Jinja2.

    Attributes:
        template (Template): Объект шаблона Jinja2.
        context (dict): Словарь, содержащий контекст для подстановки значений в шаблон.

    Methods:
        set_title(title: str) -> HtmlBuilder:
            Устанавливает заголовок документа.

        set_body_head_title(body_head_title: str) -> HtmlBuilder:
            Устанавливает заголовок основного содержимого документа.

        set_body_middle_text(body_middle_text: str) -> HtmlBuilder:
            Устанавливает текст в середине основного содержимого документа.

        set_body_bottom_text(body_bottom_text: str) -> HtmlBuilder:
            Устанавливает текст в нижней части основного содержимого документа.

        build() -> str:
            Собирает HTML-документ, используя установленные значения и возвращает строку с HTML-кодом.
    """

    def __init__(self, template_str: str):
        """
        Инициализирует экземпляр класса.

        :param
            template_str (str): Строка с содержимым HTML-шаблона.
        """
        self.template = Template(template_str)
        self.context = {}

    def set_title(self, title: str) -> 'HtmlBuilder':
        """
        Устанавливает заголовок документа.

        :param
            title (str): Текст заголовка.

        :return
            HtmlBuilder: Текущий экземпляр HtmlBuilder для цепочки вызовов методов.
        """
        self.context['title'] = title
        return self

    def set_body_head_title(self, body_head_title: str) -> 'HtmlBuilder':
        """
        Устанавливает заголовок основного содержимого документа.

        :param
            body_head_title (str): Текст заголовка основного содержимого.

        :return
            HtmlBuilder: Текущий экземпляр HtmlBuilder для цепочки вызовов методов.
        """
        self.context['body_head_title'] = body_head_title
        return self

    def set_body_middle_text(self, body_middle_text: str) -> 'HtmlBuilder':
        """
        Устанавливает текст в середине основного содержимого документа.

        :param
            body_middle_text (str): Текст для середины основного содержимого.

        :return
            HtmlBuilder: Текущий экземпляр HtmlBuilder для цепочки вызовов методов.
        """
        self.context['body_middle_text'] = body_middle_text
        return self

    def set_body_bottom_text(self, body_bottom_text: str) -> 'HtmlBuilder':
        """
        Устанавливает текст в нижней части основного содержимого документа.

        :param
            body_bottom_text (str): Текст для нижней части основного содержимого.

        :return
            HtmlBuilder: Текущий экземпляр HtmlBuilder для цепочки вызовов методов.
        """
        self.context['body_bottom_text'] = body_bottom_text
        return self

    def build(self) -> str:
        """
        Собирает HTML-документ, используя установленные значения и возвращает строку с HTML-кодом.

        :return
            str: HTML-код с установленными значениями.
        """
        return self.template.render(**self.context)
