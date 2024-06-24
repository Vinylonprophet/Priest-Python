from pathlib import Path

content = "U love programming.\n"
content += "No, I don't love programming!\n"
content += "No, U really love programming!!!\n"


path = Path("programming.txt")
path.write_text(content)
