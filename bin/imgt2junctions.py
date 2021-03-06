#! /usr/bin/env python
# Copyright 2014 Uri Laserson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import argparse

import vdj

argparser = argparse.ArgumentParser(description=None)
argparser.add_argument('positional',nargs='+')
args = argparser.parse_args()

if len(args.positional) == 2:
    inhandle = open(args.positional[0],'r')
    outhandle = open(args.positional[1],'w')
elif len(args.positional) == 1:
    inhandle = open(args.positional[0],'r')
    outhandle = sys.stdout
elif len(args.positional) == 0:
    inhandle = sys.stdin
    outhandle = sys.stdout

for chain in vdj.parse_imgt(inhandle):
    try:
        outhandle.write( ">%s\n%s\n" % (chain.id,chain.junction_nt) )
    except AttributeError:
        pass

