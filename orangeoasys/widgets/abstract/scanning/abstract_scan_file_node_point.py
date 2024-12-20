from AnyQt.QtWidgets import QFileDialog

from orangewidget import gui
from orangewidget.settings import Setting

from orangeoasys.widgets import gui as oasysgui

from orangeoasys.widgets.abstract.scanning.abstract_scan_node_point import AbstractScanLoopPoint

from orangeoasys.util.oasys_util import TriggerIn

from Orange.widgets.widget import Input, Output

class AbstractScanFileLoopPoint(AbstractScanLoopPoint):
    # inputs = [("Trigger", TriggerIn, "passTrigger"),
    #           ("Files", list, "setFiles")]


    class Inputs:
        data_trigger = Input("Trigger", TriggerIn)
        data_files = Input("Files", list)


    files_area = None
    variable_files = Setting([""])

    def create_specific_loop_box(self, box):
        box_files = oasysgui.widgetBox(box, "", addSpace=False, orientation="vertical", height=270)

        gui.button(box_files, self, "Select Height Error Profile Data Files", callback=self.select_files)

        self.files_area = oasysgui.textArea(height=200, width=360)

        self.refresh_files_text_area()

        box_files.layout().addWidget(self.files_area)

        gui.separator(box)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self,
                                                "Select Height Error Profiles", "", "Data Files (*.dat)",
                                                options=QFileDialog.Options())
        if files:
            self.variable_files = files

            self.refresh_files_text_area()

    @Inputs.data_files
    def setFiles(self, files_data):
        if not files_data is None:
            if isinstance(files_data, str):
                self.variable_files.append(files_data)
            elif isinstance(files_data, list):
                self.variable_files = files_data
            else:
                raise ValueError("Error Profile Data File: format not recognized")

            self.refresh_files_text_area()

    @Inputs.data_trigger
    def passTrigger(self, data_trigger):
        pass

    def refresh_files_text_area(self):
        text = ""
        for file in self.variable_files:
            text += file + "\n"
        self.files_area.setText(text)

        self.number_of_new_objects = len(self.variable_files)

    def has_variable_um(self): return False

    def get_current_value_type(self): return str

    def initialize_start_loop(self):
        self.current_variable_value = self.variable_files[0]
        self.number_of_new_objects = len(self.variable_files)

        self.start_button.setEnabled(False)

        return True

    def keep_looping(self):
        if self.current_new_object < self.number_of_new_objects:
            if self.current_variable_value is None: self.current_new_object = 1
            else:                                   self.current_new_object += 1

            self.current_variable_value = self.variable_files[self.current_new_object - 1]

            return True
        else:
            return False



