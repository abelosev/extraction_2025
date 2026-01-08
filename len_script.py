import sys
import xml.etree.ElementTree as ET
import statistics

if len(sys.argv) != 2:
    sys.exit(1)

FILE = sys.argv[1]

NS = {"tei": "http://www.tei-c.org/ns/1.0"}

tree = ET.parse(FILE)
root = tree.getroot()

lengths = []

for div in root.findall(".//tei:div[@type='response']", NS):
    words = div.get("words")
    if words is not None:
        lengths.append(int(words))

min_len = min(lengths)
max_len = max(lengths)
mean_len = round(statistics.mean(lengths), 2)

print(f"Nombre de réponses : {len(lengths)}")
print(f"Longueur minimale : {min_len}")
print(f"Longueur maximale : {max_len}")
print(f"Longueur moyenne  : {mean_len}")