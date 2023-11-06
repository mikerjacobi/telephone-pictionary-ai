import json
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger()


@dataclass
class SubmitPromptRequest:
    game_id: str
    prompt: str


@dataclass
class SubmitPromptResponse:
    game_id: str
    image_url: str


def handle_submit_prompt(req: SubmitPromptRequest) -> SubmitPromptResponse:
    resp = SubmitPromptResponse(req.game_id, "imageurl")
    return resp
