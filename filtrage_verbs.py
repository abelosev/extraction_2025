import sys
import spacy
import xml.etree.ElementTree as ET
import csv
from collections import Counter

def main():
    if len(sys.argv) != 3:
        return 1

    XML_FILE = sys.argv[1]
    OUTPUT_CSV = sys.argv[2]
    LANG_MODEL = "fr_core_news_md"

    nlp = spacy.load(LANG_MODEL, disable=["ner", "parser"])

    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    verb_counter = Counter()

    for elem in root.iter():
        if elem.text:
            doc = nlp(elem.text)
            for token in doc:
                if token.pos_ == "VERB":
                    lemma = token.lemma_.lower()
                    if lemma.isalpha():
                        verb_counter[lemma] += 1

    with open(OUTPUT_CSV, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["lemma", "frequency"])
        for lemma, freq in verb_counter.most_common():
            writer.writerow([lemma, freq])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())