"""
Agent data.
"""
import random
import string
from data import CARS


def agents(count):
    """
    Generate agent data, randomly ranking expertise in the different models.
    """
    car_choices = range(len(CARS))
    for _ in range(count):
        yield {
            "agent_id": "".join(random.choices(string.digits, k=6)),
            "expertise": random.sample(car_choices, k=len(CARS)),
            "service_time": random.randint(3, 5),
            "rating": round(random.random(), 3)
        }
