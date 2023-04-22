import json
import os
import re
import requests
import time
from loading import pro_bar

version = "15.0"

def main():
    start = time.time()
    text = get_test_file(version)
    end = time.time()
    time_taken = end - start
    # global stop_dancing_text
    # stop_dancing_text = True
    accu = {"comments": "", "full": [], "compact": []}
    lines = text.strip().split("\n")
    op_message = "{}"

    for line in lines:
        if line.startswith("# group: "):
            print(op_message.format(line[2:].title()))
            accu["group"] = line[9:]
        elif line.startswith("# subgroup: "):
            accu["sub-group"] = line[12:]
        else:
            meta = parse_line(line)
            if meta:
                #meta["category"] = f'{accu["group"]} ({accu["subgroup"]})'
                meta["group"] = accu["group"]
                meta["sub-group"] = accu["sub-group"]
                accu["full"].append(meta)
                accu["compact"].append(meta["char"])
            else:
                accu["comments"] = accu["comments"].strip() + "\n\n"
    print(f"\nProcessed emojis: {len(accu['full'])}")
    print(f"Version: (v{version})")
    print("O/P files: emoji.json, emoji-only.json")
    print(f"Total time taken: {time_taken:.2f} seconds\n")
    write_files(accu)

def get_test_file(ver):
    url = f"https://unicode.org/Public/emoji/{ver}/emoji-test.txt"

    response = requests.get(url)
    assert (
        response.status_code == 200
    ), f"Request failed with status {response.status_code}"

    text = response.text
    # dancing_text_thread = threading.Thread(target=dancing_text,
    # args=("Formatting Text to Json", ))
    # dancing_text_thread.daemon = True
    # dancing_text_thread.start()
    print()
    pro_bar()
    return text

def parse_line(line):
    data = re.split(r"\s+[;#] ", line.strip())

    if len(data) != 3:
        return None
    code, status, char_and_name = data
    match = re.match(r"^(\S+) E\d+\.\d+ (.+)$", char_and_name)

    if not match:
        return None
    char, name = match.groups()
    return {"name": name,"char": char, "code": code}

def write_files(collected):
    with open(os.path.join("emoji.json"), "w", encoding="utf-8") as f:
        json.dump(collected["full"], f, ensure_ascii=False, indent=2)
    with open(os.path.join("emoji-only.json"), "w", encoding="utf-8") as f:
        json.dump(collected["compact"], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()