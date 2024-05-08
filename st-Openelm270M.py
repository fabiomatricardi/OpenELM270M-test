#
# For licensing see accompanying LICENSE file.
# Copyright (C) 2024 Apple Inc. All Rights Reserved.
# https://huggingface.co/docs/transformers/main/en/internal/generation_utils#transformers.TextStreamer.on_finalized_text
# TextStreamer KWargs: https://huggingface.co/docs/transformers/main/en/internal/generation_utils#transformers.TextIteratorStreamer
#
import streamlit as st
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from threading import Thread
# Internal usage
from time import sleep


if "hf_model" not in st.session_state:
    st.session_state.hf_model = "OpenELM_270M"
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


@st.cache_resource
def create_client():   
    mydevice = 'cpu'
    checkpoint_path = 'model270/'
    #Load the Model
    model = AutoModelForCausalLM.from_pretrained(checkpoint_path,
                                                trust_remote_code=True)
    model.to(mydevice).eval()
    #Load the Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
    return model, tokenizer

# FUNCTION TO LOG ALL CHAT MESSAGES INTO chathistory.txt
def writehistory(text):
    with open('chathistoryOpenELM270M.txt', 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')
    f.close()

#AVATARS
av_us = 'user.png'  # './man.png'  #"🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". Shortcodes are not supported.
av_ass = 'applelogo.jpg'   #
# Set a default model


### START STREAMLIT UI
st.image('LogoOpenELM270-instruct.png', )
st.markdown("### *powered by Streamlit & HF Transformers*", unsafe_allow_html=True )
#st.subheader(f"Free ChatBot using {st.session_state.hf_model}")
st.markdown('---')

model, tokenizer = create_client()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar=av_us):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar=av_ass):
            st.markdown(message["content"])
# Accept user input
if myprompt := st.chat_input("What is an AI model?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": myprompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar=av_us):
        st.markdown(myprompt)
        usertext = f"🧑‍💻 user: {myprompt}"
        writehistory(usertext)
        # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=av_ass):
        message_placeholder = st.empty()
        full_response = ""
        tokenized_prompt = tokenizer([myprompt],return_tensors='pt')
        streamer = TextIteratorStreamer(tokenizer,skip_prompt=True)
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
            message_placeholder.markdown(generated_text+ "▌")
        generation_time = time.time() - stime
        message_placeholder.markdown(generated_text)
        asstext = f"🤖 assistant: {generated_text}"
        writehistory(asstext)       
        st.session_state.messages.append({"role": "assistant", "content": generated_text})