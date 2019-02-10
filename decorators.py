from bot import Bot


def handler(*args, **kwargs):
    if "other_states" in kwargs:
        states = kwargs["other_states"]
    else:
        states = list()

    if "state" not in kwargs:
        raise Exception("A handler must provide a state parameter.")
    states.append(kwargs["state"])

    def decorator(func):
        for state in states:
            if state not in Bot.handlers:
                Bot.handlers[state] = list()
            
            Bot.handlers[state].append(func)
        print("Registering handler: {} for {}".format(func.__name__, kwargs))

    return decorator
