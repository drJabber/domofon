from random import choice
from app.resources.strings import POSITIVE_OPEN_RESPONSES, POSITIVE_OPEN_RESPONSES_TTS

def get_positive_open_response_for_yd():
    return choice(POSITIVE_OPEN_RESPONSES)
    
def get_positive_open_tts_response_for_yd():
    return choice(POSITIVE_OPEN_RESPONSES_TTS)
