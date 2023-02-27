from typing import Any, List, Optional
import torch
from pydantic import BaseModel
from models.pygmalion.parsing import parse_messages_from_str

from models.pygmalion.prompting import build_prompt_for
from .model import build_model_and_tokenizer_for, run_raw_inference

from time import perf_counter


class GenerationSettings(BaseModel):
    do_sample: Optional[bool] = True
    max_new_tokens: Optional[int] = 196
    temperature: Optional[float] = 0.5
    top_p: Optional[float] = 0.9
    top_k: Optional[int] = 0
    typical_p: Optional[float] = 1.0
    repetition_penalty: Optional[float] = 1.05
    penalty_alpha: Optional[float] = 0.6


class PygmalionRequest(BaseModel):
    history: List[str]
    user_message: str
    char_name: str
    char_persona: str
    example_dialogue: str
    world_scenario: str
    generation_settings: Optional[GenerationSettings] = GenerationSettings()


class PygmalionResponse(BaseModel):
    bot_message: str
    device_name: str
    vram: int
    model_name: str
    request: PygmalionRequest
    elapsed_time: float


class PygmalionProxy:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model, self.tokenizer = build_model_and_tokenizer_for(self.model_name)
        device_info = torch.cuda.get_device_properties(torch.cuda.device)
        self.device_name = device_info.name
        self.vram = device_info.total_memory

    def get_greeting(self, request: PygmalionRequest):
        start_time = perf_counter()
        bot_message = f"{request.char_name}: {request.char_greeting}"
        return PygmalionResponse(
            bot_message=bot_message,
            device_name=self.hardware,
            model_name=self.model_name,
            elapsed_time=perf_counter() - start_time,
        )

    def generate(self, request: PygmalionRequest):
        start_time = perf_counter()
        prompt = build_prompt_for(
            history=request.history,
            user_message=request.user_message,
            char_name=request.char_name,
            char_persona=request.char_persona,
            example_dialogue=request.example_dialogue,
            world_scenario=request.world_scenario,
        )

        model_output = run_raw_inference(
            self.model,
            self.tokenizer,
            prompt=prompt,
            user_message=request.user_message,
            **request.generation_settings.dict(),
        )

        generated_message = parse_messages_from_str(
            model_output, ["You", request.char_name]
        )
        bot_message = generated_message[0]
        elapsed_time = perf_counter() - start_time

        response = PygmalionResponse(
            bot_message=bot_message,
            device_name=self.device_name,
            vram=self.vram,
            model_name=self.model_name,
            request=request,
            elapsed_time=elapsed_time,
        )

        return response
