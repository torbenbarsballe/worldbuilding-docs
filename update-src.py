import os
import subprocess

header = ""
header += "---\n"
header += "layout: default\n"
header += "---\n"

def proc_file(f):
  if (f.endswith(".md")):
    subprocess.Popen("git checkout master "+f, shell=True)
    fin = file(f, 'r')
    data = fin.read()
    fin.close()
    fout = file(f, 'w')
    fout.write(header + "\n" + data)
    fout.close()

def proc_folder(filelist, folder):
  for file in filelist:
    filepath = folder + "/" + file
    if (file.startswith(".")):
      print("Skipping "+filepath)
    elif os.path.isfile(filepath):
      print("Processing file: "+filepath)
      proc_file(filepath)
    elif os.path.isdir(filepath):
      print("Processing folder: "+filepath)
      proc_folder(os.listdir(filepath), filepath)
    else:
      print("File: "+filepath+" does not exist")

print("Updating source files from master")
subprocess.Popen("git stash", shell=True)
subprocess.Popen("git checkout master", shell=True)

rootFiles = os.listdir("./")

subprocess.Popen("git checkout gh-pages", shell=True)
subprocess.Popen("git stash apply", shell=True)

proc_folder(rootFiles, ".")

