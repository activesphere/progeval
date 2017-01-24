'''

    Program to evaluate the runtime complexity of a program
    by giving progressive inputs.

    Input: <path to file which contains progressive inputs>
    Output: Time taken for each operation to complete and how the
    time complexity progresses.

'''

import subprocess, time, traceback, os, stat, signal
from config import *
from order import is_constant_order 

class AlarmTimeoutException(Exception):
    pass

class SourceTimeoutException(Exception):
    pass

def alarm_timeout_handler(signum, frame):
    raise AlarmTimeoutException()

class SourceExecProcess(object):
    def __init__(self, timeout, paths):
        self.timeout = timeout
        self.src_file_path = paths.pop('src_file_path')
        self.ip_file_path = paths.pop('ip_file_path')
        self.actop_file_path = paths.pop('actop_file_path')
        self.desop_file_path = paths.pop('desop_file_path')
        self.subproc = None

    def run(self): 
        with open(self.ip_file_path) as ip_file, open(self.actop_file_path, 'w') as actop_file,\
            open(self.desop_file_path) as desop_file:
          
            try:
                signal.signal(signal.SIGALRM, alarm_timeout_handler)
                self.subproc = subprocess.Popen(['%s' % self.src_file_path], stdout=actop_file, stdin=ip_file)
                signal.alarm(self.timeout)
                bef_time = time.time()
                data, err = self.subproc.communicate()
                aft_time = time.time()
                result = aft_time - bef_time
            except AlarmTimeoutException:
                result = -1
            finally:
                signal.alarm(0)
                return result

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

    runtime = SourceExecProcess(timeout=timeout, paths=scale_paths).run()
    print 'source exec process returned. runtime: %s' % runtime

    if runtime == -1:
        raise SourceTimeoutException()
        
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
        # Interpolate the files' paths
        root_file_dir = '/tmp'
        problem = PROB_MAPPING[problem_id]

        if not problem:
            raise Exception('Invalid Problem ID: %s' % problem_id)

        lang_conf = LANG_MAPPING[lang]

        paths = {
            'src_file_path': '%s/program_%s.%s' % (root_file_dir, program_id, lang_conf['ext']),
            'ip_file_path': problem['ip'],
            'actop_file_path': '%s/output_%s.txt' % (root_file_dir, program_id),
            'desop_file_path': problem['desop']
        }
        src_file_path = paths['src_file_path']

        # Write lines of code to a file in /tmp directory
        with open(src_file_path, 'w') as cfn:
            cfn.write('#!/usr/bin/env %s\n' % lang_conf['command'])
            for line in code_array:
                cfn.write(line + '\n')

        # Make the source file executable
        st = os.stat(src_file_path)
        os.chmod(src_file_path, st.st_mode | stat.S_IEXEC)

        # Start the tests at different scales
        max_scale = 1000000
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
    except SourceTimeoutException:
        return 'Rejected, Takes too long to execute.'
    except Exception, ex:
        print traceback.format_exc() 
        return 'Rejected, Your Program crashed very badly.'

