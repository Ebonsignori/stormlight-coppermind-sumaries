# From https://coppermind.net/wiki/The_Stormlight_Archive/Summary
coppermind_url_mappings = {
    "The Way of Kings": "https://coppermind.net/wiki/Summary:The_Way_of_Kings",
    "Words of Radiance": "https://coppermind.net/wiki/Summary:Words_of_Radiance",
    "Edgedancer": "https://coppermind.net/wiki/Summary:Edgedancer",
    "Oathbringer": "https://coppermind.net/wiki/Summary:Oathbringer",
    "Dawnshard": "https://coppermind.net/wiki/Summary:Dawnshard",
    "Rhythm of War": "https://coppermind.net/wiki/Summary:Rhythm_of_War"
}

# Voice options for Open AI's Text-To-Speech API
# https://platform.openai.com/docs/guides/text-to-speech/voice-options
character_to_openai_voice_mapping = {
    "default": "alloy",
    # Male characters
    "adolin": "alloy",
    "dalinar": "onyx",
    "sadeas": "fable",
    "elhokar": "fable",
    "renarin": "fable",
    "kaladin": "echo",
    "gavilar": "onyx",
    "teft": "onyx",
    "rock": "onyx",
    "lupin": "fable",
    "szeth": "fable",
    # Female characters
    "shallan": "nova",
    "jasnah": "shimmer",
    "navani": "shimmer",
    "lift": "nova",
    "rysn": "shimmer",
    "eshonai": "shimmer",
    "venli": "nova",
}

vits_voice_mapping = {
    "male_1": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p226"
    },
    "male_2": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p231"
    },
    "male_3": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p236"
    },
    "male_4": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p251"
    },
    "male_5": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p234"
    },
    "male_6": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p228"
    },
    "male_7": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p229"
    },
    "male_8": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p230"
    },
    "female_1": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p243"
    },
    "female_2": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p248"
    },
    "female_3": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p225"
    },
    "female_4": {
        "model": "tts_models/en/vctk/vits",
        "speaker": "p227"
    },
}

openai_to_vits_voice_mapping = {
  "alloy": vits_voice_mapping.get("male_1"),
  "echo": vits_voice_mapping.get("male_2"),
  "fable": vits_voice_mapping.get("male_4"),
  "onyx": vits_voice_mapping.get("male_5"),
  "nova": vits_voice_mapping.get("female_1"),
  "shimmer": vits_voice_mapping.get("female_2"),
}


def get_coppermind_url_map():
  global coppermind_url_mappings
  return coppermind_url_mappings

def get_character_to_openai_voice_map():
  global character_to_openai_voice_mapping
  return character_to_openai_voice_mapping

def get_openai_to_vits_voice_map():
  global openai_to_vits_voice_mapping
  return openai_to_vits_voice_mapping