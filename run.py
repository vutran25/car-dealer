"""
Car sales.
"""
import random
import statistics
import locale
import sys
from datetime import datetime
from data import HOURS
from data.agents import agents
from data.customers import customers
from dealer.agent import Agent
from gui.panel import Sales


class Run(object):
    """
    Run the sales.
    """

    def display(self):
        """
        Simulate sales using test data using the interactive display.
        """
        Sales.show()

    def report(self):
        """
        Simulate sales using test data and print out customer and agent reports.
        """
        random.seed(0)
        Agent.init(agents(5), datetime.today().replace(hour=HOURS[0]))
        waits = []
        for customer in customers(100):
            agent, wait = Agent.get(customer)
            waits.append(wait)

        locale.setlocale(locale.LC_ALL, locale.getlocale())
        print("{:<9.4}{:<9.4}{:<9.4}".format("MEAN", "MED", "SD"))
        print("{:<9.4}{:<9.4}{:<9.4}".format(
            statistics.mean(waits),
            statistics.median(waits),
            statistics.stdev(waits)
        ))
        print("\n{:<9}{:>6}{:>18}{:>18}{:>18}".format(
            "ID",
            "DEALS",
            "REVENUE",
            "COMMISSION",
            "BONUS"
        ))
        for agent in Agent.list:
            print("{:<9}{:>6}{:>18}{:>18}{:>18}".format(
                agent.agent_id,
                agent.closes,
                locale.currency(agent.revenue),
                locale.currency(agent.closes * 10000),
                locale.currency(agent.bonuses * 100000)
            ))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "display":
            Run().display()
        elif sys.argv[1] == "report":
            Run().report()
    else:
        Run().display()
