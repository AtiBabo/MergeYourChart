import os
import sys
import json
from typing import Literal

def adofai_jeongsanghwa(path: str):
    return path.replace(", }", " }").replace(",  }", " }")

def resource_path(relative_path):
    """PyInstaller 빌드 후 리소스 파일의 경로를 반환"""
    try:
        # PyInstaller 실행 환경에서 임시 디렉토리를 반환
        base_path = sys._MEIPASS
    except AttributeError:
        # 개발 환경에서는 현재 디렉토리를 반환
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def counter(path: str, mod: Literal["angleData", "actions", "decorations"]) -> str:
    with open(resource_path(path), "r", encoding="utf-8-sig") as file:
        data: dict = json.loads(adofai_jeongsanghwa(file.read()))
    
    return len(data[mod])

if __name__ == "__main__":
    print(counter(r"E:\ADOFAI\맵\니가 해야할 거\Frums - gur yvsr(仮) (Why did you download this XD ver.)\level.adofai", "actions"))