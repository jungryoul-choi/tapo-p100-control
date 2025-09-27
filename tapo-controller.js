/**
 * Tapo P100 스마트 플러그 제어 모듈
 * 
 * 이 모듈은 Tapo P100 스마트 플러그를 제어하는 기능을 제공합니다.
 * Python 스크립트를 실행하여 장치를 제어합니다.
 */

const { exec } = require('child_process');

// 설정 (구성 정보)
const CONFIG = {
    ipAddress: '192.168.219.108',
    email: 'cjr1208@naver.com',
    password: 'onda123!',
    deviceMac: '28-87-BA-A8-9B-D4',
    deviceId: '80224DF05AAE2D913231A9A7364E7B1F1FDB7D96',
    pythonScript: 'd:\\Project\\TapoP100Control\\tapo-web-app\\tapo_control.py'
};

// 장치 상태 저장
let deviceState = {
    isOn: false,
    deviceInfo: null,
    lastUpdate: null
};

/**
 * Python 스크립트를 실행하는 헬퍼 함수
 * @param {string} action 수행할 동작 ('on', 'off', 'status')
 * @returns {Promise<string>} Python 스크립트 실행 결과
 */
function runPythonScript(action) {
    return new Promise((resolve, reject) => {
        exec(`python "${CONFIG.pythonScript}" ${action}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Python 실행 오류: ${error.message}`);
                reject(error);
                return;
            }
            if (stderr) {
                console.warn(`Python 경고: ${stderr}`);
            }
            resolve(stdout.trim());
        });
    });
}

/**
 * 플러그 전원 켜기
 * @returns {Promise<object>} 작업 결과
 */
async function turnOn() {
    try {
        console.log("Python 스크립트를 통해 장치 전원 켜는 중...");
        
        // Python 스크립트 방식으로 실행
        const pythonOutput = await runPythonScript('on');
        
        deviceState.isOn = true;
        deviceState.lastUpdate = new Date();
        
        console.log("Python 스크립트를 통해 장치 전원이 켜졌습니다.");
        return { success: true, method: 'python' };
    } catch (error) {
        console.error("장치 전원 켜기 실패:", error);
        throw new Error("장치 전원 켜기 실패: " + error.message);
    }
}

/**
 * 플러그 전원 끄기
 * @returns {Promise<object>} 작업 결과
 */
async function turnOff() {
    try {
        console.log("Python 스크립트를 통해 장치 전원 끄는 중...");
        
        // Python 스크립트 방식으로 실행
        const pythonOutput = await runPythonScript('off');
        
        deviceState.isOn = false;
        deviceState.lastUpdate = new Date();
        
        console.log("Python 스크립트를 통해 장치 전원이 꺼졌습니다.");
        return { success: true, method: 'python' };
    } catch (error) {
        console.error("장치 전원 끄기 실패:", error);
        throw new Error("장치 전원 끄기 실패: " + error.message);
    }
}

/**
 * 플러그 상태 확인
 * @returns {Promise<object>} 장치 상태 정보
 */
async function getDeviceInfo() {
    try {
        console.log("Python 스크립트를 통해 장치 상태 확인 중...");
        
        // Python 스크립트 실행
        const pythonOutput = await runPythonScript('status');
        
        try {
            // Python 스크립트 출력 파싱
            const deviceInfo = JSON.parse(pythonOutput);
            
            // 상태 업데이트
            deviceState.isOn = deviceInfo.device_on || false;
            deviceState.deviceInfo = deviceInfo;
            deviceState.lastUpdate = new Date();
            
            console.log("Python 스크립트를 통해 장치 상태를 확인했습니다.");
            return {
                ...deviceInfo,
                method: 'python',
                lastUpdate: deviceState.lastUpdate
            };
        } catch (parseError) {
            // 파싱 실패 시 기본 정보 반환
            console.error("Python 출력 파싱 실패:", parseError);
            
            // 캐시된 정보가 있으면 그 정보 반환, 없으면 기본 정보
            const fallbackInfo = deviceState.deviceInfo || {
                'device_id': CONFIG.deviceId,
                'model': 'P100',
                'mac': CONFIG.deviceMac,
                'device_on': deviceState.isOn || false,
                'error': 'Python 출력 파싱 실패'
            };
            
            return {
                ...fallbackInfo,
                method: 'cached',
                lastUpdate: deviceState.lastUpdate || new Date()
            };
        }
    } catch (error) {
        console.error("장치 상태 확인 실패:", error);
        
        // 오류 발생 시 기본 정보 반환
        return {
            'device_id': CONFIG.deviceId,
            'model': 'P100',
            'mac': CONFIG.deviceMac,
            'device_on': deviceState.isOn || false,
            'error': error.message,
            'method': 'error',
            'lastUpdate': deviceState.lastUpdate || new Date()
        };
    }
}

module.exports = {
    turnOn,
    turnOff,
    getDeviceInfo
};