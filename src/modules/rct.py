'''

    Program to evaluate the runtime complexity of a program
    by giving progressive inputs.

    Input: <path to file which contains progressive inputs>
    Output: Time taken for each operation to complete and how the
    time complexity progresses.

'''

import time, traceback, stat, os, sandbox
from config import *
from order import is_constant_order 
from requests.exceptions import ReadTimeout


def eval_program(paths, scale, timeout):
    src_file_path = paths['src_file_path']
    ip_file_path = paths['ip_file_path'] % scale
    actop_file_path = paths['actop_file_path']
    desop_file_path = paths['desop_file_path'] % scale

    scale_paths = {
        'src_file_path': src_file_path,
        'ip_file_path': ip_file_path,
        'actop_file_path': actop_file_path,
        'desop_file_path': desop_file_path
    }

    bef_time = time.time()
    sb = sandbox.Sandbox(src_file_path, ip_file_path)
    actop_gen = sb.run(scale, timeout)
    aft_time = time.time()

    runtime = aft_time - bef_time
    print 'source exec process returned. runtime: %s' % runtime

    with open(desop_file_path) as desop_file:
        matched = True

        while True:
            desop = desop_file.readline().strip()
            if not desop:
                break

            try:
                actop = actop_gen.next().strip()
            except StopIteration:
                if desop:
                    matched = False
                break

            if actop != desop:
                print 'WA for Actual: %s, Desired: %s' % (actop, desop)
                matched = False
                break

    sb.close()  
    result = True if matched else False
    return result, runtime

def dy_by_dx(results):
    delta = []
    for i in range(1, len(results)):
        dy = abs(results[i][1] - results[i-1][1])
        dx = abs(results[i][0] - results[i-1][0])
        delta.append(dy/dx)
    return delta

def run_at_scale(program_id, lang, code_array, problem_id):
    try:
        print 'Program ID: %s' % program_id

        # Interpolate the files' paths
        root_file_dir = '/tmp'
        problem = PROB_MAPPING[problem_id]

        if not problem:
            raise Exception('Invalid Problem ID: %s' % problem_id)

        lang_conf = LANG_MAPPING[lang]

        src_dir_path = '%s/%s/' % (root_file_dir, program_id)
        src_file_path = src_dir_path + 'program'
        actop_file_path = src_dir_path + 'output.txt'

        paths = {
            'src_file_path': src_file_path,
            'ip_file_path': problem['ip'],
            'actop_file_path': actop_file_path,
            'desop_file_path': problem['desop']
        }

        # Write lines of code to a file in /tmp directory
        os.makedirs(src_dir_path)
        with open(src_file_path, 'w') as cfn:
            cfn.write('#!/usr/bin/env %s\n' % lang_conf['command'])
            for line in code_array:
                cfn.write(line + '\n')

        # Make the source file executable
        st = os.stat(src_file_path)
        os.chmod(src_file_path, st.st_mode | stat.S_IEXEC)

        # Start the tests at different scales
        max_scale = 100000
        scale = 10

        # Get the Timeout in sec.
        timeout = problem['timeout']

        # Record the scale and corresponding run times
        final_answer = True
        runtime_series = []
        while scale <= max_scale:
            result, runtime = eval_program(paths, scale, timeout)
            #print '%s\t\t%s\t\t%s' % (result, scale, runtime)
            final_answer &= result
            runtime_series.append([scale, runtime])
            scale *= 10

        if not final_answer:
            return 'Rejected, Wrong Answer.'

        delta = dy_by_dx(runtime_series)

        # We assume a tolerance of 2 for the order.
        constant_order = is_constant_order(delta, tolerance=2)
        if constant_order:
            return 'Accepted'
        else:
            return 'Rejected, Exceeds Time Complexity. We Expect O(1).'
    except ReadTimeout:
        return 'Rejected, Takes too long to execute.'
    except Exception, ex:
        print traceback.format_exc() 
        return 'Rejected, Your Program crashed very badly.'

