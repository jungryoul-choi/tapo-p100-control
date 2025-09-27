/**
 * Tapo P100 스마트 플러그 웹 컨트롤러 애플리케이션
 * 
 * 이 웹앱은 Tapo P100 스마트 플러그를 웹 인터페이스로 제어할 수 있게 해줍니다.
 * Express.js 기반 서버와 HTML/JS 프론트엔드로 구성되어 있습니다.
 */

const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { turnOn, turnOff, getDeviceInfo } = require('./tapo-controller');

// 애플리케이션 설정
const app = express();
const port = process.env.PORT || 3001; // 포트 번호를 3001로 변경

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

/**
 * 플러그 전원 켜기 API 엔드포인트
 */
app.post('/turnOn', async (req, res) => {
    try {
        const result = await turnOn();
        res.json({ 
            success: true, 
            message: '전원이 켜졌습니다.', 
            method: result.method,
            timestamp: new Date()
        });
    } catch (error) {
        console.error('Error turning on device:', error);
        res.status(500).json({ 
            success: false, 
            message: '에러 발생: ' + error.message,
            timestamp: new Date()
        });
    }
});

/**
 * 플러그 전원 끄기 API 엔드포인트
 */
app.post('/turnOff', async (req, res) => {
    try {
        const result = await turnOff();
        res.json({ 
            success: true, 
            message: '전원이 꺼졌습니다.', 
            method: result.method,
            timestamp: new Date()
        });
    } catch (error) {
        console.error('Error turning off device:', error);
        res.status(500).json({ 
            success: false, 
            message: '에러 발생: ' + error.message,
            timestamp: new Date()
        });
    }
});

/**
 * 플러그 상태 확인 API 엔드포인트
 */
app.get('/status', async (req, res) => {
    try {
        const status = await getDeviceInfo();
        res.json({ 
            success: true, 
            status,
            timestamp: new Date() 
        });
    } catch (error) {
        console.error('Error getting device status:', error);
        res.status(500).json({ 
            success: false, 
            message: '에러 발생: ' + error.message,
            timestamp: new Date()
        });
    }
});

/**
 * 오류 처리 미들웨어
 */
app.use((err, req, res, next) => {
    console.error('Application error:', err);
    res.status(500).json({
        success: false,
        message: '서버 오류가 발생했습니다.',
        error: err.message,
        timestamp: new Date()
    });
});

/**
 * 404 Not Found 핸들러
 */
app.use((req, res) => {
    res.status(404).json({
        success: false,
        message: '요청한 리소스를 찾을 수 없습니다.',
        path: req.path,
        timestamp: new Date()
    });
});

/**
 * 서버 초기화 및 시작
 */
app.listen(port, () => {
    console.log(`서버가 http://localhost:${port} 에서 실행 중입니다.`);
    console.log('Tapo P100 웹 컨트롤러가 시작되었습니다.');
    console.log('사용 가능한 API 엔드포인트:');
    console.log(' - POST /turnOn: 플러그 전원 켜기');
    console.log(' - POST /turnOff: 플러그 전원 끄기');
    console.log(' - GET /status: 플러그 상태 확인');
});