#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tapo L510E 스마트 전구 제어 예제 스크립트
이 스크립트는 PyP100 라이브러리의 PyL530 클래스를 사용하여 Tapo L510E 스마트 전구를 제어합니다.
(라이브러리에 L510E 전용 클래스가 없어서 L530 클래스를 대신 사용)
기능: 전원 켜기/끄기, 밝기 조절, 색온도 조절
"""

from PyP100 import PyL530  # PyL510E 대신 PyL530 사용 (Tapo L5xx 시리즈 전구용)
import json
import argparse
import sys
from datetime import datetime

# 설정 정보
CONFIG = {
    "ip": "192.168.0.20",     # L510E 전구의 IP 주소 (실제 IP로 변경해주세요)
    "email": "cjr1208@naver.com",
    "password": "onda123!"
}

def connect_bulb():
    """스마트 전구 연결 및 로그인"""
    try:
        # 스마트 전구 연결 객체 생성
        bulb = PyL530.L530(CONFIG["ip"], CONFIG["email"], CONFIG["password"])
        
        # 로그인 및 인증
        print("전구와 연결 중...")
        bulb.handshake()
        bulb.login()
        print("연결 성공!")
        return bulb
    except Exception as e:
        print(f"연결 오류: {e}", file=sys.stderr)
        return None

def get_status(bulb=None):
    """스마트 전구 상태 확인"""
    if not bulb:
        bulb = connect_bulb()
    if not bulb:
        return {"error": "전구 연결 실패"}
    
    try:
        # 상태 정보 가져오기
        status = bulb.getDeviceInfo()
        
        # 상태 정보에 현재 시간 추가
        status["timestamp"] = datetime.now().isoformat()
        
        return status
    except Exception as e:
        print(f"상태 확인 오류: {e}", file=sys.stderr)
        return {"error": str(e)}

def turn_on(bulb=None):
    """스마트 전구 전원 켜기"""
    if not bulb:
        bulb = connect_bulb()
    if not bulb:
        return {"error": "전구 연결 실패"}
    
    try:
        # 전원 켜기
        bulb.turnOn()
        print("전구가 켜졌습니다.")
        
        # 성공 응답 반환
        return {
            "success": True,
            "action": "turnOn",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"전원 켜기 오류: {e}", file=sys.stderr)
        return {"error": str(e)}

def turn_off(bulb=None):
    """스마트 전구 전원 끄기"""
    if not bulb:
        bulb = connect_bulb()
    if not bulb:
        return {"error": "전구 연결 실패"}
    
    try:
        # 전원 끄기
        bulb.turnOff()
        print("전구가 꺼졌습니다.")
        
        # 성공 응답 반환
        return {
            "success": True,
            "action": "turnOff",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"전원 끄기 오류: {e}", file=sys.stderr)
        return {"error": str(e)}

def set_brightness(brightness, bulb=None):
    """
    스마트 전구 밝기 조절
    brightness: 1-100 사이의 값 (백분율)
    """
    if not 1 <= brightness <= 100:
        print("밝기는 1-100 사이의 값이어야 합니다.", file=sys.stderr)
        return {"error": "잘못된 밝기 값"}
    
    if not bulb:
        bulb = connect_bulb()
    if not bulb:
        return {"error": "전구 연결 실패"}
    
    try:
        # 밝기 설정
        bulb.setBrightness(brightness)
        print(f"전구 밝기가 {brightness}%로 설정되었습니다.")
        
        # 성공 응답 반환
        return {
            "success": True,
            "action": "setBrightness",
            "brightness": brightness,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"밝기 설정 오류: {e}", file=sys.stderr)
        return {"error": str(e)}

def set_color_temp(color_temp, bulb=None):
    """
    스마트 전구 색온도 조절
    color_temp: 2500-6500 사이의 값 (켈빈)
    2500K: 따뜻한 노란빛 (전구색)
    6500K: 차가운 하얀빛 (주광색)
    """
    if not 2500 <= color_temp <= 6500:
        print("색온도는 2500-6500K 사이의 값이어야 합니다.", file=sys.stderr)
        return {"error": "잘못된 색온도 값"}
    
    if not bulb:
        bulb = connect_bulb()
    if not bulb:
        return {"error": "전구 연결 실패"}
    
    try:
        # 색온도 설정
        bulb.setColorTemp(color_temp)
        print(f"전구 색온도가 {color_temp}K로 설정되었습니다.")
        
        # 성공 응답 반환
        return {
            "success": True,
            "action": "setColorTemp",
            "colorTemp": color_temp,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"색온도 설정 오류: {e}", file=sys.stderr)
        return {"error": str(e)}

def set_color(hue, saturation, bulb=None):
    """
    스마트 전구 색상 설정 (L530 전구용, L510E는 지원하지 않음)
    hue: 0-360 사이의 값 (색조)
    saturation: 0-100 사이의 값 (채도)
    """
    if not 0 <= hue <= 360:
        print("색조(hue)는 0-360 사이의 값이어야 합니다.", file=sys.stderr)
        return {"error": "잘못된 색조 값"}
    
    if not 0 <= saturation <= 100:
        print("채도(saturation)는 0-100 사이의 값이어야 합니다.", file=sys.stderr)
        return {"error": "잘못된 채도 값"}
    
    if not bulb:
        bulb = connect_bulb()
    if not bulb:
        return {"error": "전구 연결 실패"}
    
    try:
        # 색상 설정 (L530 전구용)
        bulb.setColor(hue, saturation)
        print(f"전구 색상이 설정되었습니다. (색조: {hue}, 채도: {saturation})")
        print("참고: 이 기능은 L530 전구에서만 작동하며 L510E에서는 지원되지 않습니다.")
        
        # 성공 응답 반환
        return {
            "success": True,
            "action": "setColor",
            "hue": hue,
            "saturation": saturation,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"색상 설정 오류: {e}", file=sys.stderr)
        return {"error": str(e)}

def main():
    """명령행 인터페이스: 인자 파싱 및 해당 기능 실행"""
    parser = argparse.ArgumentParser(description="Tapo L510E 스마트 전구 제어")
    
    # 명령 하위 파서 설정
    subparsers = parser.add_subparsers(dest="command", help="실행할 명령")
    
    # 상태 확인 명령
    status_parser = subparsers.add_parser("status", help="전구 상태 확인")
    
    # 전원 켜기 명령
    on_parser = subparsers.add_parser("on", help="전구 전원 켜기")
    
    # 전원 끄기 명령
    off_parser = subparsers.add_parser("off", help="전구 전원 끄기")
    
    # 밝기 설정 명령
    brightness_parser = subparsers.add_parser("brightness", help="전구 밝기 설정")
    brightness_parser.add_argument("level", type=int, help="밝기 수준 (1-100)")
    
    # 색온도 설정 명령
    colortemp_parser = subparsers.add_parser("colortemp", help="전구 색온도 설정")
    colortemp_parser.add_argument("temp", type=int, help="색온도 (2500-6500K)")
    
    # 색상 설정 명령 (L530 전구용)
    color_parser = subparsers.add_parser("color", help="전구 색상 설정 (L530 전구 전용)")
    color_parser.add_argument("hue", type=int, help="색조 (0-360)")
    color_parser.add_argument("saturation", type=int, help="채도 (0-100)")
    
    # 인자 파싱
    args = parser.parse_args()
    
    # 전구 연결
    bulb = connect_bulb()
    if not bulb:
        sys.exit(1)
    
    # 명령 실행
    if args.command == "status":
        result = get_status(bulb)
    elif args.command == "on":
        result = turn_on(bulb)
    elif args.command == "off":
        result = turn_off(bulb)
    elif args.command == "brightness":
        result = set_brightness(args.level, bulb)
    elif args.command == "colortemp":
        result = set_color_temp(args.temp, bulb)
    elif args.command == "color":
        result = set_color(args.hue, args.saturation, bulb)
    else:
        parser.print_help()
        sys.exit(0)
    
    # 결과 출력
    print("\n결과:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

def interactive_demo():
    """대화형 데모: 모든 기능을 차례로 테스트"""
    print("=== Tapo L510E 스마트 전구 대화형 데모 ===")
    print("(PyL530 라이브러리를 사용하여 L510E 전구 제어)")
    
    # 전구 연결
    bulb = connect_bulb()
    if not bulb:
        sys.exit(1)
    
    # 초기 상태 확인
    print("\n1. 초기 상태 확인:")
    status = get_status(bulb)
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # 전원 켜기
    print("\n2. 전구 전원 켜기:")
    turn_on(bulb)
    
    # 밝기 변경 테스트
    print("\n3. 밝기 변경 테스트:")
    
    # 밝기 25%
    print("\n  3.1 밝기를 25%로 설정:")
    set_brightness(25, bulb)
    
    # 잠시 대기
    input("  계속하려면 Enter 키를 누르세요...")
    
    # 밝기 100%
    print("\n  3.2 밝기를 100%로 설정:")
    set_brightness(100, bulb)
    
    # 잠시 대기
    input("  계속하려면 Enter 키를 누르세요...")
    
    # 색온도 변경 테스트
    print("\n4. 색온도 변경 테스트:")
    
    # 따뜻한 색온도 (2700K)
    print("\n  4.1 따뜻한 색온도(2700K)로 설정:")
    set_color_temp(2700, bulb)
    
    # 잠시 대기
    input("  계속하려면 Enter 키를 누르세요...")
    
    # 중간 색온도 (4000K)
    print("\n  4.2 중간 색온도(4000K)로 설정:")
    set_color_temp(4000, bulb)
    
    # 잠시 대기
    input("  계속하려면 Enter 키를 누르세요...")
    
    # 차가운 색온도 (6500K)
    print("\n  4.3 차가운 색온도(6500K)로 설정:")
    set_color_temp(6500, bulb)
    
    # 잠시 대기
    input("  계속하려면 Enter 키를 누르세요...")
    
    # 색상 변경 테스트 (L530 전구 전용)
    print("\n5. 색상 변경 테스트 (L530 전구 전용):")
    print("   주의: 이 기능은 L510E 전구에서는 작동하지 않습니다.")
    print("   L530과 같은 컬러 전구에서만 작동합니다.")
    
    test_color = input("  L530 컬러 전구를 사용하고 계신가요? (y/n): ")
    if test_color.lower() == 'y':
        # 빨간색 (0, 100)
        print("\n  5.1 빨간색으로 설정:")
        set_color(0, 100, bulb)
        
        # 잠시 대기
        input("  계속하려면 Enter 키를 누르세요...")
        
        # 초록색 (120, 100)
        print("\n  5.2 초록색으로 설정:")
        set_color(120, 100, bulb)
        
        # 잠시 대기
        input("  계속하려면 Enter 키를 누르세요...")
        
        # 파란색 (240, 100)
        print("\n  5.3 파란색으로 설정:")
        set_color(240, 100, bulb)
        
        # 잠시 대기
        input("  계속하려면 Enter 키를 누르세요...")
    
    # 최종 상태 확인
    print("\n6. 최종 상태 확인:")
    status = get_status(bulb)
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # 전원 끄기
    print("\n7. 전구 전원 끄기:")
    turn_off(bulb)
    
    print("\n=== 데모 완료 ===")

if __name__ == "__main__":
    # 인자가 없으면 대화형 데모 실행, 있으면 명령행 인터페이스 실행
    if len(sys.argv) == 1:
        interactive_demo()
    else:
        main()
