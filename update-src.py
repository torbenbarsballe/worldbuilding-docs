import os
import subprocess

header = "layout: default\n"

def proc_file(f):
  if (f.endswith(".md")):
    permalink = f[1:]
    if (f.endswith("index.md")):
      permalink = permalink[:-8]
    else:
      permalink = permalink[:-3]

    sp = subprocess.Popen("git checkout master "+f, shell=True)
    sp.wait()
    fin = file(f, 'r')
    data = fin.read()
    fin.close()
    fout = file(f, 'w')
    fout.write("---\n"+header+"permalink: "+permalink+"\n"+"---\n"+"\n"+data)
    fout.close()
      
def find_files(folder):
  contents = os.listdir(folder)
  files = []
  for file in contents:
    filepath = folder + "/" + file
    if (file.startswith(".")):
      print("Skipping "+filepath)
    elif os.path.isfile(filepath):
      print("Processing file: "+filepath)
      files.append(filepath)
    elif os.path.isdir(filepath):
      print("Processing folder: "+filepath)
      files.extend(find_files(filepath))
    else:
      print("File: "+filepath+" does not exist")
  return files
  
print("Updating source files from master")
sp = subprocess.Popen("git stash", shell=True)
sp.wait()
sp = subprocess.Popen("git checkout master", shell=True)
sp.wait()
sp = subprocess.Popen("git pull origin master", shell=True)
sp.wait()

files = find_files('.')

sp = subprocess.Popen("git checkout gh-pages", shell=True)
sp.wait()
sp = subprocess.Popen("git stash apply", shell=True)
sp.wait()

for file in files:
  proc_file(file)
