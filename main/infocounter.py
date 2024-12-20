import json
from typing import Literal

def adofai_jeongsanghwa(path: str):
    return path.replace(", }", " }").replace(",  }", " }")

def counter(path: str, mod: Literal["angleData", "actions", "decorations"]) -> str:
    with open(path, "r", encoding="utf-8-sig") as file:
        data: dict = json.loads(adofai_jeongsanghwa(file.read()))
    
    return len(data[mod])

if __name__ == "__main__":
    print(counter(r"E:\ADOFAI\맵\니가 해야할 거\Frums - gur yvsr(仮) (Why did you download this XD ver.)\level.adofai", "actions"))