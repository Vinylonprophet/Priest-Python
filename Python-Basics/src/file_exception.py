from pathlib import Path

path = Path("not_exist_file.txt")
try:
    contents = path.read_text(encoding="utf-8")
except FileNotFoundError:
    print(f"Sorry, file {path} doesn't exist")
