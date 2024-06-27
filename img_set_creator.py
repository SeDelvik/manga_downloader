import shutil
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from PIL import Image
import urllib.request
import os

temporary_dir = './.tmp/'


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
    if not os.path.isdir(temporary_dir):
        os.mkdir(temporary_dir)
    pdf = canvas.Canvas(temporary_dir + file_name)
    for i in range(len(url_image_set)):
        urllib.request.urlretrieve(
            url_image_set[i],
            temporary_dir + f"{i}.png")
        img = Image.open(temporary_dir + f"{i}.png")
        list_height = 595
        list_width = 842
        padding = 10
        x = 0
        y = 0
        img_height, img_width = img.size
        cfc_h = (list_height / img_height)
        cfc_w = (list_width / img_width)

        if cfc_h < cfc_w:
            print('1', int(img_height * cfc_h), int(img_width * cfc_h))
            img = img.resize((int(img_height * cfc_h) - padding * 2, int(img_width * cfc_h) - padding * 2))
            y = int((list_width - int(img_width * cfc_h)) / 2)
        else:
            print('2', int(img_height * cfc_w), int(img_width * cfc_w))
            img = img.resize((int(img_height * cfc_w) - padding * 2, int(img_width * cfc_w) - padding * 2))
            x = int((list_height - int(img_height * cfc_w)) / 2)

        img.save(temporary_dir + f"{i}.png")
        pdf.drawImage(temporary_dir + f"{i}.png", x=x + padding, y=y + padding)
        pdf.showPage()
    pdf.save()


def drop_tmp_dir():
    if os.path.isdir(temporary_dir):
        shutil.rmtree(temporary_dir)


def main():
    # print(get_img_set(get_html('')))
    # print(get_chapter_list(get_html('')))
    gis = get_img_set('')
    # print(gis)
    get_pdf_file('test.pdf', gis)


if __name__ == '__main__':
    main()
