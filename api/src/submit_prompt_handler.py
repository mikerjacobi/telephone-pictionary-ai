from common import AppContext
import requests
import json
from dataclasses import dataclass, asdict
import logging
import openai
from io import BytesIO

logger = logging.getLogger()


@dataclass
class SubmitPromptRequest:
    game_id: str
    prompt: str


@dataclass
class SubmitPromptResponse:
    game_id: str
    image_url: str


def generate_image(ctx: AppContext, req: SubmitPromptRequest) -> bytes:
    response = ctx.openai.images.generate(
        model="dall-e-3",
        prompt=req.prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    image = requests.get(image_url)
    return BytesIO(image.content)


def store_image(ctx: AppContext, image: bytes) -> str:
    key = "test.jpg"
    ctx.s3.put_object(Bucket=ctx.image_bucket_name, Key=key, Body=image)
    presigned_url = ctx.s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": ctx.image_bucket_name, "Key": key},
        ExpiresIn=3600,
    )
    return presigned_url


def handle_submit_prompt(
    ctx: AppContext, req: SubmitPromptRequest
) -> SubmitPromptResponse:
    image = generate_image(ctx, req)
    presigned_url = store_image(ctx, image)
    resp = SubmitPromptResponse(req.game_id, presigned_url)
    return resp
