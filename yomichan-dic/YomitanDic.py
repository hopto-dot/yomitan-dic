import json
import os
import zipfile
from html import escape

class DicEntry:
    def __init__(self, word, reading, tag="", definition=None):
        self.word = word
        self.reading = reading
        self.tag = tag
        self.content = []
        if definition:
            self.set_simple_content(definition)


    def to_list(self):
        return [
            self.word,
            self.reading,
            self.tag,
            "",
            0,
            [{"type": "structured-content", "content": self.content}],
            0,
            ""
        ]

    def add_element(self, element):
        self.content.append(element)

    def set_simple_content(self, definition):
        self.content = [
            create_html_element("p", definition)
        ]

    def set_link_content(self, definition, link):
        self.content = [
            create_html_element("ul", [
                create_html_element("li", definition)
            ], data={"wikipedia": "abstract"}),

            create_html_element("ul", [
                create_html_element("li", [create_html_element("a", link, href=link)])
            ], style={"listStyleType": "\"⧉\""}, data={"wikipedia": "continue-reading"})
        ]

class Dictionary:
    def __init__(self, dictionary_name):
        self.dictionary_name = dictionary_name
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def export(self):
        folder_name = self.dictionary_name
        os.makedirs(folder_name, exist_ok=True)

        # Save index.json
        index_json = {
            "title": self.dictionary_name,
            "format": 3,
            "revision": "1"
        }
        index_file = os.path.join(folder_name, "index.json")
        with open(index_file, 'w', encoding='utf-8') as out_file:
            json.dump(index_json, out_file, ensure_ascii=False, indent=2)

        file_counter = 1
        entry_counter = 0
        dictionary = []
        entry_id = 1

        for entry in self.entries:
            entry_list = entry.to_list()
            entry_list[6] = entry_id
            dictionary.append(entry_list)
            entry_counter += 1
            entry_id += 1

            if entry_counter >= 10000:
                output_file = os.path.join(folder_name, f"term_bank_{file_counter}.json")
                with open(output_file, 'w', encoding='utf-8') as out_file:
                    json.dump(dictionary, out_file, ensure_ascii=False, indent=2)
                dictionary = []
                file_counter += 1
                entry_counter = 0

        if dictionary:
            output_file = os.path.join(folder_name, f"term_bank_{file_counter}.json")
            with open(output_file, 'w', encoding='utf-8') as out_file:
                json.dump(dictionary, out_file, ensure_ascii=False, indent=2)

    def zip(self):
        zip_file_name = f"{self.dictionary_name}.zip"
        with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.dictionary_name):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, self.dictionary_name))

def create_html_element(tag, content, href=None, style=None, data=None):
    element = {"tag": tag, "content": content}
    if href:
        element["href"] = href
    if style:
        element["style"] = style
    if data:
        element["data"] = data
    return element

if __name__ == "__main__":
    # Usage example
    from Dictionary_Advanced import DicEntry, Dictionary, create_html_element

    # Create a dictionary to add entries to
    dictionary = Dictionary("Example_Dictionary")

    # Method 1: The simplest way of creating an entry
    entry1 = DicEntry("踊る", "おどる", definition="To dance")
    dictionary.add_entry(entry1)

    # Method 2: set_link_content() sets the definition content to a show a definition along with a link underneath
    entry2 = DicEntry("行く", "いく")
    entry2.set_link_content(
        "行く means 'to go'.",
        "https://ja.wikipedia.org/wiki/行く"
    )

    dictionary.add_entry(entry2)

    # Method 3: Manually add html element to the definition content. This includes being able to add hrefs, styles and data
    entry3 = DicEntry("食べる", "たべる", tag="v5r")

    definition_element = create_html_element("ul", [
        create_html_element("li", "To ", [create_html_element("b", "eat"), "."])
    ])
    link_element = create_html_element("ul", [
        create_html_element("li", [create_html_element("a", "https://jisho.org/word/食べる", href="https://jisho.org/word/食べる")])
    ], style={"listStyleType": "\"⧉\""}, data={"wikipedia": "continue-reading"})

    entry3.add_element(definition_element) # <ul> <li>To <b>eat</b>.</li> </ul>
    entry3.add_element(link_element)       # <ul> <li> <a href="https://jisho.org/word/食べる">https://jisho.org/word/食べる</a> </li> </ul>

    dictionary.add_entry(entry3)

    dictionary.export() # Write all entries to word_bank.json files inside a folder with the name of the dictionary
    dictionary.zip() # Zip the folder