import xml.etree.ElementTree as ET
from urllib import request
import os

import deepl


def main():
    # download rss feeds
    request.urlretrieve("https://www.nature.com/nature.rss", "nature.rss")
    request.urlretrieve("http://mediagazer.com/feed.xml", "mediagazer.rss")

    # deepl
    API_KEY = os.environ.get("DEEPL_KEY")
    translator = deepl.Translator(API_KEY)
    target_language = "JA"

    # parse Nature
    tree = ET.parse("nature.rss")
    root = tree.getroot()
    items = root.findall("item", {"": "http://purl.org/rss/1.0/"})

    for child in items:
        result = translator.translate_text(
            child.findall("title", {"", "http://purl.org/dc/elements/1.1/"})[0].text,
            target_lang=target_language,
        )

        child.findall("title", {"", "http://purl.org/dc/elements/1.1/"})[
            0
        ].text = result.text
        child.findall("title", {"": "http://purl.org/rss/1.0/"})[0].text = result.text
    tree.write("nature.rss", encoding="utf-8", xml_declaration=True)

    # parse mediagazer
    tree = ET.parse("mediagazer.rss")
    root = tree.getroot()

    for child in root.find("channel").findall("item"):
        title = child.find("title")
        t_title = translator.translate_text(title.text, target_lang=target_language)
        title.text = t_title.text

    tree.write("mediagazer.rss", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
