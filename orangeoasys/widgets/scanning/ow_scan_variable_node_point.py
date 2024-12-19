from orangeoasys.widgets.abstract.scanning.abstract_scan_variable_node_point import AbstractScanVariableLoopPoint

class ScanVariableLoopPoint(AbstractScanVariableLoopPoint):

    name = "Scanning Variable Loop Point"
    description = "Tools: LoopPoint"
    icon = "icons/cycle_variable.png"
    maintainer = "Luca Rebuffi"
    maintainer_email = "lrebuffi(@at@)anl.gov"
    priority = 1
    category = "Oasys Scanning Loops"
    keywords = ["data", "file", "load", "read"]

    def __init__(self):
        super(ScanVariableLoopPoint, self).__init__()



if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(ScanVariableLoopPoint).run()
