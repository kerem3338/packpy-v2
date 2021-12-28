import os
import sys
import re
import json
import shutil
import requests
import xml.etree.ElementTree as et

class PackPy:
  def __init__(self, file, dir=os.getcwd()):
    if os.path.isdir(dir):
      self.dir=dir
      self.url_file=None
    else:
      print(f"Dir {dir} is not dir or dir not exits")
    if file in os.listdir():
      self.file=file
      self.xml=et.fromstring(open(file,"r",
      encoding="utf8").read())
    else:
      print(f"File {file} not found in {dir}")
    
    self.config={}
    
    self.execute()

  def execute(self):
    if self.xml.tag == "packpy":
      pass
    else:
      print(f"file {self.file} Not Package file")
    for elem in self.xml.iter():
      if elem.tag == "packpy":
        pass
      elif elem.tag == "author":
        self.config["author"] = elem.text
      elif elem.tag == "progname":
        self.config["progname"]=elem.text
      elif elem.tag == "publisher":
        self.config["publisher"]=elem.text
      elif elem.tag == "installdir":
        if os.path.isdir(elem.text):
          self.config["installdir"]=elem.text
        else:
          print(f"Dir '{elem.text}' Not Exits or Not a Dir")
          sys.exit()
      elif elem.tag == "file":
        if "url" in elem.attrib:
          self.url_file=elem.attrib["url"]
          self.config["file"]=elem.attrib["url"]
        else:
          if os.path.isfile(elem.text):
            self.config["file"]=elem.text
          else:
            print(f"Dir '{elem.text}' Not Exits or Not a Dir")
      else:
        print(f"PackpyError: {elem} not found")
  def install(self):
    #Show program information
    print(f"""Packpy Package Installion

Package Name: {self.config["progname"]}
Publisher: {self.config["publisher"]}
Author: {self.config["author"]}
file: {self.config["file"]}
installion location: {self.config["installdir"]}
""")
    check=input(f"İnstall This Program? (y/n):")
    if check == "y":
      print("installion Started")
      try:
        os.mkdir(self.dir+f"//{self.config['progname']}")
      except FileExistsError:
        print(self.dir+f"//{self.config['progname']} already exits")
      if self.url_file is None:
        shutil.copy(self.config["file"], self.dir+"f//{self.config['progname']}")
      else:
        code=requests.get(self.url_file,allow_redirects=True)
        filename=self.config["progname"].replace(" ", "-")
        with open(self.dir+f"//{self.config['progname']}//{filename}","w",encoding="utf8") as file:
          file.write(code.text)
    else:
      sys.exit()
  

a=PackPy("install.pack")
a.install()