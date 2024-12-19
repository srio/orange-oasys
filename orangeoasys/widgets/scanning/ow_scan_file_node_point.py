from orangeoasys.widgets.abstract.scanning.abstract_scan_file_node_point import AbstractScanFileLoopPoint

class ScanFileLoopPoint(AbstractScanFileLoopPoint):

    name = "Scanning File Loop Point"
    description = "Tools: LoopPoint"
    icon = "icons/cycle_file.png"
    maintainer = "Luca Rebuffi"
    maintainer_email = "lrebuffi(@at@)anl.gov"
    priority = 2
    category = "Oasys Scanning Loops"
    keywords = ["data", "file", "load", "read"]

    def __init__(self):
        super(ScanFileLoopPoint, self).__init__()

if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(ScanFileLoopPoint).run()
