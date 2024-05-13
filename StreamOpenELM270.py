#
# For licensing see accompanying LICENSE file.
# Copyright (C) 2024 Apple Inc. All Rights Reserved.
# https://huggingface.co/docs/transformers/main/en/internal/generation_utils#transformers.TextStreamer.on_finalized_text
#

"""Module to generate OpenELM output given a model and an input prompt."""
#import os
#import logging
import time
#import argparse
#from typing import Optional, Union
import torch
 
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from threading import Thread


mydevice = 'cpu'
checkpoint_path = 'model270/'
#Load the Model
model = AutoModelForCausalLM.from_pretrained(checkpoint_path,
                                            trust_remote_code=True)
model.to(mydevice).eval()
#Load the Tokenizer
tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
# Prepare the prompt
prompt = input('> ')
tokenized_prompt = tokenizer([prompt],return_tensors='pt')
streamer = TextIteratorStreamer(tokenizer)

# Generate
stime = time.time()
generation_kwargs = dict(tokenized_prompt, streamer=streamer, max_new_tokens=450, 
                         pad_token_id=0,
                        repetition_penalty= 1.2, do_sample=True,temperature=0.1)
thread = Thread(target=model.generate, kwargs=generation_kwargs)
thread.start()
generated_text = ""
for new_text in streamer:
    generated_text += new_text
    print(new_text, end="", flush=True)

generation_time = time.time() - stime
print(f'generated in \033[1m\033[92m {round(generation_time, 2)} \033[0m seconds')
