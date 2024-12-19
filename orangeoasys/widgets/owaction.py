from AnyQt.QtWidgets import QAction
class OWAction(QAction):
    """
    An action to be inserted into canvas right click context menu.

    Actions defined and added this way are pulled from the widget and
    inserted into canvas GUI's right context menu. The actions must
    be defined in the OWWidget's `__init__` method and added to the
    widget with `QWidget.addAction`.

    """
    pass