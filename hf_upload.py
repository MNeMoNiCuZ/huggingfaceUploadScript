import os
import json
import shutil
import time
from huggingface_hub import HfApi, HfFolder

# Set up your Hugging Face access token
HUGGINGFACE_TOKEN = 'hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

api = HfApi()

# List of models to upload and their data
model_info = [
    {
        'model_path': r'C:\Path\To\My\Model\AbstractPatternStyle.safetensors',
        'base_model': 'SD1.5',
        'repo_name': 'AbstractPatternStyle-SD1.5-LoRA',
        'pretty_name': 'AbstractPatternStyle - SD1.5 - LoRA',
        'information': 'Creates beautiful abstract patterns.'
    },
    {
        'model_path': r'C:\Path\To\My\Model\HornyfierXL.safetensors',
        'base_model': 'SDXL',
        'repo_name': 'HornyfierXL-SDXL-LoRA',
        'pretty_name': 'HornyfierXL - SDXL - LoRA',
        'information': 'Adds horns to anything.'
    },
    {
        'model_path': r'C:\Path\To\My\Model\CardboardStylePony.safetensors',
        'base_model': 'PDXL',
        'repo_name': 'CardboardStyle-PDXL-LoRA',
        'pretty_name': 'CardboardStyle - PDXL - LoRA',
        'information': 'Things are now made out of cardboard!'
    }
]

# Define the base model mapping
base_model_mapping = {
    'SD1.5': 'runwayml/stable-diffusion-v1-5',
    'SDXL': 'stabilityai/stable-diffusion-xl-base-1.0',
    'PDXL': 'AstraliteHeart/pony-diffusion-v6',
    'SD3': 'stabilityai/stable-diffusion-3-medium'
}

def read_metadata(metadata_path):
    with open(metadata_path, 'r') as file:
        return json.load(file)

def create_hf_repo(repo_name, repo_description):
    namespace = api.whoami(token=HUGGINGFACE_TOKEN)['name']
    repo_id = f"{namespace}/{repo_name}"
    
    # Check if the repo already exists
    try:
        api.create_repo(repo_id, repo_type="model", private=False, token=HUGGINGFACE_TOKEN)
    except Exception as e:
        if "409" in str(e):
            print(f"Repository {repo_name} already exists. Using the existing repository.")
        else:
            raise e
    return repo_id

def create_readme(metadata, base_model, pretty_name, information, image_url=None):
    base_model_id = base_model_mapping.get(base_model, base_model)
    yaml_metadata = (
        "---\n"
        "license: gpl-3.0\n"
        f"base_model: {base_model_id}\n"
        f"trained_words: {', '.join(metadata.get('trainedWords', []))}\n"
        "---\n\n"
    )
    readme_content = yaml_metadata
    readme_content += f"# {pretty_name}\n\n"
    if 'modelId' in metadata:
        readme_content += f"[CivitAI Page](https://civitai.com/models/{metadata['modelId']})\n\n"
    
    if metadata.get('trainedWords', []):
        readme_content += "## Trigger Words\n**"
        readme_content += ", ".join(metadata.get('trainedWords', [])) + "**\n\n"
    
    if image_url:
        readme_content += f"![Model Preview]({image_url})\n\n"
    
    if information:
        readme_content += f"{information}\n\n"
    
    return readme_content

def upload_to_hf(model_info):
    model_path = model_info['model_path']
    base_model = model_info['base_model']
    repo_name = model_info['repo_name']
    pretty_name = model_info['pretty_name']
    information = model_info['information']
    
    metadata_path = model_path.replace('.safetensors', '.civitai.info')
    metadata = read_metadata(metadata_path)
    repo_description = metadata.get('description', 'No description provided.')
    
    repo_id = create_hf_repo(repo_name, repo_description)
    
    # Create a temporary directory for the repo
    temp_dir = os.path.join(os.getcwd(), repo_name.replace(' ', '_'))
    os.makedirs(temp_dir, exist_ok=True)
    
    # Copy the model and metadata to the repo directory
    shutil.copy(model_path, temp_dir)
    shutil.copy(metadata_path, temp_dir)
    
    # Check for and include the image
    image_path = model_path.replace('.safetensors', '.preview.png')
    image_url = None
    if os.path.exists(image_path):
        shutil.copy(image_path, temp_dir)
        image_url = f"https://huggingface.co/{repo_id}/raw/main/{os.path.basename(image_path)}"
    
    # Create README.md file
    readme_content = create_readme(metadata, base_model, pretty_name, information, image_url)
    readme_path = os.path.join(temp_dir, 'README.md')
    with open(readme_path, 'w') as readme_file:
        readme_file.write(readme_content)
    
    # Upload files to the repository
    api.upload_folder(repo_id=repo_id, folder_path=temp_dir, path_in_repo=".", token=HUGGINGFACE_TOKEN)

    # Clean up
    time.sleep(2)  # Delay to ensure all operations are complete before deletion
    shutil.rmtree(temp_dir)

for info in model_info:
    upload_to_hf(info)