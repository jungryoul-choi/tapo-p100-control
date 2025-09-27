#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tapo P100 스마트 플러그 통합 제어 스크립트
이 스크립트는 PyP100 라이브러리를 사용하여 Tapo P100 스마트 플러그를 제어합니다.
명령행 인수를 통해 on, off, status 등 다양한 기능을 수행할 수 있습니다.
"""

from PyP100 import PyP100
import json
import sys
import argparse
from datetime import datetime

# 설정 정보
CONFIG = {
    "ip": "192.168.219.108",
    "email": "cjr1208@naver.com",
    "password": "onda123!"
}

def connect_plug():
    """스마트 플러그 연결 및 로그인"""
    try:
        # 스마트 플러그 연결
        plug = PyP100.P100(CONFIG["ip"], CONFIG["email"], CONFIG["password"])
        
        # 로그인
        plug.handshake()
        plug.login()
        return plug
    except Exception as e:
        print(f"오류 발생: {e}", file=sys.stderr)
        return None

def get_status():
    """스마트 플러그 상태 확인"""
    plug = connect_plug()
    if not plug:
        return {"error": "장치 연결 실패"}
    
    try:
        # 상태 가져오기
        status = plug.getDeviceInfo()
        
        # 상태 정보에 현재 시간 추가
        status["timestamp"] = datetime.now().isoformat()
        
        return status
    except Exception as e:
        print(f"상태 확인 오류: {e}", file=sys.stderr)
        return {"error": str(e)}

def turn_on():
    """스마트 플러그 전원 켜기"""
    plug = connect_plug()
    if not plug:
        return {"error": "장치 연결 실패"}
    
    try:
        # 전원 켜기
        plug.turnOn()
        
        # 성공 응답 반환
        return {
            "success": True,
            "action": "turnOn",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"전원 켜기 오류: {e}", file=sys.stderr)
        return {"error": str(e)}

def turn_off():
    """스마트 플러그 전원 끄기"""
    plug = connect_plug()
    if not plug:
        return {"error": "장치 연결 실패"}
    
    try:
        # 전원 끄기
        plug.turnOff()
        
        # 성공 응답 반환
        return {
            "success": True,
            "action": "turnOff",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"전원 끄기 오류: {e}", file=sys.stderr)
        return {"error": str(e)}

def main():
    """메인 함수: 명령행 인자 파싱 및 해당 기능 실행"""
    parser = argparse.ArgumentParser(description="Tapo P100 스마트 플러그 제어")
    
    # 위치 인수 - 동작 지정 (on, off, status)
    parser.add_argument("action", choices=["on", "off", "status", "toggle"], 
                        help="수행할 동작: on(전원 켜기), off(전원 끄기), status(상태 확인), toggle(상태 전환)")
    
    # 선택적 인수 - 출력 포맷
    parser.add_argument("-c", "--compact", action="store_true", help="간결한 형식으로 출력")
    
    # 인자 파싱
    args = parser.parse_args()
    
    # 선택된 동작 수행
    if args.action == "status":
        result = get_status()
    elif args.action == "on":
        result = turn_on()
    elif args.action == "off":
        result = turn_off()
    elif args.action == "toggle":
        # 현재 상태 확인 후 반대로 설정
        status = get_status()
        if "device_on" in status:
            if status["device_on"]:
                result = turn_off()
            else:
                result = turn_on()
        else:
            result = {"error": "상태 확인 실패"}
    
    # 결과 출력
    if args.compact:
        # 간결한 형식
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)
        elif args.action == "status":
            print(f"Status: {'ON' if result.get('device_on') else 'OFF'}")
        else:
            print("Success")
    else:
        # JSON 형식
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()