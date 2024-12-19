import sys

from orangeoasys.widgets import widget
# from Orange.widgets import widget
from Orange.widgets.widget import OWWidget

from orangewidget import  gui

from PyQt5 import QtGui

from orangeoasys.util.oasys_util import TriggerOut
from silx.gui import qt
from Orange.widgets.widget import Input, Output


class Pin(OWWidget): # qt.QWidget): # widget.OWWidget):

    name = "Pin"
    description = "Tools: Pin"
    icon = "icons/pin.png"
    maintainer = "Luca Rebuffi"
    maintainer_email = "lrebuffi(@at@)anl.gov"
    priority = 3
    category = "Oasys Basic Loops"
    keywords = ["data", "file", "load", "read"]

    class Inputs:
        data = Input("Trigger", TriggerOut)

    class Outputs:
        data = Output("Trigger", TriggerOut)

    # inputs = [("Trigger", TriggerOut, "passTrigger")]
    #
    # outputs = [{"name":"Trigger",
    #             "type":TriggerOut,
    #             "doc":"Trigger",
    #             "id":"Trigger"}]

    want_main_area = 0
    want_control_area = 1

    def __init__(self):
         # super().__init__()
         self.setFixedWidth(300)
         self.setFixedHeight(100)

         gui.separator(self.controlArea, height=20)
         gui.label(self.controlArea, self, "         SIMPLE PASSAGE POINT", orientation="horizontal")
         gui.rubber(self.controlArea)

    # def passTrigger(self, trigger):
    @Inputs.data
    def set_data(self, trigger):
        # self.send("Trigger", trigger)
        self.Outputs.data.send(trigger)


if __name__ == "__main__":
    from PyQt5 import QtGui, QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ow = Pin()
    ow.show()
    app.exec_()
    ow.saveSettings()

    # a = QtGui.QApplication(sys.argv)
    # ow = Pin()
    # ow.show()
    # a.exec_()
    # ow.saveSettings()
    # from orangewidget.utils.widgetpreview import WidgetPreview
    # WidgetPreview(Pin).run()
