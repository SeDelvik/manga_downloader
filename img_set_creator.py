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
zip_dir = os.path.join(temporary_dir, 'pdf')


def get_html(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    f = urllib.request.urlopen(req)
    return f.read().decode('utf-8')


def get_chapter_list(url):
    html_doc = get_html(url + '/vol1/1')
    soup = BeautifulSoup(html_doc, 'html.parser')
    html_block_set = soup.find_all("a", class_="chapter-link cp-l")
    url_with_content = []
    for elem in html_block_set:
        url_with_content.append([elem['href'], elem.get_text().strip()])
    return url_with_content[::-1]


def get_img_set(url):  # возможно потребуется выкинуть исключение если картинок на странице не будет
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


def get_pdf_file(file_name, url_image_set):
    create_tmp_dir()
    print(os.path.join(abs_path_project, temporary_dir))
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


def create_tmp_dir():
    if not os.path.isdir(temporary_dir):
        os.mkdir(temporary_dir)
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    if not os.path.isdir(pdf_dir):
        os.mkdir(pdf_dir)
    if not os.path.isdir(zip_dir):
        os.mkdir(zip_dir)


def drop_tmp_dir():
    if os.path.isdir(temporary_dir):
        shutil.rmtree(temporary_dir)


def drop_images_dir():
    if os.path.isdir(image_dir):
        shutil.rmtree(image_dir)


def drop_pdf_dir():
    if os.path.isdir(pdf_dir):
        shutil.rmtree(pdf_dir)


def create_zip(zip_name):
    shutil.make_archive(os.path.join(zip_dir, zip_name), 'zip', pdf_dir)
    return os.path.join(zip_dir, f'{zip_name}.zip')


def main():
    # print(get_img_set(get_html('')))
    # print(get_chapter_list(get_html('')))
    gis = get_img_set('')
    # print(gis)
    get_pdf_file('test.pdf', gis)


if __name__ == '__main__':
    main()
