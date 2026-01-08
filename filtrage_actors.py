import sys
import xml.etree.ElementTree as ET
from collections import Counter
import spacy
import csv


def iter_response_texts(xml_path):
    NS = {"tei": "http://www.tei-c.org/ns/1.0"}
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for p in root.findall(".//tei:div[@type='response']/tei:p", NS):
        if p.text:
            yield p.text


def main():
    if len(sys.argv) != 3:
        return 1

    xml_path = sys.argv[1]
    output_csv = sys.argv[2]

    nlp = spacy.load("fr_core_news_sm", disable=["parser", "ner"])

    nouns = Counter()
    propn = Counter()

    for doc in nlp.pipe(iter_response_texts(xml_path), batch_size=50):
        for tok in doc:
            if tok.is_punct or tok.is_space:
                continue

            if tok.pos_ == "NOUN":
                lemma = tok.lemma_.lower()
                if lemma.isalpha():
                    nouns[lemma] += 1

            elif tok.pos_ == "PROPN":
                propn[tok.text] += 1

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "form_or_lemma", "frequency"])

        # NOUN : seuil ≥ 20
        for lemma, freq in nouns.most_common():
            if freq >= 20:
                writer.writerow(["NOUN", lemma, freq])

        # PROPN : seuil ≥ 5
        for name, freq in propn.most_common():
            if freq >= 5:
                writer.writerow(["PROPN", name, freq])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())