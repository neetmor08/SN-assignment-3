import tkinter as tk
from tkinter import scrolledtext

class BaseFrame(tk.LabelFrame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)


class ModelInfoFrame(BaseFrame):

    def __init__(self, master):
        super().__init__(master, text="Selected Model Info", padx=10, pady=5)
        text = scrolledtext.ScrolledText(self, width=45, height=8)
        text.pack(fill="both", expand=True)

        info = (
            "DistilGPT2\n"
            "- Category: Text Generation\n"
            "- Small version of GPT-2 for English text generation\n\n"
            "Whisper-small\n"
            "- Category: Automatic Speech Recognition\n"
            "- Robust ASR trained on large-scale weak supervision\n"
        )

        refs = (
            "\nReferences:\n"
            "• https://huggingface.co/distilgpt2\n"
            "• https://huggingface.co/openai/whisper-small\n"
        )

        text.insert(tk.END, info + refs)
        text.configure(state="disabled")


class ExplanationFrame(BaseFrame):
    
    def __init__(self, master):
        super().__init__(master, text="OOP Concepts Explanation", padx=10, pady=5)
        text = scrolledtext.ScrolledText(self, width=45, height=8)
        text.pack(fill="both", expand=True)

        explanation = (
            "• Encapsulation: Model classes hide pipelines inside objects.\n"
            "• Polymorphism: Both models inherit AIModel and implement run().\n"
            "• Method Overriding: run() behaves differently for each model.\n"
            "• Multiple Inheritance: Frames combine BaseFrame + tk widgets.\n"
            "• Decorators: log_action & handle_errors wrap button callbacks.\n"
        )

        text.insert(tk.END, explanation)
        text.configure(state="disabled")
