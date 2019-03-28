import io
import json
from lxml import etree
import requests
import unidecode

url_archives = 'http://grantland.com/features/complete-column-archives-grantland-edition/'

XPATH_BLOG_TEXT = "//div[@class='blog-body']/p/text()"
XPATH_LINKS = '//*[@id="layout-main"]/div[1]/p/a/@href'


def make_request_with_xpath(url, xpath):
    response = requests.get(url)
    root = etree.HTML(response.content)
    content = root.xpath(xpath)

    return content

def get_links():
    list_of_urls = make_request_with_xpath(url_archives, XPATH_LINKS)

    return list_of_urls

def get_blog_data(url):
    blog_paragraphs = make_request_with_xpath(url, XPATH_BLOG_TEXT)
    clean_paragraphs = [unidecode.unidecode(paragraph) for paragraph in blog_paragraphs]
    raw_text = "\n".join(clean_paragraphs)
    clean_text = raw_text.replace("\'","")

    return clean_text

def parse_blog_data(url, clean_text):

    row = {
        'url': url,
        'blog_text': clean_text
    }

    return row

if __name__ == '__main__':
    archive_urls = get_links()

    raw_data = []

    for url in archive_urls:
        print(url)
        try:
            clean_text = get_blog_data(url)
            row = parse_blog_data(url, clean_text)
            raw_data.append(row)
        except Exception as e:
            print(e)

    simmons_data = {'data': raw_data}

    with open('data/simmons.json', 'w') as outfile:
        json.dump(simmons_data, outfile)
