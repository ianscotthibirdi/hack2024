import glob
import os
import time
from pathlib import Path

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def wait_for_files_active(files):
    """Waits for the given files to be active.

    Some files uploaded to the Gemini API need to be processed before they can be
    used as prompt inputs. The status can be seen by querying the file's "state"
    field.

    This implementation uses a simple blocking polling loop. Production code
    should probably employ a more sophisticated approach.
    """
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()


def list_files_in_folder(folder_path):
    folder = Path(folder_path)
    return [file for file in folder.iterdir() if file.is_file()]


def get_non_empty_string(strings):
    for string in strings:
        if string:
            return string
    return None
