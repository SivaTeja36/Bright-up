import base64
from pathlib import Path
import random
import string
from app.utils.constants import (
    ATTACHMENT_FOLDER_NAME, 
    TEMPLATE_FOLDER_NAME
)


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def get_template_folder_path(schema: str) -> Path:
    return get_project_root() / TEMPLATE_FOLDER_NAME / schema


def get_attachments_folder_path(schema: str) -> Path:
    return get_project_root() / ATTACHMENT_FOLDER_NAME / schema


def get_randome_str(chars=string.ascii_letters, N=10):
    return "".join(random.choice(chars) for _ in range(N))


def get_original_str(base64Str: str):
    try:
        return base64.b64decode(base64Str.encode()).decode()
    except:
        raise Exception("Invalid base64 content")
