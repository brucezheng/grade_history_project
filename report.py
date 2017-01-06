import csv
import os
import re

grades = list("ABCDF")

def calc_gpr(v):
    return (v['A']*4.0 + v['B']*3.0 + v['C']*2.0 + v['D'])/ v['Total']

def cast_int(row):
    row['A'] = int(row['A'])
    row['B'] = int(row['B'])
    row['C'] = int(row['C'])
    row['D'] = int(row['D'])
    row['F'] = int(row['F'])
    row['Total'] = int(row['Total'])
    return row

dept = set()
data = []
csv_files = [f for f in os.listdir('./csv/') if re.match("grd[0-9]+[A-Z]+\.csv", str(f)) is not None]
for f in csv_files:
    file = open('csv/' + str(f))
    reader = csv.DictReader(file)
    for row in reader:
        cast_row = cast_int(row)
        dept.add(cast_row["Department"])
        data.append(cast_row)

#print(sorted(list(dept)))

sort_gpr = True

def subquery(cols, vals):
    result = []
    for row in data:
        match = True
        for i in range(len(cols)):
            if row[cols[i]] != vals[i]:
                match = False
                break
        if match:
            result.append(row)
    return result

def subquery_class(dept, class_no):
    return subquery(("Department", "Class"), (dept, class_no))

#def subquery_class(dept, class_no):
#    result = []
#    for row in data:
#        if row["Department"] == dept and row["Class"] == class_no:
#            result.append(row)
#    return result
        
def subquery_prof(name):
    result = []
    for row in data:
        if row["Name"] == name:
            result.append(row)
    return result

grd_fields = ('A','B','C','D','F','Total')

def retrieve(cols, vals, key):
    query = ' '.join(vals)
    print("## %s ##\n" % (query))
    red_data = {}
    for row in subquery(cols,vals):
        key_val = ' '.join(map(lambda x : row[x], key))
        if key_val in red_data:
            for x in grd_fields:
                red_data[key_val][x] += row[x]
        else:
            new_entry = {}
            for x in grd_fields:
                new_entry[x] = row[x]
            red_data[key_val] = new_entry
    output = []
    for k, v in red_data.iteritems():
        v['GPR'] = calc_gpr(v)
        grade_dist = "/".join(map(lambda x : "%02d%%" % (round(float(100)*v[x]/v['Total'])), grades))
        if v['A'] != v['Total']:
            grade_dist = " " + grade_dist
        row_out = "%20s: %s GPR: %.2f Num: %d" % (k, grade_dist, v['GPR'], v['Total'])
        output.append(row_out)
    if sort_gpr:
        output = sorted(output, key = lambda x : float(re.search("GPR: ([0-9]+)", x).group(1)), reverse = True)
    else:
        output = sorted(output, key = lambda x : int(re.search("Num: ([0-9]+)", x).group(1)), reverse = True)
    for entry in output:
        print(entry)
    print('')
    
def retrieve_prof(name):
    retrieve(("Name",),(name,),("Department", "Class"))

def retrieve_class(dept, class_no):
    retrieve(("Department", "Class"),(dept,class_no),("Name",))

'''
def retrieve_prof(name):
    print("## %s ##\n" % (name))
    class_data = {}
    for row in subquery_prof(name):
        key = (row['Department'], row['Class'])
        if (row['Department'], row['Class']) in class_data:
            class_data[key]['A'] += row['A']
            class_data[key]['B'] += row['B']
            class_data[key]['C'] += row['C']
            class_data[key]['D'] += row['D']
            class_data[key]['F'] += row['F']
            class_data[key]['Total'] += row['Total']
        else:
            entry = {}
            entry['A'] = row['A']
            entry['B'] = row['B']
            entry['C'] = row['C']
            entry['D'] = row['D']
            entry['F'] = row['F']
            entry['Total'] = row['Total']
            class_data[key] = entry
    output = []
    for key, value in class_data.iteritems():
        value['GPR'] = calc_gpr(value)
        grade_dist = "/".join(map(lambda x : "%02d%%" % (round(float(100)*value[x]/value['Total'])), grades))
        if value['A'] != value['Total']:
            grade_dist = " " + grade_dist
        row_out = "%11s %s: %s GPR: %.2f Num: %d" % (key[0], key[1] , grade_dist, value['GPR'], value['Total'])
        output.append(row_out)
    if sort_gpr:
        output = sorted(output, key = lambda x : float(re.search("GPR: ([0-9]+)", x).group(1)), reverse = True)
    else:
        output = sorted(output, key = lambda x : int(re.search("Num: ([0-9]+)", x).group(1)), reverse = True)
    for entry in output:
        print(entry)
    print('')
    
def retrieve_class(dept, class_no):
    print("## %s %s ##\n" % (dept, class_no))
    prof_data = {}
    for row in subquery_class(dept, class_no):
        if row['Name'] in prof_data:
            prof_data[row['Name']]['A'] += row['A']
            prof_data[row['Name']]['B'] += row['B']
            prof_data[row['Name']]['C'] += row['C']
            prof_data[row['Name']]['D'] += row['D']
            prof_data[row['Name']]['F'] += row['F']
            prof_data[row['Name']]['Total'] += row['Total']
        else:
            entry = {}
            entry['A'] = row['A']
            entry['B'] = row['B']
            entry['C'] = row['C']
            entry['D'] = row['D']
            entry['F'] = row['F']
            entry['Total'] = row['Total']
            prof_data[row['Name']] = entry
    output = []
    for key, value in prof_data.iteritems():
        value['GPR'] = calc_gpr(value)
        grade_dist = "/".join(map(lambda x : "%02d%%" % (round(float(100)*value[x]/value['Total'])), grades))
        if value['A'] != value['Total']:
            grade_dist = " " + grade_dist
        row_out = "%15s: %s GPR: %.2f Num: %d" % (key, grade_dist, value['GPR'], value['Total'])
        output.append(row_out)
    if sort_gpr:
        output = sorted(output, key = lambda x : float(re.search("GPR: ([0-9]+)", x).group(1)), reverse = True)
    else:
        output = sorted(output, key = lambda x : int(re.search("Num: ([0-9]+)", x).group(1)), reverse = True)
    for entry in output:
        print(entry)
    if len(output) == 0:
        print("\tNo output found for query") 
    print('')
'''

while(True):
    cmd = raw_input(": ")
    cmd = cmd.upper()
    if cmd == "QUIT" or cmd == "Q":
        print("Quitting...")
        break
    m_sort = re.match("sort (GPR|NUM|NUMBER)", cmd, re.IGNORECASE)
    m_class = re.match("([A-Z0-9]+) ([0-9]{3})", cmd)
    if m_sort is not None:
        if m_sort.group(1) == "GPR":
            print('Sorting by GPR')
            sort_gpr = True
        else:
            print('Sorting by Number of Students')
            sort_gpr = False
    elif m_class is not None:
        retrieve_class(m_class.group(1), m_class.group(2))
    else:
        retrieve_prof(cmd)
    
