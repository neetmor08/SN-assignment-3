from transformers import pipeline

class AIModel:

    def run(self, data):
        raise NotImplementedError("Subclasses must override run()")


class TextGenModel(AIModel):
    """
    DistilGPT2 for text generation.

    Reference:
    - https://huggingface.co/distilgpt2
    - Radford et al.,(2019) “Language Models are Unsupervised Multitask Learners”
    """

    def __init__(self):
        self._generator = pipeline("text-generation", model="distilgpt2")

    def run(self, text):
        return self._generator(text, max_length=40, num_return_sequences=1)[0]["generated_text"]


class SpeechToTextModel(AIModel):
    """
    Whisper-small for automatic speech recognition.

    Reference:
    - https://huggingface.co/openai/whisper-small
    - Radford et al.,(2022) “Robust Speech Recognition via Large-Scale Weak Supervision”
    """

    def __init__(self):
        self._asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")

    def run(self, file_path):
        return self._asr(file_path)["text"]
