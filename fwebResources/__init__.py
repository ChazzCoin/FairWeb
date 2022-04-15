import random
import os
from pathlib import Path

def get_parent_directory():
    path = Path(os.getcwd())
    return path.parent.absolute().__str__()

class Resource:
    USER_AGENTS = os.path.join(get_parent_directory(), 'FWEB/fwebResources/useragents.txt')

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