#!/usr/bin/env python

import os
import time
import argparse
import re

LINESIZE = 120

INF = 99999
file = None
parser = argparse.ArgumentParser(description="Code file stats")



def find_methods_lengths(file):
    print "Countint methods lengths..."
    lengths_of_methods = {}
    result = None
    inside = False
    name = None
    string_count = 0
    for i in file:
        #print i
        result = re.match(r'def', i)
        if result is None:
            result = re.match(r'class', i)
        #print result
        if (inside == True):
            string_count += 1
        if ((result is not None) and (inside == True)):
            lengths_of_methods[name] = string_count-3
            string_count = 0
            inside = False
        if ((result is not None) and (inside == False)):
            func_name = re.search('(?<=def )\w+\(.*\)', i)
            if (func_name is not None):
                name =  func_name.group(0)
            else:
                func_name = re.search('(?<=class )\w+\(.*\)', i)
            string_count = 0
            inside = True
        result2 = re.match(r'[a-z]|[A-Z]', i)
        if ((result2 is not None) and (result is None) and (inside == True)):
            lengths_of_methods[name] = string_count-3
            string_count = 0
            inside = False
    if name not in lengths_of_methods.keys():
        lengths_of_methods[name] = string_count
    return lengths_of_methods

def count_methods(file):
    print "Counting methods"
    methods_amount = 0
    result = True
    for i in file:
        result = re.match(r'def ', i)
        if (result is not None):
            methods_amount += 1
        else:
            result = re.match(r'class ', i)
            if(result is not None):
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
    lines = sum(1 for line in file)
    return lines


def count_chars_in_lines(file):
    print "Counting chars in lines"
    chars = []
    for i in file:
        chars.append(len(i))
    return chars

def count_spaces(string):
    count = 0
    for i in string:
        if (i != ' '):
            break
        else:
            count += 1
    return count


def count_loop_nesting(file):
    print "Counting nesting loops if any"
    level = 0
    begin = []
    end = []
    num_spaces = []
    num_str = -1
    file.seek(0)
    while True:
        x = file.readline()
        if not x: break
        num_str += 1
        result1 = re.search(r'    for', x)
        if (result1 is not None):
            begin.append(num_str)
        result2 = re.search(r'    while', x)
        if (result2 is not None):
            begin.append(num_str)
        #print num_str
    #print begin
    file.seek(0)
    num_str = -1
    while True:
        x = file.readline()
        if not x: break
        num_spaces.append(count_spaces(x))
    #print num_spaces
    file.seek(0)
    num_str = count_strings(file)
    file.seek(0)
    for i in begin:
        #print i
        for j in range(i+1, num_str):
            if (num_spaces[j] <= num_spaces[i]):
                #print j
                end.append(j)
                break
    end.sort()
    if not end:
        for i in begin:
            end.append(num_str)
    #print end
    nests = 0
    max_nests = 0
    end.append(INF)
    begin.append(INF)
    i = 0
    j = 0
    while ((begin[i] != 99999) and (end[j] != 99999)):
            #print begin[i]
            #print end[j]
            if begin[i] < end[j]:
                nests += 1
                if max_nests < nests:
                    max_nests = nests
                i += 1
            if begin[i] >= end[j]: 
                nests -= 1
                j += 1
    return max_nests


def main():
    parser.add_argument('filename', metavar='F', 
                                    help='Path to file you want to analyze')
    parser.add_argument('destination', metavar='dest',
                                    help='Path to results')
    args = parser.parse_args()
    ofile = fopen(args.filename)
    print args.filename
    res = open(args.destination, 'a+')
    #print "Counting lines..."
    strings_amount = count_strings(ofile)
    if (strings_amount != 0):
        print strings_amount
        res.write(str(strings_amount) + "\n")
    else:
        return 0
    ofile.seek(0)
    chars = count_chars_in_lines(ofile)
    count_lines = 0
    been = False
    for i in chars:
        count_lines += 1
        if (i > LINESIZE):
             #print "Too many chars in line {}: {} chars".format(count_lines, i)
             been = True
    if not been:
        res.write("0\n")
        #print "OK"
    if been:
        res.write("1\n")
    ofile.seek(0)
    methods_amount =  count_methods(ofile)
    max = 0
    if (methods_amount == 0):
        res.write("0\n")
        #print "No methods found"
    else:
        res.write(str(methods_amount) + "\n")
        print methods_amount
        ofile.seek(0)
        lengths = find_methods_lengths(ofile)
        #print lengths
        #print "List of methods with lengths:\n"
        for key, value in lengths.iteritems():
            if (value > max):
                max = value
            #print "{}: {}".format(key, value)
    print max
    res.write(str(max) + '\n')
    ofile.seek(0)
    max_nesting_loops = count_loop_nesting(ofile)
    print "Nesting loops amount: {}".format(max_nesting_loops)
    res.write(str(max_nesting_loops) + "\n")
    res.write('\n')
    ofile.close()
    res.close()
    #print fstring
    print "OK\n"

main()
