# Huggingface Upload Script
## What is this?
This is a small script to help you batch upload your models like LoRAs or whatever to HuggingFace.

## How to use
1. Create your own HF access token: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. With the following permissions: **Fine-grained (custom)**
3. Allow the `Read access to all collections under your personal namespace` setting
4. Allow the `Write access to all collections under your personal namespace` setting
5. Enter your token in the script, or environment variable before running the script, or otherwise sign in to HuggingFace in the CLI where you are running the script.
6. Edit the `model_info` list with the local path to your model, the base model (follow the base model list below for linking to base models), as well as a repo-name, a pretty-name and any information you would like to add.
7. Make sure that you have the `.preview.png` and the `.civitai.info` file with the same name as your model, in the same directory, for the script to work.
8. Run the script, and it should create and upload the files for you.

![image](https://github.com/MNeMoNiCuZ/huggingfaceUploadScript/assets/60541708/1a48b863-82c1-4f5b-b367-725790a62c4b)


## How do I get the .preview.png and .civitai.info files?
[https://github.com/zixaphir/Stable-Diffusion-Webui-Civitai-Helper](https://github.com/zixaphir/Stable-Diffusion-Webui-Civitai-Helper)

Use this extension in A1111 and press the `Scan`-button to download it all from CivitAI automatically.
