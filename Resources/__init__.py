import random
import os

class Resource:
    USER_AGENTS = os.path.join(os.path.dirname(__file__), 'useragents.txt')

def get_random_user_agent():
    return get_random_resource(Resource.USER_AGENTS)

def get_random_resource(resource):
    """Uses generator to return next useragent in saved file
    """
    items = get_resource(resource)
    selection = random.randint(0, len(items) - 1)
    agent = items[selection]
    return agent.strip()

def get_resource(resource):
    """Uses generator to return next useragent in saved file
    """
    with open(resource, 'r') as f:
        agents = f.readlines()
        return agents