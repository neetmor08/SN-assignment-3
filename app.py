import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from models import TextGenModel, SpeechToTextModel
from views import ModelInfoFrame, ExplanationFrame
from decorators import log_action, handle_errors

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter AI GUI")
        self.geometry("850x650")

        self.text_model = TextGenModel()
        self.audio_model = SpeechToTextModel()
        self.audio_path = None

        self._create_menu()
        self._create_top_row()
        self._create_middle_row()
        self._create_info_row()
        self._create_notes_row()
    def _create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        model_menu = tk.Menu(menubar, tearoff=0)
        model_menu.add_command(label="Reload Models", command=self._reload_models)
        menubar.add_cascade(label="Models", menu=model_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)
    
    def _create_top_row(self):
        top = tk.Frame(self)
        top.pack(fill="x", pady=5)

        tk.Label(top, text="Model Selection:", font=("Arial", 11)).pack(side="left", padx=5)

        self.model_choice = tk.StringVar(value="Text Generation")
        ttk.Combobox(
            top,
            textvariable=self.model_choice,
            values=["Text Generation", "Speech-to-Text"],
            width=25,
            state="readonly",
        ).pack(side="left", padx=5)

        tk.Button(top, text="Load Model", command=self._reload_models).pack(side="left", padx=5)
    
    def _create_middle_row(self):
        middle = tk.Frame(self)
        middle.pack(fill="both", expand=True, padx=5, pady=5)
       
        input_frame = tk.LabelFrame(middle, text="User Input Section", padx=10, pady=10)
        input_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.input_type = tk.StringVar(value="Text")
        tk.Radiobutton(input_frame, text="Text", variable=self.input_type, value="Text",
                       command=self._on_type_change).pack(anchor="w")
        tk.Radiobutton(input_frame, text="Audio", variable=self.input_type, value="Audio",
                       command=self._on_type_change).pack(anchor="w")

        self.browse_btn = tk.Button(input_frame, text="Browse", command=self._browse_audio)
        self.browse_btn.pack_forget()

        self.input_box = scrolledtext.ScrolledText(input_frame, width=40, height=5)
        self.input_box.pack(pady=5)

        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Run Model 1", command=lambda: self._run_model(1)).grid(row=0, column=0, padx=3)
        tk.Button(btn_frame, text="Run Model 2", command=lambda: self._run_model(2)).grid(row=0, column=1, padx=3)
        tk.Button(btn_frame, text="Clear", command=self._clear_all).grid(row=0, column=2, padx=3)
 
        output_frame = tk.LabelFrame(middle, text="Model Output Section", padx=10, pady=10)
        output_frame.pack(side="right", fill="both", expand=True, padx=5)

        tk.Label(output_frame, text="Output Display:", font=("Arial", 11)).pack(anchor="w")
        self.output_box = scrolledtext.ScrolledText(output_frame, width=45, height=10)
        self.output_box.pack(pady=5, fill="both", expand=True)

    def _create_info_row(self):
        info_row = tk.Frame(self)
        info_row.pack(fill="x", pady=5, padx=5)

        # Left: model info & references
        self.model_info = ModelInfoFrame(info_row)
        self.model_info.pack(side="left", fill="both", expand=True, padx=5)

        self.explanation = ExplanationFrame(info_row)
        self.explanation.pack(side="right", fill="both", expand=True, padx=5)

    def _create_notes_row(self):
        notes_frame = tk.LabelFrame(self, text="Notes / References", padx=10, pady=5)
        notes_frame.pack(fill="x", padx=5, pady=5)
        self.notes = scrolledtext.ScrolledText(notes_frame, height=4)
        self.notes.pack(fill="x")
        self.notes.insert(
            tk.END,
            "References:\n"
            "- DistilGPT2: https://huggingface.co/distilgpt2\n"
            "- OpenAI-Whisper-small: https://huggingface.co/openai/whisper-small\n"
            "- Radford et al.,(2019) “Language Models are Unsupervised Multitask Learners” (GPT-2)\n"
            "- Radford et al.,(2022) “Robust Speech Recognition via Large-Scale Weak Supervision” (Whisper)\n",
        )
        self.notes.configure(state="disabled")
    
    def _on_type_change(self):
        if self.input_type.get() == "Audio":
            self.browse_btn.pack(pady=4)
        else:
            self.browse_btn.pack_forget()
            self.input_box.delete("1.0", tk.END)

    @log_action
    def _browse_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        if path:
            self.audio_path = path
            self.input_box.delete("1.0", tk.END)
            self.input_box.insert(tk.END, f"[Audio file selected: {path}]")

    @log_action
    @handle_errors
    def _run_model(self, which):
       
        self.output_box.delete("1.0", tk.END)
        if self.input_type.get() == "Text":
            text = self.input_box.get("1.0", tk.END).strip() or "Hello world"
            result = self.text_model.run(text)
        else:
            if not self.audio_path:
                raise ValueError("Please browse for an audio file.")
            result = self.audio_model.run(self.audio_path)
        self.output_box.insert(tk.END, result)

    @log_action
    def _clear_all(self):
        self.input_box.delete("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)
        self.audio_path = None

    def _reload_models(self):
        self.text_model = TextGenModel()
        self.audio_model = SpeechToTextModel()
        tk.messagebox.showinfo("Models", "Models reloaded successfully.")

    def _show_about(self):
        tk.messagebox.showinfo("About", "AI GUI using Tkinter, Hugging Face models, and OOP concepts.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
