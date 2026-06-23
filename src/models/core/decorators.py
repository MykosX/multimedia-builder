
# src/models/core/decorators.py

def command(name):
    def decorator(func):
        func._command_name = name
        return func
    return decorator
