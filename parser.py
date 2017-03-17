#!/usr/bin/env python

import os
import time
import argparse
import re

file = None
parser = argparse.ArgumentParser(description="Code file stats")

def find_methods_lengths(file):
    print "Countint methods lengths...\n"
    lengths_of_methods = {}
    result = None
    inside = False
    name = None
    string_count = 0
    for i in file:
        #print i
        result = re.match(r'def', i)
        #print result
        if (inside == True):
            string_count += 1
        if ((result is not None) and (inside == True)):
            lengths_of_methods[name] = string_count-3
            string_count = 0
            inside = False
        if ((result is not None) and (inside == False)):
            func_name = re.search('(?<=def )\w+\(.*\)', i)
            name =  func_name.group(0)
            string_count = 0
            inside = True
        result2 = re.match(r'[a-z]|[A-Z]', i)
        if ((result2 is not None) and (result is None) and (inside == True)):
            lengths_of_methods[name] = string_count-3
            string_count = 0
            inside = False
    if name not in lengths_of_methods.keys():
        lengths_of_methods[name] = string_count-3
    return lengths_of_methods

def count_methods(file):
    print "Counting methods...\n"
    methods_amount = 0
    result = True
    for i in file:
        result = re.match(r'def ', i)
        if (result is not None):
            methods_amount += 1
    return methods_amount

def fopen(filename):
    print "Open file."
    if os.path.isfile(filename):
        file = open(filename, 'r')
    else:
        parser.error("The file %s doesn't exist!" % filename)
    return file

def count_strings(file):
    print "Counting lines..."
    lines = sum(1 for line in file)
    return lines


def count_chars_in_lines(file):
    print "Counting chars in lines..."
    chars = []
    for i in file:
        chars.append(len(i))
    return chars

LINESIZE = 80

def count_loop_nesting(file):
    print "Counting nesting loops if any..."
    return 0

def main():
    parser.add_argument('filename', metavar='F', help='Path to file you want to analyze')
    args = parser.parse_args()
    ofile = fopen(args.filename)
    strings_amount = count_strings(ofile)
    if (strings_amount != 0):
        print strings_amount
        ofile.seek(0)
    else:
        print "File is empty"
        return 0
    chars = count_chars_in_lines(ofile)
    count_lines = 0
    for i in chars:
        count_lines += 1
        if (i > LINESIZE):
             print "Too many chars in line {}: {} chars".format(count_lines, i)
    ofile.seek(0)
    methods_amount =  count_methods(ofile)
    if (methods_amount == 0):
        print "No methods found"
    else:
        print methods_amount
        ofile.seek(0)
        lengths = find_methods_lengths(ofile)
        #print lengths
        print "List of methods with lengths:\n"
        for key, value in lengths.iteritems():
            print "{}: {}".format(key, value)
    #print count_methods(fstring)
    #print fstring

main()