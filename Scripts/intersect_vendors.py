#!/usr/bin/python
from afcsv import *
import csv

#
# When importing vendors from Quickbooks POS (QBPOS), you run into 
# a problem:  The QBPOS vendor export contains *every* vendor 
# you've ever paid with Quickbooks Financial.  This is because
# QBPOS does a 2-way sync with QB Financial (pulling it its 
# vendors.
# To clean up this huge list of vendors, you want to reduce it
# to the vendors you actually use to buy stock from for your
# store.  To accomplish this, do a report of sales (or purchases)
# by vendor in QBPOS, and export that to a .csv file.  This .csv
# file (qb_vendor_totals.csv) will only contain those vendors you
# actually bought stock from.  
# Also do a standard export of all vendors from QBPOS and save as
# VendorsExport.csv.
# Make sure the files are cleaned up (contain only header and data
# columns and rows.
# Next, run this script on the two files and it will create
# new_vendor_file.csv, which contains only the vendors you
# care about.  You can then use that file to import into 
# LightSpeed.
#
# Author: Aaron Fabbri 2013
#
file1 = "qb_vendor_totals.csv"
file2 =  "VendorsExport.csv"

(dummy, list1) = csv_file_to_2d_list(file1)
print "%s had %d rows" % (file1, len(list1))
dprint(" list 1: " + str(list1))

(fieldnames, list_all) = csv_file_to_2d_list(file2)
print "%s had %d rows" % (file2, len(list_all))
wanted_names = map((lambda l : l["Vendor"]), list1)
dprint("Wanted names: " + str(wanted_names))
new_list = []
for r in list_all :
	index = list_find(wanted_names, r["Company"])
	if index != -1 :
		new_list.append(r)
	else:
		print "No match for " + str(r["Company"])

f = open("new_vendor_file.csv", "wb")
writer = csv.DictWriter(f, fieldnames)
writer.writeheader()
writer.writerows(new_list)

# vim: ai ts=4 sts=4 et sw=4 syntax=python:
