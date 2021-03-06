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

import optparse

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import vdj
import vdj.analysis

option_parser = optparse.OptionParser()
option_parser.add_option('-s','--samples')
option_parser.add_option('-q','--quantify',choices=['clone','junction','v','j','vj','vdj'])
option_parser.add_option('-f','--freq',action='store_true')
(options,args) = option_parser.parse_args()

if len(args) == 1:
    inhandle = open(args[0],'r')
else:
    raise ValueError, "Must give a single argument to vdjxml file"

# determine mapping between barcodes and samples
sampledict = {}
ip = open(options.samples,'r')
for line in ip:
    sampledict[line.split()[0]] = line.split()[1]
ip.close()

features = ['barcode',options.quantify]
(uniq_feature_values,countdict) = vdj.analysis.imgt2countdict(inhandle,features)
max_size = max([max(cd.itervalues()) for cd in countdict.itervalues()])

# make the plots
outbasename = '.'.join(args[0].split('.')[:-1])

colors_10 = ['#e31a1c',
            '#377db8',
            '#4daf4a',
            '#984ea3',
            '#ff7f00',
            '#ffff33',
            '#a65628',
            '#f781bf',
            '#999999',
            '#444444']
markers = 'ovs^<>ph*d'

fig = plt.figure()
ax = fig.add_subplot(111)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_position(('outward',5))
ax.spines['left'].set_position(('outward',5))
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
for (i,(barcode,label)) in enumerate(sampledict.iteritems()):
    num_chains = sum(countdict[barcode].values())
    sizes = np.arange(1,max_size+1)
    (hist,garbage) = np.histogram(countdict[barcode].values(),bins=sizes)
    idxs = hist > 0
    if options.freq == True:
        freqs = np.float_(sizes) / num_chains
        ax.plot(freqs[idxs],hist[idxs],marker=markers[i],linestyle='None',color=colors_10[i],markeredgewidth=0,markersize=4,clip_on=False,label=label)
    else:
        ax.plot(sizes[idxs],hist[idxs],marker=markers[i],linestyle='None',color=colors_10[i],markeredgewidth=0,markersize=4,clip_on=False,label=label)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(options.quantify+(' frequency' if options.freq else ' counts'))
ax.set_ylabel('number')
leg = ax.legend(loc=0,numpoints=1,prop=mpl.font_manager.FontProperties(size='small'))
leg.get_frame().set_visible(False)
# fig.show()
fig.savefig(outbasename+'.%shist.png' % options.quantify)
fig.savefig(outbasename+'.%shist.pdf' % options.quantify)
