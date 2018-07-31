"""
Display panel to show sales stats.
"""
import random
import statistics
import locale
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel,\
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, \
    QSpacerItem
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSlot

from data import HOURS
from data.agents import agents
from data.customers import customers
from dealer.agent import Agent

STYLE = open("gui/style.css").read()


class Sales(object):
    """
    Interactive panel.
    """

    def __init__(self):
        self.agents = 0
        self.customers = 0

    @staticmethod
    @pyqtSlot()
    def initAgent(agentNum):
        """
        Initialize the number of agents
        """
        Sales.agents = int("0" + agentNum)

    @staticmethod
    @pyqtSlot()
    def initCustomer(customerNum):
        """
        Initialize the number of customers
        """
        Sales.customers = int("0" + customerNum)

    @staticmethod
    @pyqtSlot()
    def showTable():
        """
        Show all the performaces results and display them in a QTableWidget
        """
        random.seed(0)

        # Check if user enter 0
        if Sales.agents == 0 or Sales.customers == 0:
            Sales.table.setRowCount(0)
            Sales.mean.setText("0.0")
            Sales.median.setText("0.0")
            Sales.sd.setText("0.0")
            return
        # Else do regular logic and display result to the table
        else:
            Agent.init(agents(Sales.agents),
                       datetime.today().replace(hour=HOURS[0]))
            waits = []
            for customer in customers(Sales.customers):
                agent, wait = Agent.get(customer)
                waits.append(wait)
            locale.setlocale(locale.LC_ALL, locale.getlocale())
            Sales.mean.setText(str(statistics.mean(waits)))
            Sales.median.setText(str(statistics.median(waits)))
            if len(waits) == 1:
                Sales.sd.setText("0.0")
            else:
                Sales.sd.setText("{:.2f}".format(statistics.stdev(waits)))
            Sales.table.setRowCount(Sales.agents)
            for index, agent in enumerate(Agent.list):
                Sales.table.setItem(
                    index, 0, QTableWidgetItem(str(agent.agent_id)))
                Sales.table.setItem(
                    index, 1, QTableWidgetItem(str(agent.closes)))
                Sales.table.setItem(index, 2, QTableWidgetItem(
                    str(locale.currency(agent.revenue))))
                Sales.table.setItem(index, 3, QTableWidgetItem(
                    str(locale.currency(agent.closes * 10000))))
                Sales.table.setItem(index, 4, QTableWidgetItem(
                    str(locale.currency(agent.bonuses * 100000))))

    @staticmethod
    def show():
        """
        Bring up the panel to interactively show sales data.
        """
        app = QApplication([])
        app.setApplicationName("Car Sales")
        app.setStyleSheet(STYLE)

        window = QWidget()
        page = QGridLayout(window)
        # Row 0 has 2 labels
        for index, lable in enumerate(["Agents", "Customers"]):
            page.addWidget(QLabel(lable), 0, index*2, 1, 2)
        # Row 1 has 2 LineEdit and 1 Run button
        agentInput = QLineEdit()
        page.addWidget(agentInput, 2, 0, 1, 2)
        customerInput = QLineEdit()
        page.addWidget(customerInput, 2, 2, 1, 2)

        runButton = QPushButton("Run")
        page.addWidget(runButton, 2, 4)

        # Row 2 has spacing accordingly
        page.addItem(QSpacerItem(200, 20), 3, 0, 1, 7)

        # Row 3 has 3 Labels
        for index, lable in enumerate(["Mean", "Median", "SD"]):
            page.addWidget(QLabel(lable), 4, index)

        # Row 4 has 3 labels contain result values
        Sales.mean = QLabel("0.0")
        Sales.median = QLabel("0.0")
        Sales.sd = QLabel("0.0")
        for index, value in enumerate([Sales.mean, Sales.median, Sales.sd]):
            page.addWidget(value, 5, index)

        # Row 5 is a table display results
        table = QTableWidget(5, 5)
        Sales.table = table
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setHorizontalHeaderLabels(
            ["ID", "Deals", "Revenue", "Commission", "Bonus"]
        )
        page.addWidget(table, 6, 0, 1, 7)

        # Set IntValidator to only accept integers
        agentInput.setValidator(QIntValidator(0, 500))
        customerInput.setValidator(QIntValidator(0, 10000))
        # Get input from users
        agentInput.textChanged.connect(Sales.initAgent)
        customerInput.textChanged.connect(Sales.initCustomer)
        # Run result if run clicked
        runButton.clicked.connect(Sales.showTable)

        window.show()

        app.exec()
