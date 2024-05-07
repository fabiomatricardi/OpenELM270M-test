# OpenELM270M-test
Repo of the code from the Medium article

This model does not have an offiial Transformers pipeline, as far as  I know.

The model weights are in the official Apple Repository, but this model uses the Llama2 tokenizer

so...

Create a Virtual Environment, activate it and install huggingFace CLI 
```
python -m venv venv
venv\Scripts\activate

pip install -U huggingface_hub[cli]
```


Get your HuggingFace Access token from  https://huggingface.co/settings/tokens

In the terminal run
```
huggingface-cli login
```

and paste your HF token (should be something lilke hf_xxxxxxxxxxxxxxxxxxxxx)

Use the CLI commands to download the model files and tokenizer into `model270` directory

```
huggingface-cli download apple/OpenELM-270M-Instruct --local-dir model270
huggingface-cli download meta-llama/Llama-2-7b-hf --include "*token*" --local-dir model270
```


Now install the required packages

```
pip install transformers==4.40.2 streamlit==1.24.0 torch torchvision torchaudio
```

and download my special python file

```
wget https://github.com/fabiomatricardi/OpenELM270M-test/raw/main/OpenELM270.py -OutFile OpenELM270.py
```

---

If you want to do it manually...

Download in the `model` sub-folder the following files:

from the official [apple/OpenELM-270M-Instruct Repo](https://huggingface.co/apple/OpenELM-270M-Instruct/tree/main) download all the files
```
config.json
configuration_openelm.py
generate_openelm.py
generation_config.json
LICENSE
model.safetensors
modeling_openelm.py
README.md
```

from the Official Llama2 Repo [meta-llama/Llama-2-7b-hf](https://huggingface.co/meta-llama/Llama-2-7b-hf/tree/main)
> download the Tokenizer files
```
special_tokens_map.json
tokenizer.json
tokenizer.model
tokenizer_config.json  
```

---

### Extra bonus
If you want to test also the 450M anad the 1.1B parameters model, here how to download the weights and tokenizer
```
huggingface-cli download meta-llama/Llama-2-7b-hf --include "*token*" --local-dir model450
huggingface-cli download apple/OpenELM-450M-Instruct --local-dir model450

huggingface-cli download meta-llama/Llama-2-7b-hf --include "*token*" --local-dir model1B
huggingface-cli download apple/OpenELM-1_1B-Instruct --local-dir model1B
```

And here the files to use in python
> python OpenELM1B.py

or

> python OpenELM450.py
