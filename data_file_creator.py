import shutil
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from PIL import Image
import urllib.request
import os

abs_path_project = os.path.dirname(os.path.abspath(__file__))
temporary_dir = os.path.join(abs_path_project, '.tmp')
image_dir = os.path.join(temporary_dir, 'img')
pdf_dir = os.path.join(temporary_dir, 'pdf')
zip_dir = os.path.join(temporary_dir, 'zip')

static_dir = './static'


def get_html(url: str) -> str:
    """
    Возвращает html документ, скачанный по переданной ссылке.
    :param url: Внешняя ссылка
    :return: Содержимое html-документа
    """
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    f = urllib.request.urlopen(req)
    return f.read().decode('utf-8')


def get_chapter_list(url: str) -> list[list[str]]:
    """
    Возвращает двумерный список со ссылками на главы.
    :param url: Внешняя ссылка, ведущая на основной ресурс
    :return: Список с вложенными списками формата: [ссылка_на_главу, название_главы]
    """
    html_doc = get_html(url + '/vol1/1?mtr=true')
    soup = BeautifulSoup(html_doc, 'html.parser')
    html_block_set = soup.find_all("a", class_="chapter-link cp-l")
    if len(html_block_set) < 1:
        html_block_set = soup.find_all("a", class_="chapter-link cp-l manga-mtr")
    url_with_content = []
    for elem in html_block_set:
        url_with_content.append([url + '/' + '/'.join(elem['href'].split('/')[2:]),
                                 # сборка полной внешней ссылки так как ссылка на главу приходит обрезанная
                                 elem.get_text().strip()])
    # if len(url_with_content) < 1:  # correct but not manga url
    #     raise ValueError
    return url_with_content[::-1]


def get_img_set(url: str) -> list[str]:
    """
    Из полученного url главы создает список ссылок на изображения.
    :param url: Внешняя ссылка на главу.
    :return: Список внешних ссылок на изображения
    """
    html_doc = get_html(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    html_block_set = soup.find_all("script")
    script_source_bock = ''
    for block in html_block_set:
        if 'readerDoInit' in block.get_text():
            script_source_bock = block.get_text()
            break
    raw_url_strings = (((script_source_bock.split('readerDoInit')[1]).split('false')[0])[3:-4]).split('],[')
    pretty_urls = []
    for raw_url in raw_url_strings:
        tmp = raw_url.split(',')
        url = tmp[0].replace("'", '') + tmp[2].replace('"', '')
        pretty_urls.append(url)
    return pretty_urls


def get_pdf_file(file_name: str, url_image_set: list[str]) -> str:
    """
    На основе списка внешних ссылок на изображения создает во временной папке pdf файл с заданным названием.
    :param file_name: Имя выходного pdf-файла.
    :param url_image_set: Список внешних ссылок.
    :return: Абсолютный путь до созданного pdf-файла.
    """
    create_tmp_dir()
    pdf = canvas.Canvas(os.path.join(pdf_dir, f'{file_name}.pdf'))
    for i in range(len(url_image_set)):
        abs_tmp_img_path = os.path.join(image_dir, f'{i}.png')
        urllib.request.urlretrieve(
            url_image_set[i],
            abs_tmp_img_path

        )
        img = Image.open(abs_tmp_img_path)
        list_height = 595
        list_width = 842
        padding = 10
        x = 0
        y = 0
        img_height, img_width = img.size
        cfc_h = (list_height / img_height)
        cfc_w = (list_width / img_width)

        if cfc_h < cfc_w:
            img = img.resize((int(img_height * cfc_h) - padding * 2, int(img_width * cfc_h) - padding * 2))
            y = int((list_width - int(img_width * cfc_h)) / 2)
        else:
            img = img.resize((int(img_height * cfc_w) - padding * 2, int(img_width * cfc_w) - padding * 2))
            x = int((list_height - int(img_height * cfc_w)) / 2)

        img.save(abs_tmp_img_path)
        pdf.drawImage(abs_tmp_img_path, x=x + padding, y=y + padding)
        pdf.showPage()
    pdf.save()
    drop_images_dir()
    return os.path.join(pdf_dir, f'{file_name}.pdf')


def create_tmp_dir() -> None:
    """
    Создает временные папки для хранения файлов.
    :return:
    """
    if not os.path.isdir(temporary_dir):
        os.mkdir(temporary_dir)
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    if not os.path.isdir(pdf_dir):
        os.mkdir(pdf_dir)
    if not os.path.isdir(zip_dir):
        os.mkdir(zip_dir)


def drop_tmp_dir() -> None:
    """
    Рекурсивно удаляет временную папку и ее содержимое.
    :return:
    """
    if os.path.isdir(temporary_dir):
        shutil.rmtree(temporary_dir)


def drop_images_dir() -> None:
    """
    Рекурсивно удаляет временную папку с изображениями для одной главы
    :return:
    """
    if os.path.isdir(image_dir):
        shutil.rmtree(image_dir)


def drop_pdf_dir() -> None:
    """
    Рекурсивно удаляет временную папку с pdf файлами
    :return:
    """
    if os.path.isdir(pdf_dir):
        shutil.rmtree(pdf_dir)


def create_content(url_arr: list[str], output_file_name: str) -> str:
    """
    На основе списка внешних ссылок на главы создает zip архив с заданным названием,
    содержащий в себе pdf файлы с главами.
    :param url_arr: Список внешних ссылок на главы.
    :param output_file_name: Имя zip архива.
    :return: Абсолютный путь до созданного zip архива.
    """
    for url_vol in url_arr:
        img_set = get_img_set(url_vol)
        get_pdf_file(str(url_vol.split('/')[-1].split('?')[0]), img_set)
    shutil.make_archive(os.path.join(zip_dir, output_file_name), 'zip', pdf_dir)
    drop_pdf_dir()
    return os.path.join(zip_dir, f'{output_file_name}.zip')


def get_image(url: str) -> str:
    """
    По переданному url возвращает обложку манги.
    :param url: Внешняя ссылка на мангу
    :return: Внутренняя ссылка на изображение
    """
    html_doc = get_html(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    div_set = soup.find_all("div", class_="picture-fotorama")
    img_url = div_set[0].find_all("img")[0]['src']
    path = os.path.join(static_dir, 'title.png')
    urllib.request.urlretrieve(
        img_url,
        path
    )
    return path


def get_title_name(url: str) -> str:
    """
    По переданному url возвращает название тайтла.
    :param url: Внешняя ссылка на мангу
    :return: Название тайтла
    """
    html_doc = get_html(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    title_dom = soup.find("title")
    title_text = title_dom.get_text().split(")")[0].strip() + ")"
    return title_text


def main():
    pass


if __name__ == '__main__':
    main()
