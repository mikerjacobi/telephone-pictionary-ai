import inspect
import json
import logging
import os
import time
import traceback
from dataclasses import asdict
from common import AppContext

import boto3
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from hello_world_handler import handle_hello_world
from submit_prompt_handler import handle_submit_prompt, SubmitPromptRequest
from openai import OpenAI


logging.basicConfig(level="INFO")
logger = logging.getLogger()
cors_config = CORSConfig(allow_origin="*", allow_headers=["*"])
app = APIGatewayRestResolver(cors=cors_config)

# dynamodb = boto3.client("dynamodb")
env = os.environ["TP_ENV"]
if env == "sandbox":
    # dynamodb_url = os.environ["TP_DYNAMODB_URL"]
    # dynamodb = boto3.client("dynamodb", endpoint_url=dynamodb_url)
    pass

ctx = AppContext(
    boto3.client("s3"),
    # dynamodb,
    OpenAI(),
    env,
    os.environ["TP_IMAGE_BUCKET_NAME"],
)


@app.get("/hello")
def get_hello():
    func = inspect.currentframe().f_code.co_name
    try:
        resp = handle_hello_world()
        logger.warning(f"successfully handled {func}")
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
        resp = handle_submit_prompt(ctx, req)
        logger.warning(f"successfully handled {func}. prompt: {req.prompt}")
        return asdict(resp), 200
    except Exception as e:
        logger.error(f"failed to handle {func}. {traceback.format_exc()}")
        return {"message": "Server Error"}, 500


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
