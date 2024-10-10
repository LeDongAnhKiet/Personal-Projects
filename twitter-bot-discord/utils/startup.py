from time import strftime, gmtime


def pprint(message):
    # Pretty print a message during startup
    print(f"[INFO {strftime('%Y-%m-%d %H:%M:%S', gmtime())}]: {message}")
