'''
    Program to evaluate the runtime complexity of a program
    by giving progressive inputs.

    Input: <path to file which contains progressive inputs>
    Output: Time taken for each operation to complete and how the
    time complexity progresses.

'''

import subprocess, time, traceback, os, stat
from order import is_constant_order 

LANG_MAPPING = {
    'PYTHON':   { 'ext': 'py' },
}

def create_io_files(paths, scale):
    ip_file_path = paths['ip_file_path']
    actop_file_path = paths['actop_file_path']
    desop_file_path = paths['desop_file_path']

    with open(ip_file_path,'w') as ipf, open(desop_file_path,'w') as dopf:
        for i in range(scale):
            ipf.write('PUT %s %s\n' % (i,i))
            dopf.write('INSERTED %s\n' % i)
        for i in range(scale-1, -1, -1):
            ipf.write('GET %s\n' % i)
            dopf.write('%s\n' % i)
        ipf.write('\n')
        dopf.write('\n')
        
    with open(actop_file_path, 'w'):
            pass

def eval_program(paths, scale):
    src_file_path = paths['src_file_path']
    ip_file_path = paths['ip_file_path']
    actop_file_path = paths['actop_file_path']
    desop_file_path = paths['desop_file_path']

    create_io_files(paths, scale)

    with open(ip_file_path) as ip_file, open(actop_file_path, 'w+') as actop_file, open(desop_file_path) as desop_file:
        proc = subprocess.Popen(['%s' % src_file_path], stdout=actop_file, stdin=ip_file)
        
        bef_time = time.time()
        proc.communicate()
        proc.wait()
        aft_time = time.time()
        run_time = aft_time - bef_time
    
    with open(actop_file_path) as actop_file, open(desop_file_path) as desop_file:
        matched = True

        while True:
            actop = actop_file.readline().strip()
            desop = desop_file.readline().strip()

            if desop == '':
                break

            if actop != desop:
                print 'WA for Actual: %s, Desired: %s' % (actop, desop)
                matched = False
                break

        result = 'Correct' if matched else 'Incorrect'

        return result, run_time

def dy_by_dx(results):
    delta = []
    for i in range(1, len(results)):
        dy = abs(results[i][1] - results[i-1][1])
        dx = abs(results[i][0] - results[i-1][0])
        delta.append(dy/dx)
    return delta

def run_at_scale(program_id, lang, code_array):
    try:
        # Interpolate the files' paths
        root_file_dir = '/tmp'
        paths = {
            'src_file_path': '%s/program_%s.%s' % (root_file_dir, program_id, LANG_MAPPING[lang]['ext']),
            'ip_file_path': '%s/input_%s.txt' % (root_file_dir, program_id),
            'actop_file_path': '%s/output_%s.txt' % (root_file_dir, program_id),
            'desop_file_path': '%s/desired_output_%s.txt' % (root_file_dir, program_id)
        }
        src_file_path = paths['src_file_path']

        # Write lines of code to a file in /tmp directory
        with open(src_file_path, 'w') as cfn:
            cfn.write('#!/usr/bin/env python\n')
            for line in code_array:
                cfn.write(line + '\n')

        # Make the source file executable
        st = os.stat(src_file_path)
        os.chmod(src_file_path, st.st_mode | stat.S_IEXEC)

        # Start the tests at different scales
        max_scale = 1000000
        scale = 10

        # Record the scale and corresponding run times
        results = []
        while scale <= max_scale:
            result, run_time = eval_program(paths, scale)
            print '%s\t\t%s\t\t%s' % (result, scale, run_time)
            results.append([scale, run_time])
            scale *= 10
        
        delta = dy_by_dx(results)

        # We assume a tolerance of 2 for the order.
        constant_order = is_constant_order(delta, tolerance=2)
        if constant_order:
            return 'ACCEPTED'
        else:
            return 'REJECTED'
    except Exception, ex:
        print traceback.format_exc() 
        return 'REJECTED'

