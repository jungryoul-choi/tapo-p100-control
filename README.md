# Tapo P100 스마트 플러그 웹 컨트롤러

이 웹 애플리케이션은 Tapo P100 스마트 플러그를 웹 인터페이스를 통해 손쉽게 제어할 수 있게 해주는 도구입니다.

## 소개

이 프로젝트는 Node.js 백엔드와 HTML/JavaScript 프론트엔드를 사용하여 TP-Link Tapo P100 스마트 플러그를 제어합니다.
하나의 통합 Python 스크립트(`tapo_control.py`)를 통해 스마트 플러그를 효율적으로 제어합니다.

## 특징

- 웹 브라우저를 통한 간편한 제어
- 전원 켜기/끄기 기능
- 장치 상태 확인
- 통합 Python 스크립트를 통한 효율적인 제어
- 오류 처리 및 상태 모니터링

## 설치 및 실행 방법

### 사전 요구사항

1. **Node.js 및 npm**: [Node.js 웹사이트](https://nodejs.org/)에서 최신 LTS 버전을 설치하세요.
2. **Python**: [Python 웹사이트](https://www.python.org/downloads/)에서 Python 3.x를 설치하세요.
3. **PyP100 라이브러리**: 다음 명령어로 설치하세요.
   ```
   pip install PyP100
   ```

   또는 최신 펌웨어와의 호환성 문제가 발생할 경우 (KeyError: 'result' 오류 발생 시), 커뮤니티에서 유지 관리하는 업데이트된 버전을 설치하세요:
   ```
   pip install git+https://github.com/almottier/TapoP100.git@main
   ```

   > **참고**: Tapo는 주기적으로 장치 펌웨어를 업데이트하는데, 이로 인해 기존 PyP100 라이브러리와의 호환성이 깨질 수 있습니다. 펌웨어 업데이트로 인해 로그인 응답 형식이 변경되어 라이브러리의 토큰 추출 시도가 실패할 수 있습니다.

### 설치 과정

1. 저장소 클론 또는 다운로드:
   ```
   git clone https://github.com/yourusername/tapo-web-controller.git
   cd tapo-web-controller
   ```

2. 필요한 Node.js 패키지 설치:
   ```
   npm install
   ```

3. 설정 정보 수정:
   `tapo-controller.js` 파일에서 다음 정보를 수정하세요:
   - `ipAddress`: 스마트 플러그의 IP 주소
   - `email`: TP-Link 계정 이메일
   - `password`: TP-Link 계정 비밀번호

4. Python 스크립트 설정 정보도 같이 수정:
   `tapo_control.py` 파일의 CONFIG 객체


### 실행 방법

애플리케이션을 시작하려면:
```
npm start
```

웹 브라우저에서 `http://localhost:3001`으로 접속하세요.

---

### 파이썬 예제 파일 단독 실행

`tapo_p100_control_example.py` 파일은 단독 실행이 가능한 파이썬 예제 파일입니다. 이 파일을 직접 실행하여 Tapo P100 플러그 제어 예제를 테스트할 수 있습니다.

실행 방법:
```
python tapo_p100_control_example.py
```

## API 엔드포인트

- `POST /turnOn`: 플러그 전원 켜기
- `POST /turnOff`: 플러그 전원 끄기
- `GET /status`: 플러그 상태 확인

## 주의사항

- 장치와 컴퓨터가 같은 네트워크에 있어야 합니다.
- 보안을 위해 운영 환경에서는 환경 변수를 사용하여 계정 정보를 관리하세요.
- 공용 네트워크에서는 HTTPS를 사용하여 통신을 암호화하세요.

## 문제 해결

### KeyError: 'result' 오류

```
File "c:\DevEnv\Python313\Lib\site-packages\PyP100\PyP100.py", line 168, in login
    self.token = ast.literal_eval(decryptedResponse)["result"]["token"]
KeyError: 'result'
```

이 오류가 발생하는 경우, 펌웨어 업데이트로 인해 API 응답 형식이 변경되었을 가능성이 높습니다. 다음 해결 방법을 시도해보세요:

1. 업데이트된 버전의 라이브러리 설치:
   ```
   pip install git+https://github.com/almottier/TapoP100.git@main
   ```

2. 설치 후 서버 재시작:
   ```
   npm start
   ```