#!/usr/bin/env python3

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom


def is_list_line(line: str) -> bool:
    s = line.lstrip()
    return s.startswith(("- ", "– ", "— ", "• ", "● ", "* "))


def read_responses(path: Path):
    raw = (
        path.read_text(encoding="utf-8")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .lstrip("\ufeff")
    )
    lines = [l.strip() for l in raw.split("\n") if l.strip()]

    responses = []
    current_list = []

    for line in lines:
        if is_list_line(line):
            current_list.append(line)
        else:
            if current_list:
                responses.append("\n".join(current_list))
                current_list = []
            responses.append(line)

    if current_list:
        responses.append("\n".join(current_list))

    return responses


def build_tei(responses, title: str):
    tei = ET.Element("TEI")

    teiHeader = ET.SubElement(tei, "teiHeader")
    fileDesc = ET.SubElement(teiHeader, "fileDesc")

    titleStmt = ET.SubElement(fileDesc, "titleStmt")
    ET.SubElement(titleStmt, "title").text = title

    publicationStmt = ET.SubElement(fileDesc, "publicationStmt")
    ET.SubElement(publicationStmt, "p").text = (
        "Corpus généré automatiquement pour analyse dans TXM."
    )

    sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
    ET.SubElement(sourceDesc, "p").text = (
        "Contributions citoyennes (avec regroupement des listes)."
    )

    text_root = ET.SubElement(tei, "text", {"xml:id": "corpus"})
    body = ET.SubElement(text_root, "body")

    for i, resp in enumerate(responses, start=1):
        div = ET.SubElement(
            body,
            "div",
            {
                "type": "response",
                "xml:id": f"resp{i:05d}",
                "n": str(i),
                "words": str(len(resp.split())),
            },
        )
        p = ET.SubElement(div, "p")
        p.text = resp

    return tei


def pretty_xml(element: ET.Element) -> bytes:
    rough = ET.tostring(element, encoding="utf-8")
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent="  ", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Convertir un corpus texte en TEI-XML pour TXM."
    )
    parser.add_argument("input", help="Fichier texte d'entrée (UTF-8)")
    parser.add_argument("output", help="Fichier XML TEI de sortie")
    parser.add_argument(
        "--title", default="Corpus sur l’écologie", help="Titre du corpus"
    )
    args = parser.parse_args()

    responses = read_responses(Path(args.input))
    xml_bytes = pretty_xml(build_tei(responses, title=args.title))
    Path(args.output).write_bytes(xml_bytes)


if __name__ == "__main__":
    main()