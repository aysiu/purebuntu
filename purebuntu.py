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

def getdependencies(metapackage):
   cmd="apt-cache showpkg " + metapackage + " | grep -A2 \"Dependencies\" | awk -F \" - \" '{print $2}' | awk -F \":i386\" '{print $1}'"
   dependencies=subprocess.check_output(cmd, shell=True)
   dependencylist=dependencies.split(" (0 (null)) ")
   dependencylist.sort()
   return dependencylist

# Checks for each of the items to potentially remove. If they're not in what to keep, plop them into a list of items to actually remove.
def getitemstoremove(metapackagetoremove, metapackagetokeep):
   itemstoremove=[]
   for itemtoconsider in metapackagetoremove:
      if itemtoconsider not in metapackagetokeep:
         # For some reason, a couple of items have one or two instances of a preceding carriage return, so let's get rid of that
         itemstoremove.append(itemtoconsider.replace("\n",""))
   return itemstoremove

def main():
   parser=argparse.ArgumentParser(description='To use this, run python purebuntu.py --remove NAMEOFMETAPACKAGETOREMOVE --keep NAMEOFMETAPACKAGETOKEEP')
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

if __name__ == '__main__':
   main()
