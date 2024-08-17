import string, re
from difflib import Differ

README = """
    # Scalefocus AI Tools
    
    This app is a prototype effort to showcase various use cases with Large Language Models (LLMs) and inspire colleagues for potential product ideas.
    The app utilizes a flexible architecture that supports multiple AI providers,
    including OpenAI and self-hosted solutions, to perform language and speech tasks.

    ### Features
    - **Audio Recording**: Users can record their speech directly within the app using their device's microphone.
    - **Speech Transcription**: The app transcribes the recorded speech to text using the Whisper model.
    - **Text Improvement**: Utilizes various GPT models to refine the speech text, focusing on simplicity, brevity, and clarity.
    - **Difference Highlighting**: Displays the differences between the original and improved texts, with changes clearly marked for easy review.

    - **Speech Improvement**: Enhances the clarity and conciseness of speech transcripts.
    - **Text Summarization**: Provides summaries of text inputs at various levels of detail, adjustable by the user.
    - **Wisdom Extraction**: Extracts insightful or wise statements from the provided text.
    """

SEMANTIC_LEVELS = {
    1 :"Level 1: Single Sentence Summary",
    2 :"Level 2: High-Level Overview",
    3 :"Level 3: Twitter Post Summary (40-60 words)",
    4 :"Level 4: Executive Summary (80-100 words)",
    5 :"Level 5: Structured Summary (100-120 words, covering all main points and supporting arguments)"
}

def diff_texts(text1, text2):
    text1, text2 = remove_punctuation(text1), remove_punctuation(text2)
    
    d = Differ()
    return [
        (token[2:], token[0] if token[0] != " " else None)
        for token in d.compare(text1, text2)
    ]

def remove_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation))

def count_lines_and_words(text):
    lines = text.splitlines()
    num_lines = len(lines)
    num_words = sum(len(line.split()) for line in lines)
    return num_lines, num_words