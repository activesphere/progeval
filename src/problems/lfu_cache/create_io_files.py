#!/usr/bin/env python

'''
Module to create ip_(scale).txt and desop_(scale).txt files for LFU Cache problem statement.

'''

def create_io_files(scale):
    with open('ip_%s.txt' % scale, 'w') as ip, open('desop_%s.txt' % scale, 'w') as desop:
        for i in range(scale):
            ip.write('PUT %s %s\n' % (i, i))
            desop.write('INSERTED %s\n' % i)
        for i in range(scale-1, -1, -1):
            ip.write('GET %s\n' % i)
            desop.write('%s\n' % i)
        ip.write('\n')

scale = 10
max_scale = 1000000

while(scale <= max_scale):
    create_io_files(scale)
    scale *= 10
