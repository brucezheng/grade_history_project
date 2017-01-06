import urllib2

urlpref = "http://web-as.tamu.edu/gradereport/PDFReports/"
depts = ["AG", "AR", "BA", "DN", "ED", "EL", "EN", "GB", "GE", "GV", "LA", "MD", "MS", "NU", "CP", "PH", "SC", "SL", "VM"]

not_found = []

def download_file(url,file_name):
    try: 
        response = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        if e.code == 404:
            not_found.append(file_name)
            print("File not found")
    else:
        file = open("pdf/" + file_name, 'wb')
        file.write(response.read())
        file.close()
        print("Complete")

for year in range(2012,2016):
    for sem in range(1,4):
        yearsem = str(year) + str(sem)
        for dept in depts:
            file_name = "grd" + yearsem + dept + ".pdf"
            url = urlpref + yearsem + "/" + file_name
            print("Downloading " + file_name)
            download_file(url,file_name)

not_found_str = "Not found: "
for file_name in not_found:
    not_found_str += file_name + " "
print(not_found_str)
