import inspect
import json
import logging
import os
import time
import traceback
from dataclasses import asdict

from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from hello_world_handler import handle_hello_world
from submit_prompt_handler import handle_submit_prompt, SubmitPromptRequest

logging.basicConfig(level="INFO")
logger = logging.getLogger()
cors_config = CORSConfig(allow_origin="*", allow_headers=["*"])
app = APIGatewayRestResolver(cors=cors_config)


@app.get("/hello")
def get_hello():
    func = inspect.currentframe().f_code.co_name
    try:
        resp = handle_hello_world()
        logger.info(f"successfully handled {func}")
        return asdict(resp), 200
    except Exception as e:
        logger.error(f"failed to handle {func}. {traceback.format_exc()}")
        return {"message": "Server Error"}, 500


@app.post("/game/<game_id>/prompt")
def post_game_prompt(game_id):
    func = inspect.currentframe().f_code.co_name
    try:
        request_data = json.loads(app.current_event.decoded_body)
        request_data["game_id"] = game_id
        req = SubmitPromptRequest(**request_data)
        resp = handle_submit_prompt(req)
        logger.info(f"successfully handled {func}")
        return asdict(resp), 200
    except Exception as e:
        logger.error(f"failed to handle {func}. {traceback.format_exc()}")
        return {"message": "Server Error"}, 500


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
