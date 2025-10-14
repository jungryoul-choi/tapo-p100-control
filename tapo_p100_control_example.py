#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tapo P100 스마트 플러그 제어 기본 예제 스크립트
이 스크립트는 PyP100 라이브러리를 사용하여 Tapo P100 스마트 플러그를 제어하는 기본 예제를 제공합니다.
"""

from PyP100 import PyP100
import json

# 설정 정보
CONFIG = {
    "ip": "192.168.0.19",
    "email": "cjr1208@naver.com",
    "password": "onda123!"
}

def main():
    """기본 제어 기능 예제"""
    # 스마트 플러그 연결
    plug = PyP100.P100(CONFIG["ip"], CONFIG["email"], CONFIG["password"])
    
    # 인증
    print("장치와 인증 중...")
    plug.handshake()
    plug.login()
    print("인증 완료")
    
    # 상태 확인
    print("\n현재 상태 확인:")
    status = plug.getDeviceInfo()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # 전원 상태 출력
    is_on = status.get("device_on", False)
    print(f"전원 상태: {'켜짐' if is_on else '꺼짐'}")
    
    # 전원 켜기/끄기 (현재 상태의 반대로 설정)
    if is_on:
        print("\n전원 끄는 중...")
        plug.turnOff()
        print("전원이 꺼졌습니다.")
    else:
        print("\n전원 켜는 중...")
        plug.turnOn()
        print("전원이 켜졌습니다.")
    
    # 변경된 상태 확인
    print("\n변경된 상태 확인:")
    status = plug.getDeviceInfo()
    print(json.dumps(status, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
