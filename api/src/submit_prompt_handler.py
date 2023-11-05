import json
from dataclasses import dataclass, asdict


@dataclass
class Request:
    game_id: str
    prompt: str


@dataclass
class Response:
    game_id: str
    image_url: str


def handle_submit_prompt(req: Request) -> Response:
    resp = Response(req.game_id, "imageurl")
    return resp


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        body["game_id"] = event["pathParameters"]["game_id"]
        req = Request(**body)
        resp = handle_submit_prompt(req)
        return {"statusCode": 200, "body": asdict(resp)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
