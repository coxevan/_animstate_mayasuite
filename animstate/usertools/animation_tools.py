'''
A window for animation tools!
'''
#todo: recursive script finding with categories
#todo: user defined macros
#todo: user copying/editing
import os

# animstate imports
import animstate.util.gui
import animstate.const

SCRIPT_DIRECTORY = os.path.join(animstate.const.FULL_RESOURCES_DIR, 'userscripts')

class AnimationToolsWindow(animstate.util.gui.Window):
    def __init__(self):
        animstate.util.gui.Window.__init__(self, 'animation_tools')
        self.refresh_script_tree()

        self.runScriptButton.clicked.connect(self.run_selected_script_cmd)
        self.scriptListWidget.currentItemChanged.connect(self.on_item_changed_cmd)
        self.scriptListWidget.itemDoubleClicked.connect(self.run_selected_script_cmd)

    def refresh_script_tree(self, network = False):
        '''
        Refresh the interface with the scripts found on the HDD
        :param bool network: scrape files from git
        :return: True/False
        '''
        #todo: should this be a file tree instead of a list widget?
        dir_contents = os.listdir(SCRIPT_DIRECTORY)
        py_files = [_file for _file in dir_contents if _file.endswith('.py')]
        self.scriptListWidget.addItems(py_files)

    def run_selected_script_cmd(self, *args):
        print 'Running'

    def on_item_changed_command(self, *args):
        print args

def show():
    window = AnimationToolsWindow()
    window.show()