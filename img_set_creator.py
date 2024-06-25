from bs4 import BeautifulSoup


def get_html(url):
    import urllib.request
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    f = urllib.request.urlopen(req)
    return f.read().decode('utf-8')


def get_chapter_list(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    html_block_set = soup.find_all("a", class_="chapter-link cp-l")
    url_with_content = []
    for elem in html_block_set:
        url_with_content.append([elem['href'], elem.get_text().strip()])
    return url_with_content[::-1]


def get_img_set(html_doc):  # возможно потребуется выкинуть исключение если картинок на странице не будет
    soup = BeautifulSoup(html_doc, 'html.parser')
    # print(soup.prettify())
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


def main():
    print(get_img_set(get_html('')))
    print(get_chapter_list(get_html('')))


if __name__ == '__main__':
    main()
