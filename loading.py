import time
from tqdm import tqdm

def pro_bar():
    for i in tqdm(range(100), desc="Loading", leave=False):
        time.sleep(0.1)
    print("""
< Data Fetched Successfully! >
 -------------------------
    \   ^__^
     \  (oo)\_______
        (__)\       )\/\\
            ||----w |
            ||     ||
""")