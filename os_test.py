import os
import re

pdf_pattern = "grd[0-9]+([A-Z]+)\.pdf"

files = [f for f in os.listdir('./pdf/')]
en_files = []
for f in files:
    #print(str(f))
    m = re.match(pdf_pattern,str(f))
    if m is not None and m.group(1) == "EN":
        en_files.append(str(f))

for f in en_files:
    in_path = "pdf/" + f
    out_path = "test/" + f
    reader = open(in_path, 'rb')
    text = reader.read()
    reader.close()
    writer = open(out_path, 'wb')
    writer.write(text)
    writer.close()
