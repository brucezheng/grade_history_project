import subprocess
from os import listdir
from os.path import isfile, join

#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def convert(in_file):
    print("Converting " + in_file + "...")
    txt_file = in_file.replace('.pdf','.txt')
    cmd = "pdftotext.exe -table pdf/" + in_file + " txt/" + txt_file
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    #print(output)
    #file = open("txt/" + txt_name, "w")
    #file.write(output.replace('\n',' ').replace('\r',''))
    #file.close()
    print("Complete")

file_name = "grd20153EN.pdf"
convert(file_name)
