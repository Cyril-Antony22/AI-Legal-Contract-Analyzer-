"""
Module 1 - Contract Upload
----------------------------
Small helper functions for validating and saving the uploaded file.
"""

import os
import uuid
from config import Config


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_upload(file_storage):
    """
    Saves the uploaded file with a unique name (so two users uploading
    "contract.pdf" at the same time don't overwrite each other) and
    returns (unique_id, saved_path).
    """
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    unique_id = uuid.uuid4().hex
    saved_name = f"{unique_id}.{ext}"
    saved_path = os.path.join(Config.UPLOAD_FOLDER, saved_name)
    file_storage.save(saved_path)
    return unique_id, saved_path
