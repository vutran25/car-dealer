"""
Agent object.
"""
from datetime import timedelta
from data import CARS


class Agent(object):
    """
    Car sales agent. The score attribute combines expertise and rating into one.
    The following attributes are accessible:
        - list: Class attribute giving list of agent instances.
        - agent_id: Agent ID as specified in the data.
        - closes: Total deals closed by the agent.
        - revenue: Total revenue generated.
        - bonuses: Number of bonuses earned.
    """

    def __init__(self, agent_id, expertise, service_time, rating, start):
        self.agent_id = agent_id
        self.service_time = timedelta(hours=service_time)
        self.score = [10 * e + rating for e in expertise]
        self.closes = 0
        self.revenue = 0
        self.bonus = Bonus(start)
        self.time = None

    @classmethod
    def init(cls, agents, start):
        """
        Initialize with agent data.
            - agents: Agent data.
            - start: Start date for sales.
        """
        cls.list = [cls(**d, start=start) for d in agents]

    @classmethod
    def get(cls, customer):
        """
        Assign the best agent for the customer, creating an instance if necessary.
        Return the agent and wait time (0 if an agent is readily available).
            - customer: Info of customer.
        """
        time, interest = customer["arrival_time"], customer["interest"]
        agents = list(filter(lambda a: not a.time or a.time <= time, cls.list))
        if agents:
            agent = max(agents, key=lambda a: a.score[interest])
            wait_time = 0
            agent.time = time + agent.service_time
        else:
            agent = min(cls.list, key=lambda a: a.time)
            agents = list(filter(lambda a: a.time == agent.time, cls.list))
            agent = max(agents, key=lambda a: a.score[interest])
            wait_time = (agent.time - time).total_seconds() / 60
            agent.time += agent.service_time

        if customer["sale_closed"]:
            agent.closes += 1
            agent.revenue += CARS[interest]["price"]
            agent.bonus.close(time)

        return agent, wait_time

    @property
    def bonuses(self):
        """
        Expose only the bonus count.
        """
        return self.bonus.count


class Bonus(object):
    """
    Agent bonus logic.
    """
    week = timedelta(days=7)

    def __init__(self, start):
        self.start, self.closes, self.count = start, 0, 0

    def close(self, time):
        """
        Record deal closing to figure out bonus.
        """
        if self.start <= time < self.start + self.week:
            self.closes += 1
            if self.closes == 10:
                self.closes = 0
                self.count += 1
                self.start += self.week
        elif time >= self.start + self.week:
            self.closes = 1
            days_gap = 7 * ((time - self.start).days // 7)
            self.start += timedelta(days=days_gap)
