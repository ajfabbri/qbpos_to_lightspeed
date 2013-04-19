# convenience wrappers around python csv stuff
# Author: Aaron Fabbri 2013
import csv

debug_print = False

def dprint(s) :
	if debug_print :
		print s

# Return (fieldnames, 2d_list)
# 2d_list is now a list of dicts
def csv_file_to_2d_list(filename) :
    f1 = open(filename, 'rb')
    sample = f1.read(1024)
    f1.seek(0)
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(sample)
    has_header = sniffer.has_header(sample)
    dprint ("Detected .csv type " + str(dialect))
#reader = csv.reader(f1, dialect)
    reader = csv.DictReader(f1, fieldnames=None, restkey=None, restval=None,  dialect=dialect)

    output = []
    for row in reader :
        output.append(row)
    #dprint("Fieldnames: " + str(reader.fieldnames))
    #dprint("\n\n")
    #dprint(str(output[0:2]))
    #dprint("\n\n")
    return (reader.fieldnames, output)

# list.index uses exceptions for not found, meh
def list_find(l, val) :
	i = -1
	try :
		i = l.index(val)
	except :
		pass
	return i

# vim: ai ts=4 sts=4 et sw=4 syntax=python:
