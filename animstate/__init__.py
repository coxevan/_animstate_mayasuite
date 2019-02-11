import os
from importlib import import_module
import inspect

import usertools

USER_TOOLS_DIR = os.path.dirname(usertools.__file__)

def open_tool(tool_name):
    '''
    run an interface's "show" command
    :param str tool_name: tool to run
    :return: True/False
    '''
    # Don't import everything all at once. But let's search usertools for it
    #todo: determine what will happen if we ever need subfolders for user tools?
    dir_contents = os.listdir(USER_TOOLS_DIR)
    for _file in dir_contents:
        if _file.endswith('.pyc') or _file.startswith('__'):
            # We don't want to open any rogue pycs that aren't getting culled.
            # We don't want to load init's or any private tool functions from this. We can use __ as a means of testing
            # interfaces without a need to expose it everywhere.
            continue
        module_name = _file.split('.')[0]
        if module_name.lower() == tool_name.lower():
            module = import_module('{0}.{1}'.format(usertools.__name__, module_name))
            try:
                module.show()
                return True
            except AttributeError as exception:
                if "'module' object has no attribute 'show'" in exception.message:
                    # This is non-critical.
                    print 'Module {0} has no show method.'.format(module)
                else:
                    # if it's not just a problem with the module not having show, we should raise it.
                    raise
    return False
