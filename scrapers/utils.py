from langdetect import detect, detect_langs

def detect_language(content):
    try:
        lang = detect(content)
        return lang
    except Exception as e:
        print(f"Language detection error: {e}")
        return 'unknown'
