'''프로그램이 재시작해야 할 필요가 있거나 PyInstaller에서 빌드될 때 조정해야할 값 등을 제어하는 모듈'''

import sys
import os
import subprocess

def resource_path(relative_path):
    '''PyInstaller 빌드 후 리소스 파일의 경로를 반환'''
    try:
        # PyInstaller 실행 환경에서 임시 디렉토리를 반환
        base_path = sys._MEIPASS
    except AttributeError:
        # 개발 환경에서는 현재 디렉토리를 반환
        return(relative_path)
    
    return os.path.join(base_path, relative_path)

# 재시작
def running_ide():
    return not hasattr(sys, 'frozen')  # exe로 빌드되면 frozen 속성이 생김

def restart():
    if running_ide():
        print("IDE에서 실행 중입니다. exit()로 종료합니다.")
        exit()  # IDE에서는 exit()로 종료
    else:
        print("EXE 파일로 실행 중입니다. 재시작합니다.")
        try:
            current_exe = sys.executable
            subprocess.Popen([current_exe])
            sys.exit(0)
        except Exception as e:
            print(f"프로그램 재시작 실패: {e}")