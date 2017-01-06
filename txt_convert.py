import os
import re

def convert(in_file):
    f = open("txt/" + in_file)
    input_string = f.read()
    
    file_pattern = "grd([0-9]{4})([0-9])([A-Z]{2}).txt"
    file_regex = re.match(file_pattern, in_file)
    if file_regex:
        year = file_regex.group(1)
        semester_num = file_regex.group(2)
        if semester_num == "1":
            semester = "Spring"
        elif semester_num == "2":
            semester = "Summer"
        elif semester_num == "3":
            semester = "Fall"
        else:
            semester = "Winter"

        pattern = "([A-Z]{4})-([A-Z0-9]+)-([0-9]{3})[ ]+" + "([0-9]+)[ ]+" * 6 + "[0-9]+\.[0-9]+[ ]+" + "[0-9]+[ ]+" * 6 + "(.*)"
        print(pattern)
        regex = re.compile(pattern)

        out = ""
        csv_format = ','.join(map(lambda x: "{" + str(x) + "}", range(12)))

        out += csv_format.format("Department", "Class", "Section", "Year", "Semester", "A", "B", "C", "D", "F", "Total", "Name") + '\n'

        num_rows = 0
        for m in regex.finditer(input_string):
            num_rows += 1
            out += csv_format.format(m.group(1), m.group(2), m.group(3), year, semester,
                                     m.group(4), m.group(5), m.group(6), m.group(7), m.group(8), m.group(9), re.sub("[ ]+"," ",m.group(10).strip())) + '\n'

        csv_name = in_file.replace(".txt",".csv")
        file = open("csv/" + csv_name, "w")
        file.write(out)
        file.close()
        print("Converted " + in_file + ", " + str(num_rows) + " rows processed")
    else:
        print("Could not convert " + in_file)

files = [f for f in os.listdir('./txt/') if re.match("grd[0-9]+[A-Z]+\.txt", str(f)) is not None]
for f in files:
    convert(str(f))
