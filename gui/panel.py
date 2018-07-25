"""
Display panel to show sales stats.
"""

from PyQt5.QtWidgets import QApplication, QWidget


class Sales(object):
    """
    Interactive panel.
    """

    @staticmethod
    def show():
        """
        Bring up the panel to interactively show sales data.
        """
        app = QApplication([])

        window = QWidget()
        window.show()

        app.exec()
