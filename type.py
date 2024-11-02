from typing import Dict

Character = Dict[str, int]
Scene = Dict[str, str]
Actor = Dict[str, int]
Stage = Dict[str, str]

HEADER_SCENES = {
    "SceneName": "SceneName",
    "Lines": "Lines",
    "Didascalies": "Didascalies",
    "Words": "Words",
    "Characters": "Characters"}

HEADER_CHARACTERS = {
    "CharacterName": "CharacterName",
    "Lines": "Lines",
    "Words": "Words",
}

HEADER_ACTORS = {
    "ActorName": "ActorName",
    "CharactersPlayed": "CharactersPlayed"
}