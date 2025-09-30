from functools import wraps
from tkinter import messagebox

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} called")
        return func(*args, **kwargs)
    return wrapper

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
    return wrapper
