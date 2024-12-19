from orangeoasys.widgets import gui as oasysgui

from orangewidget import gui
from PyQt5.QtGui import QFont, QPalette, QColor
from orangewidget.settings import Setting

from orangeoasys.widgets.abstract.scanning.abstract_scan_node_point import AbstractScanLoopPoint

class AbstractScanVariableLoopPoint(AbstractScanLoopPoint):

    variable_value_from = Setting(0.0)
    variable_value_to = Setting(0.0)
    variable_value_step = Setting(0.0)

    list_of_values = Setting([""])
    kind_of_loop = Setting(0)

    def create_specific_loop_box(self, box):
        gui.separator(box)

        gui.comboBox(box, self, "kind_of_loop", label="Kind of Loop", labelWidth=350,
                     items=["From Range", "From List"],
                     callback=self.set_KindOfLoop, sendSelectedValue=False, orientation="horizontal")

        self.box_1 = oasysgui.widgetBox(box, "", addSpace=False, orientation="vertical", width=360, height=160)
        self.box_2 = oasysgui.widgetBox(box, "", addSpace=False, orientation="vertical", width=360, height=160)

        oasysgui.lineEdit(self.box_1, self, "variable_value_from", "Value From", labelWidth=250, valueType=float, orientation="horizontal", callback=self.calculate_step)
        oasysgui.lineEdit(self.box_1, self, "variable_value_to", "Value to", labelWidth=250, valueType=float, orientation="horizontal", callback=self.calculate_step)
        oasysgui.lineEdit(self.box_1, self, "number_of_new_objects", "Number of Steps", labelWidth=250, valueType=int, orientation="horizontal", callback=self.calculate_step)

        self.list_of_values_ta = oasysgui.textArea(height=150, width=360, readOnly=False)
        self.list_of_values_ta.textChanged.connect(self.list_of_values_ta_changed)

        text = ""
        for value in self.list_of_values:
            text += value + "\n"

        self.list_of_values_ta.setText(text[:-1])
        self.box_2.layout().addWidget(self.list_of_values_ta)

        self.le_variable_value_step = oasysgui.lineEdit(self.box_1, self, "variable_value_step", "Step Value", labelWidth=250, valueType=float, orientation="horizontal")
        self.le_variable_value_step.setReadOnly(True)
        font = QFont(self.le_variable_value_step.font())
        font.setBold(True)
        self.le_variable_value_step.setFont(font)
        palette = QPalette(self.le_variable_value_step.palette()) # make a copy of the palette
        palette.setColor(QPalette.Text, QColor('dark blue'))
        palette.setColor(QPalette.Base, QColor(243, 240, 160))
        self.le_variable_value_step.setPalette(palette)

        self.set_KindOfLoop()
        self.calculate_step()

        gui.separator(box)

    def list_of_values_ta_changed(self):
        self.list_of_values = []

        values = self.list_of_values_ta.toPlainText().split("\n")
        for value in values:
            if not value.strip() == "": self.list_of_values.append(value)

        if self.kind_of_loop==1: self.number_of_new_objects = len(self.list_of_values)

        if len(self.list_of_values) == 0: self.list_of_values.append("")

    def set_KindOfLoop(self):
        self.box_1.setVisible(self.kind_of_loop == 0)
        self.box_2.setVisible(self.kind_of_loop == 1)

    def calculate_step(self):
        try:    self.variable_value_step = round((self.variable_value_to - self.variable_value_from) / self.number_of_new_objects, 8)
        except: self.variable_value_step = 0.0

    def get_current_value_type(self): return float

    def initialize_start_loop(self):
        do_loop = True

        if self.kind_of_loop == 0:
            self.current_variable_value = round(self.variable_value_from, 8)
            self.calculate_step()
        elif len(self.list_of_values) > 0:
            self.current_variable_value = self.list_of_values[self.current_new_object - 1]
        else:
            do_loop = False

        return do_loop

    def keep_looping(self):
        if (self.current_new_object < self.number_of_new_objects) or (self.current_new_object == self.number_of_new_objects and self.kind_of_loop==0):
            if self.current_variable_value is None:
                self.current_new_object = 1

                if self.kind_of_loop == 0:
                    self.current_variable_value = round(self.variable_value_from, 8)
                    self.calculate_step()
                elif len(self.list_of_values) > 0:
                    self.current_variable_value = self.list_of_values[self.current_new_object - 1]
            else:
                self.current_new_object += 1
                if self.kind_of_loop == 0:
                    self.current_variable_value = round(self.current_variable_value + self.variable_value_step, 8)
                elif len(self.list_of_values) > 0:
                    self.current_variable_value = self.list_of_values[self.current_new_object - 1]
            return True
        else:
            return False
