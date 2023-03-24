class GetPoems:
    """
   Класс собирает стихи с сайта с учётом пауз.
    """

    def __init__(self, original_link, author):
        import bs4 as bs
        import urllib.request

        self.original_link = original_link
        self.author = author
        self.source = urllib.request.urlopen(self.original_link).read()
        self.soup = bs.BeautifulSoup(self.source, "html.parser")
        self.page_links = []
        self.poem_links = []
        self.all_texts = []

        self._preparePoems()

    def _getCorpus(self):
        """
        Получает все страницы с веб-сайта, где находятся стихи Лермонтова.
        """
        import bs4 as bs
        import urllib.request

        page_links = []
        page_values = []

        # Сбор страниц
        for page in self.soup.findAll("div", class_="nav-links"):
            page_links.append(str(page))

        for page in page_links:
            # Нахождение последней страницы при условиях существования и отображения
            start_point = page.find("Последняя", 0) - 20
            new_start_point = page.find("page", start_point) + len("page/")
            end_point = page.find("/", new_start_point)
            try:
                page_value = int(page[new_start_point:end_point])
                page_values.append(page_value)
            except:
                pass

            text_pointer = 0
            while text_pointer < len(page):
                start_point = page.find("Страница", text_pointer) + len("Страница ")
                end_point = page.find(">", start_point) - 1
                try:
                    page_value = int(page[start_point:end_point])
                    page_values.append(page_value)
                except:
                    pass
                text_pointer += 1

        min_page = 0
        for value in set(page_values):
            if value > min_page:
                min_page = value

        page_links = []
        for page_value in range(1, value + 1):
            page_links.append(self.original_link + "page/" + str(page_value) + "/")

        self.page_links = page_links

    def _getPoems(self):
        """
        Получение всех ссылок на веб-сайт, которые ведут к Лермонтову.
        """
        import bs4 as bs
        import urllib.request
        import time
        import random

        self._getCorpus()

        poem_links = []
        for page in self.page_links:
            rng = random.randint(4, 8)
            time.sleep(rng)

            page_source = urllib.request.urlopen(page).read()
            soup = bs.BeautifulSoup(page_source, "html.parser")
            for poem in soup.findAll("div", class_="entry-title"):
                start_point = str(poem).find("href", 0) + len("href=") + 1
                end_point = str(poem).find(">", start_point) - 1
                poem_link = str(poem)[start_point:end_point]
                poem_links.append(poem_link)

        self.poem_links = poem_links

    def _preparePoems(self):
        """
        Сохранение всех стихов и их запись в переменную.
        """
        import bs4 as bs
        import urllib.request
        import time
        import random
        import io

        self._getPoems()
        all_text = []

        for idx, link in enumerate(self.poem_links):
            rng = random.randint(5, 15)
            time.sleep(rng)

            page_source = urllib.request.urlopen(link).read()
            soup = bs.BeautifulSoup(page_source, "html.parser")

            print(f"{idx + 1}. Обрабатывается: {soup.title.string}")

            for text in soup.findAll("div", class_="entry-content poem-text"):
                all_text.append(text.text)

        self.all_texts = all_text

        # Сохранение всех стихов
        file_name = "poems " + self.author + ".txt"
        with io.open(file_name, "w", encoding="utf-8") as output:
            for poem in self.all_texts:
                output.write(poem + "\n")

poems = GetPoems(original_link = "https://rustih.ru/mixail-lermontov/", author = "Lermontov")


class CleanPoems:
    """
    Класс, очищающий стихи.
    """

    def __init__(self, original_file):
        self.original_file = original_file
        self.new_file = ""
        self._cleanPoems()

    def _cleanPoems(self):
        import io
        import re

        # Очистка ненужного материала
        regex = re.compile("[^абвгдеёжзийклмнопрстуфхцчшщъыьэюя]")
        collector = []
        poems_file = io.open(self.original_file, "r", encoding="utf-8")

        if poems_file.mode == "r":
            contents = poems_file.readlines()
            for content in contents:
                temp_collector = []
                for word in content.split():
                    new_word = regex.sub("", word.lower())
                    if new_word != "" and new_word != " ":
                        temp_collector.append(new_word)
                collector.append(temp_collector)

        # Save the new clean poems
        self.new_file = self.original_file[:-4] + "_clean.txt"

        with io.open(self.new_file, "w", encoding="utf-8") as output:
            temp_text = " "
            for entry in collector:
                new_poem = temp_text.join(entry)
                output.write(new_poem + "\n")

poems_clean = CleanPoems(original_file = "poems Lermontov.txt")