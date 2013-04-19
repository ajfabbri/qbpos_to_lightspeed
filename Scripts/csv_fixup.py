#!/usr/bin/python
import sys
import csv
import afcsv

def usage() :
    print "Usage:\nTo clean up .csv files:\n\t%s clean <filename>" % sys.argv[0]
    print ("To clean up and merge customer data:\n\t%s cmerge <customer.csv> "\
        + "<customer-sales.csv>") % sys.argv[0]
    sys.exit()

afcsv.debug_print = False

def remove_dict_vals_newlines(d) :
    bad_chars = [(r'\n', "\n"), (r'\r',"\r"), (r'\t', "\t")]
    i = 0
    for k in d.keys() :
        #afcsv.dprint("key :'%s'" % k)
        if k == None :
            afcsv.dprint(("Removing None key from dictionary (i = %d)." % i))
            del d[k]

        i += 1
        if k == None:
            continue

        for (p, bad) in bad_chars :
            v = d[k]
            try:
                idx = v.find(bad)
            except :
                print "unexpected type " + str(v.__class__)
                print str(v)
                print "key " + str(k)
                sys.exit()
            if idx >= 0 :
                afcsv.dprint("Key %s had %s: %s" % (k, p, v))
                d[k] = v.replace(bad, " | ")
                afcsv.dprint("*** fixed: " + d[k])
    return d

def analyze_file(filename) :
    (fieldnames, dlist) = afcsv.csv_file_to_2d_list(filename)
    print "%s had %d rows" % (filename, len(dlist))
    #afcsv.dprint(" list 1: " + str(dlist))
    for d in dlist :
        remove_dict_vals_newlines(d)
    return (fieldnames, dlist)

def write_out(fieldnames, dlist, newfilename) :
    f = open(newfilename, "wb")
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    writer.writerows(dlist)

def caseify(s, nocase) :
    if nocase :
        return s.lower()
    else :
        return s

def all_keys_match(kv_tuple_list, d, nocase=False) :
    match = True
    for (k, v) in kv_tuple_list :
        if (not d.has_key(k)) or caseify(d[k], nocase) != caseify(v, nocase) :
            match = False
            break
    return match

# TODO move to afcsv.py
def dict_list_match(kv_tuple_list, dlist, nocase=False) :
    """ Given a list of (key, value) tuples, search the given list of
    dictionaries 'dlist' for the first element which matches ALL (key, value)
    pairs and return it. """
    result = None
    for d in dlist:
        if all_keys_match(kv_tuple_list, d, nocase) :
            result = d
            break
    return result

def merge_cust_spent(fieldnames, dlist, cust_spent) :
    k_lastname = "Last Name"
    k_firstname = "First Name"
    k_note = "Notes"
    k_spent = "Ext Price"
    matchkeys = [k_firstname, k_lastname]

    (s_fieldnames, s_dlist) = afcsv.csv_file_to_2d_list(cust_spent)
    afcsv.dprint("merge_cust_spend w/ filename " + cust_spent)

    # For each customer in main DB, find the corresponding name in customer's
    # total spent DB, and bring that value into the main DB by prepending to the
    # Note field.
    orphans = []
    case_wrongs = [ ] 
    for d in dlist :
        matchlist = [(k, d[k]) for k in matchkeys]
        spent_dict = dict_list_match(matchlist, s_dlist) 
        afcsv.dprint("matchlist '%s', spent_dict '%s'" % (matchlist, spent_dict))
        if spent_dict == None :
            spent_dict = dict_list_match(matchlist, s_dlist, True)
            if spent_dict == None:
                orphans.append(matchlist)
            else :
                case_wrongs.append(matchlist)

        if spent_dict != None:
            d[k_note] = ("QBPOS spent %s | " % spent_dict[k_spent]) + d[k_note]
            
    print ("** There were %d customers w/ no $ spent record." % len(orphans))
    afcsv.dprint(str(orphans))
    print ("** And %d customers w/ case mismatches." % len(case_wrongs))
    afcsv.dprint(str(case_wrongs))

def main() :
    args = len(sys.argv)
    if args < 3 or args > 4:
        usage()
    else :
        cmd = sys.argv[1]
        if args == 3 and cmd != "clean" :
            usage()
        elif args == 4 and cmd != "cmerge" :
            usage()
        elif cmd == "clean" :
            filename = sys.argv[2]
            (fieldnames, dlist) = analyze_file(filename) 
            write_out(fieldnames, dlist, "rewritten_" + filename )
        elif cmd == "cmerge" :
            cust_file = sys.argv[2]
            cust_spent = sys.argv[3]
            # first, clean up main customer csv
            (fieldnames, dlist) = analyze_file(cust_file)
            merge_cust_spent(fieldnames, dlist, cust_spent)
            write_out(fieldnames, dlist, "rewritten_" + cust_file)

if __name__ == "__main__" :
	main()

# vim: ai ts=4 sts=4 et sw=4 syntax=python:
