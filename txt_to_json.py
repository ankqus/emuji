import json
import os
import re
import requests
import time
# import shutil
# import threading

version = "15.0"

# stop_dancing_text = False

# def dancing_text(text):
# global stop_dancing_text
# while not stop_dancing_text:
# for i in range(len(text)):
# if stop_dancing_text:
# break
# columns, rows = shutil.get_terminal_size()
# center = (columns - len(text)) // 2
# print(
#   "\033[s" + " " * center + text[:i] + text[i].upper() +
#   text[i + 1:].lower() + "\033[u",
#   end="\r",
#   flush=True,
# )
# time.sleep(0.5)
# print("\033[s" + "Fetching complete." + "\033[u")


def main():
    text = get_test_file(version)
    print("[FETCHED]")
    print()
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
        # elif line.startswith("#"):
        # accu["comments"] += line + "\n"
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
    print(f"\nProcessed emujis: {len(accu['full'])}")
    print(f"Version: (v{version})")
    print("O/P file: emuji.json, emuji-only.json\n")
    write_files(accu)


def print_progress_bar(
    iteration, total, prefix="", suffix="", decimals=1, length=50, fill="█"
):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end="\r")
    if iteration == total:
        print()


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

    for i in range(61):
        print_progress_bar(i, 60)
        time.sleep(0.2)
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
    with open(os.path.join("emuji.json"), "w", encoding="utf-8") as f:
        json.dump(collected["full"], f, ensure_ascii=False, indent=2)
    with open(os.path.join("emuji-only.json"), "w", encoding="utf-8") as f:
        json.dump(collected["compact"], f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
