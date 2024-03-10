# YomitanDic

YomitanDic is a Python library that makes it easy to create dictionary files importable into Yomitan for Japanese popup dictionaries. With YomitanDic, you can quickly create dictionary entries with definitions, links, and custom HTML elements.

## Installation

To install YomitanDic, use pip:

```
pip install yomitandic
```

## Usage

Here's how you can use YomitanDic to create dictionary entries:

### Creating a Dictionary

First, create a `Dictionary` object to hold your entries:

```python
from yomitandic import DicEntry, Dictionary, create_html_element

dictionary = Dictionary("Example_Dictionary")
```

### Adding Entries

There are three ways to add entries to a dictionary:

#### Method 1: Simple Definition

Self explanatory.

```python
entry = DicEntry("踊る", "おどる", definition="To dance", tag="v5r")
dictionary.add_entry(entry)
```

#### Method 2: Definition with Link

`set_link_content()` is a method that allows you to easily add text and a link to an entry without having to know html.

```python
entry = DicEntry("行く", "いく", tag="v5k-s")
entry.set_link_content(
    "行く means 'to go'.", # definition
    "https://ja.wikipedia.org/wiki/行く" # link that goes underneath
)
dictionary.add_entry(entry)
```

#### Method 3: Custom HTML Elements

For more control over the entry's content, you can manually add HTML elements using the `create_html_element()` function:

```python
dictionary = Dictionary("Example_Dictionary")

entry = DicEntry("食べる", "たべる", tag="v5r")

definition_element = create_html_element("ul", [ # A bullet point list containing one bullet point with text "To eat"
    create_html_element("li", "To eat")
])
link_element = create_html_element("ul", [ # A bullet point list containing one bullet point with hyperlink text "View on Jisho"
    create_html_element("li", [
        create_html_element("a", "View on Jisho", href="https://jisho.org/word/食べる")
    ])
], style={"listStyleType": "\"⧉\""})

entry.add_element(definition_element)
entry.add_element(link_element)

dictionary.add_entry(entry)
```

### Exporting and Zipping

After you've added all the entries to your dictionary, you can export it to json and zip into a folder:

```python
dictionary.export()  # Write all entries to word_bank.json files inside a folder with the name of the dictionary
dictionary.zip()     # Zip the folder
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an [issue](https://github.com/hopto-dot/yomitan-dic/issues) or submit a [pull request](https://github.com/hopto-dot/yomitan-dic/pulls).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
