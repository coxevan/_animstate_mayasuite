#python
import os

#animstate
import animstate.const

# maya
import pymel.core
import PySide2.QtGui as qtgui
import PySide2.QtCore as qtcore
import PySide2.QtWidgets as qtwidgets
import shiboken2
import maya.OpenMayaUI as apiUI


def get_maya_window():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    # from https://stackoverflow.com/questions/22331337/how-to-get-maya-main-window-pointer-using-pyside
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken2.wrapInstance(long(ptr), qtgui.QWindow)

def maya_to_qt(maya_name):
    """Convert a Maya ui path to a Qt object.

    :param maya_name: Maya UI Path to convert
        (Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" )
    :return: PyQt representation of that object
    """
    ptr = apiUI.MQtUtil.findControl(maya_name)
    if ptr is None:
        ptr = apiUI.MQtUtil.findLayout(maya_name)
    if ptr is None:
        ptr = apiUI.MQtUtil.findMenuItem(maya_name)

    if ptr is not None:
        return shiboken2.wrapInstance(long(ptr), qtwidgets.QWidget)


class Window(object):
    window_cache = {}
    def __init__(self, ui_name):
        '''
        Create a window from a specified .ui file in the resources/ui directory
        :param str ui_name:
        '''
        if self._window_exists(ui_name):
            existing_window = self._get_cached_window(ui_name)
            pymel.core.evalDeferred(lambda:existing_window.close())

        self._add_to_cache(ui_name, self)
        # Use this as a stopper for methods that shouldn't be run during a close event.
        # (things that are run on selection/click etc.)
        self._closing = False

        if not isinstance(ui_name, str):
            raise RuntimeWarning('Ui file must be specified and a string. Found: {0}'.format(ui_name))

        if not ui_name.endswith('.ui'):
            ui_name = ui_name + '.ui'

        full_ui_path = os.path.join(animstate.const.FULL_UI_DIRECTORY, ui_name)
        if not os.path.exists(full_ui_path):
            raise RuntimeWarning('Ui file not found: {0}'.format(full_ui_path))

        self._ui = pymel.core.loadUI(uiFile=full_ui_path)
        self.show()
        self.window = maya_to_qt(self._ui)

    @classmethod
    def _window_exists(cls, window_name):
        return cls.window_cache.has_key(window_name)

    @classmethod
    def _add_to_cache(cls, window_name, instance):
        if not cls._window_exists(window_name):
            cls.window_cache[window_name] = instance
            return True
        return False

    @classmethod
    def _get_cached_window(cls, window_name):
        if cls.window_cache.has_key(window_name):
            return cls.window_cache[window_name]
        return None

    def show(self):
        pymel.core.showWindow(self._ui)

    def close(self):
        self._closing = True
        self.window.close()

    def __getattr__(self, item):
        try:
            result = self.__getattribute__(item)
        except AttributeError:
            result = qtcore.QObject.findChild(self.window, qtwidgets.QWidget, item)
        return result