#!/usr/bin/env python3

import argparse
import sys
import os
import time
import collections
import operator


def parse_my_arg (args):
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="show this help message and exit" ,nargs='?', default='.')
                        
    parser.add_argument("-H" ,"--hidden",help=" show hidden files [default: off]",
                       action = "store_true")
    parser.add_argument("-s","--sizes", help=" show sizes [default: off]" , action = "store_true")
    parser.add_argument("-o","--ordered", help="order by ('name', 'n', 'modified', 'm', 'size', 's')",
                       default= 'name',choices=['name','modified','size','s','m','n'],nargs='?')
    parser.add_argument("-r","--recursive", help="recurse into subdirectories [default: off]" , action = "store_true")
    parser.add_argument("-m","--modified", help=" show last modified date/time [default: off]", action = "store_true")
    return parser.parse_args(args)


def main():
    args = parse_my_arg(sys.argv[1:])
    items = os.listdir(args.directory)
    result = []
    stack=[]
    if args.recursive:
        aroot = args.directory
        result = my_tree(aroot,args,stack,result)
    else:
        for item in items:
            lis = collections.defaultdict(str)
            fullitem = os.path.join(args.directory,item)
            if args.hidden:
                if os.path.isdir(fullitem):
                    lis['name'] = item + '/'
                else:
                    lis['name'] = item
            else:
                if not item.startswith('.'):
                    if os.path.isdir(fullitem):
                        lis['name'] = item+'/'
                    else:
                        lis['name'] = item
            if args.sizes or args.ordered=='size' or args.ordered=='s':
                lis['size'] = os.path.getsize(fullitem)    
            if args.modified or args.ordered=='modified' or args.ordered=='m' :
                lis['modified'] = os.path.getmtime(fullitem)
            result.append(lis)
    print_result(result,args)

   
def my_tree(aroot,args,stack,result):
    while True:
        items = os.listdir(aroot)
        for item in items:   
            lis = collections.defaultdict(str)
            fullitem = os.path.join(aroot,item)
            if os.path.isdir(fullitem):
                if not item.startswith('.') or args.hidden:
                    stack.append(fullitem)
            else:
                if args.hidden:               
                    lis['name'] =aroot + "/" + item
                else:
                    if not item.startswith('.'):
                        lis['name'] = aroot +"/" + item
                if args.sizes or args.ordered=='size' or args.ordered=='s':
                    lis['size'] = os.path.getsize(fullitem)    
                if args.modified or args.ordered=='modified' or args.ordered=='m' :
                    lis['modified'] = os.path.getmtime(fullitem)
                result.append(lis)

        if len(stack)<1:
            return result  
        else:
            aroot = stack.pop()    
            
def print_result(result,args):
    if args.ordered=='name' or args.ordered=='n':
       result.sort(key=operator.itemgetter('name'))
       
    if args.ordered=='size' or args.ordered=='s':
        result.sort(key=operator.itemgetter('size'))   

    if args.ordered=='modified' or args.ordered=='m':
        result.sort(key=operator.itemgetter('modified'))
    number = 0  
    for dic in result:
        dic['name'] = dic['name'].lstrip("./")
        if dic['name'] != "":   
            strh = ""
            if args.modified:
                dic['modified'] = time.ctime(dic['modified'])
                strh += "{modified:^25}"
            if args.sizes:
                strh += "{size:^10}"
            strh += "{name:>}"
            print(strh.format(**dic))
            number += 1
    print(number, "files")   

main()
