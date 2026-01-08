#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
import spacy


def clean_with_spacy(text: str, doc) -> str:
    tokens = [
        t.text.lower()
        for t in doc
        if not t.is_stop and not t.is_punct and not t.is_space
    ]
    return " ".join(tokens)


def main() -> int:
    if len(sys.argv) != 3:
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    NS = {"tei": "http://www.tei-c.org/ns/1.0"}
    ET.register_namespace("", NS["tei"])

    nlp = spacy.load("fr_core_news_sm", disable=["parser", "ner", "tagger"])

    tree = ET.parse(input_file)
    root = tree.getroot()

    ps = root.findall(".//tei:div[@type='response']/tei:p", NS)
    total = len(ps)
    print(f"Nombre de réponses à traiter : {total}")

    texts = [(p.text or "") for p in ps]

    batch_size = 50

    for i, doc in enumerate(nlp.pipe(texts, batch_size=batch_size), start=1):
        ps[i - 1].text = clean_with_spacy(texts[i - 1], doc)

        if i % 1000 == 0:
            print(f"{i}/{total} réponses traitées")

    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
