#!/usr/bin/python

### This program is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program.If not, see http://www.gnu.org/licenses/

### Originally developed by aysiu, 2016

# Workaround to print items without line breaks in Python 2
from __future__ import print_function
import argparse
import os
# To run bash commands from Python
import subprocess

# Lines come back with a Recommends: or Depends: potentially at the beginning of the line and parentheses with some notes potentially at the end of the line
def cleanline(dirtyline):
   if ":" in dirtyline:
      temparray1=dirtyline.split(":", 1)
      tempstring1=temparray1[1]
   else:
      tempstring1=dirtyline
   if "(" in tempstring1:
      temparray2=tempstring1.split("(", 1)
      tempstring2=temparray2[0]
   else:
      tempstring2=tempstring1
   # There may be extra white space as well, so get rid of all that... package names are usually one word (or several words separated by hyphens)
   cleanedline=tempstring2.replace(" ", "")
   return cleanedline

# I've looked into using apt-cache depends NAMEOFMETAPACKAGE --recurse, but it brings back a whole mess of packages, and it just doesn't work for the logic we're using here, which is basically: list all the recursive dependencies of both metapackages, and then find the difference between the two.
def getdependencies(metapackage):
   cmd="apt-rdepends --follow=Recommends " + metapackage
   dependencies=subprocess.check_output(cmd, shell=True)
   dependencylistdirty=dependencies.split("\n")
   dependencylist=[]
   for dependency in dependencylistdirty:
      if cleanline(dependency) not in dependencylist and cleanline(dependency)!='':
         dependencylist.append(cleanline(dependency))
   dependencylist.sort()
   return dependencylist

# Checks for each of the items to potentially remove. If they're not in what to keep, plop them into a list of items to actually remove.
def getitemstoremove(metapackagetoremove, metapackagetokeep):
   itemstoremove=[]
   for itemtoconsider in metapackagetoremove:
      if itemtoconsider not in metapackagetokeep:
         itemstoremove.append(itemtoconsider)
   return itemstoremove

def main():
   # Make sure apt-rdepends is installed (it's not by default in Ubuntu)
   rdepends='/usr/bin/apt-rdepends'
   if(os.path.isfile(rdepends)):
      parser=argparse.ArgumentParser(description='Requires the apt-rdepends package, which more reliably and cleanly displays the recursive dependencies of a metapackage than apt-cache depends does. To use this, run python purebuntu.py --remove NAMEOFMETAPACKAGETOREMOVE --keep NAMEOFMETAPACKAGETOKEEP')
      parser.add_argument('--remove', required=True, help='REMOVE is the name of metapackage to remove')
      parser.add_argument('--keep', required=True, help='KEEP is the name of metapackage to keep') 
      args=parser.parse_args()
      if(args.remove) and (args.keep):
         removalmetapackage=args.remove
         keptmetapackage=args.keep         
         removalitems=getitemstoremove(getdependencies(removalmetapackage), getdependencies(keptmetapackage))
         print("\nsudo apt-get remove", end=" ")
         for removalitem in removalitems:
            print(removalitem, end=" ")
         print("&& sudo apt-get install %s" % keptmetapackage, end="\n")
      else:
         print("You need to specify a metapackage to --keep and a metapackage to --remove. Run pureubuntu.py -h for more details.", end="\n")
   else:
      # If apt-rdepends isn't installed, let the user know how to install it.
      print ("Please run\n\nsudo apt-get install apt-rdepends\n\nbefore proceeding", end="\n")

if __name__ == '__main__':
    main()
