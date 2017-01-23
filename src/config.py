###########################################################
# All Configuration Constants, Variables go in this file. #
###########################################################

LANG_MAPPING = {
    'PYTHON':       { 'ext': 'py', 'command': 'python'},
    'JAVASCRIPT':   { 'ext': 'js', 'command': 'node'},
    'RUBY':         { 'ext': 'rb', 'command': 'ruby' }
}

PROB_MAPPING = {
    'LFU_CACHE': { 
        'ip':       'problems/lfu_cache/ip_%s.txt',
        'desop':    'problems/lfu_cache/desop_%s.txt' 
    }    
}
