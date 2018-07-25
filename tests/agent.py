"""
Unit tests for agent module.
"""
import unittest
import random
from datetime import datetime, timedelta
from data import HOURS, CARS
from dealer.agent import Agent, Bonus


class TestAgent(unittest.TestCase):
    """
    Tests for agent.
    """

    def setUp(self):
        self.start = datetime.today().replace(hour=HOURS[0])
        self.agents = [
            {
                "agent_id": "345232",
                "expertise": [1, 2, 3, 0],
                "service_time": 4,
                "rating": 0.4
            },
            {
                "agent_id": "443156",
                "expertise": [2, 0, 3, 1],
                "service_time": 5,
                "rating": 0.6
            }
        ]
        self.customers = [
            {
                "arrival_time": self.start + timedelta(hours=1),
                "interest": 0,
                "sale_closed": True
            },
            {
                "arrival_time": self.start + timedelta(hours=2),
                "interest": 3,
                "sale_closed": False
            },
            {
                "arrival_time": self.start + timedelta(hours=4),
                "interest": 2,
                "sale_closed": True
            }
        ]

    def test_init(self):
        """
        Do a rudumentary check on initialization.
        """
        Agent.init(self.agents, self.start)
        self.assertEqual(len(Agent.list), len(self.agents))

    def test_get(self):
        """
        Check the basic agent assignment.
        """
        Agent.init(self.agents, self.start)

        # Should assign agent with better expertise.
        agent, wait = Agent.get(self.customers[0])
        self.assertEqual(agent.agent_id, self.agents[1]["agent_id"])
        self.assertEqual(wait, 0)

        # Should assign agent avaialable, even if not best match.
        agent, wait = Agent.get(self.customers[1])
        self.assertEqual(agent.agent_id, self.agents[0]["agent_id"])
        self.assertEqual(wait, 0)

        # Should pick better-rated agent to tie break, even when both finish simultaneously.
        agent, wait = Agent.get(self.customers[2])
        self.assertEqual(agent.agent_id, self.agents[1]["agent_id"])
        self.assertEqual(wait, 120)

        # Should get commission only if deal closes.
        self.assertEqual(Agent.list[0].closes, 0)
        self.assertEqual(Agent.list[1].closes, 2)

        # Should show revenue generated.
        revenues = 0, sum([CARS[c]["price"] for c in [0, 2]])
        self.assertEqual(Agent.list[0].revenue, revenues[0])
        self.assertEqual(Agent.list[1].revenue, revenues[1])

        # Nobody should have got a bonus.
        self.assertEqual(Agent.list[0].bonuses, 0)
        self.assertEqual(Agent.list[1].bonuses, 0)


class TestBonus(unittest.TestCase):
    """
    Tests on the Bonus logic.
    """

    def setUp(self):
        self.start = datetime.today().replace(hour=HOURS[0])
        self.bonus = Bonus(self.start)
        random.seed(1)

    def test_bonus_a(self):
        """
        Should get no bonus if < 10 in week.
        """
        self.add(0, 7, 9)
        self.assertEqual(self.bonus.count, 0)

    def test_bonus_b(self):
        """
        Should get 1 bonus if exactly 10 in week.
        """
        self.add(0, 7, 10)
        self.assertEqual(self.bonus.count, 1)

    def test_bonus_c(self):
        """
        Should get 1 bonus even if > 20 in week.
        """
        self.add(0, 7, 21)
        self.assertEqual(self.bonus.count, 1)

    def test_bonus_d(self):
        """
        Should get 2 bonuses if >= 10 in both weeks.
        """
        self.add(0, 7, 10)
        self.add(7, 14, 30)
        self.assertEqual(self.bonus.count, 2)

    def test_bonus_e(self):
        """
        Should get 1 bonus if >= 10 only in first week.
        """
        self.add(0, 7, 10)
        self.add(7, 14, 9)
        self.assertEqual(self.bonus.count, 1)

    def test_bonus_f(self):
        """
        Should get 1 bonus if >= 10 only in second week.
        """
        self.add(0, 7, 9)
        self.add(7, 14, 30)
        self.assertEqual(self.bonus.count, 1)

    def add(self, start_day=0, end_day=7, count=10):
        """
        Add closes to generate bonus.
        """
        for days in random.choices(range(start_day, end_day), k=count):
            hours = random.choice(range(8))
            self.bonus.close(self.start + timedelta(days=days, hours=hours))


if __name__ == "__main__":
    unittest.main()
