# 🔐 Upgrade Security Quiz - AI4Thai Hacktron 2025

> **ทีม:** Make me happy  
> **งาน:** AI4Thai Hacktron 2025

## 📋 ภาพรวมโปรเจกต์

โปรเจกต์นี้สาธิตการทำงานของ Microservices Architecture โดยใช้ FastAPI สองตัวที่เชื่อมต่อกันด้วย HTTP และจัดการด้วย Docker Compose พร้อมระบบ Authentication และ Logging ที่ครอบคลุม

## 🏗️ สถาปัตยกรรม

```
┌─────────────┐   HTTP + Auth   ┌──────────────────┐
│             │ ──────────────► │                  │
│   Gateway   │                │ Message Processor│
│ (Port 5000) │ ◄────────────── │   (Port 5001)    │
│             │   JSON Response │                  │
└─────────────┘                 └──────────────────┘
       ▲                                   ▲
       │                                   │
User + Bearer Token              Internal Processing
```

### Gateway Service (Port 5000)
- **Authentication**: ใช้ Bearer Token (`makemehappy`)
- **GET /messages**: ส่งคำขอไปยัง Message Processor โดยไม่ส่งข้อมูล
- **POST /messages**: ส่ง JSON payload ไปยัง Message Processor (ไม่จำเป็นต้องส่งข้อมูล)
- **GET /health**: Health check endpoint
- ระบบ Logging แบบสี (Blue สำหรับ INFO)
- ทำหน้าที่เป็น API Gateway พร้อม Authentication

### Message Processor Service (Port 5001)
- **POST /process**: ประมวลผลข้อความและส่งกลับพร้อม request_id และ timestamp
- **GET /health**: Health check endpoint  
- ระบบ Logging แบบสี (Yellow สำหรับ INFO)
- สร้าง unique request_id สำหรับแต่ละคำขอ
- Default message: `"Hello from make me happy"`

## 📁 โครงสร้างโปรเจกต์

```
.
├── gateway/
│   ├── app.py              # Gateway FastAPI application
│   ├── main.py             # App factory
│   ├── requirements.txt    # Dependencies
│   └── Dockerfile         # Container configuration
├── message_processor/
│   ├── app.py              # Message Processor FastAPI application
│   ├── main.py             # App factory
│   ├── requirements.txt    # Dependencies
│   └── Dockerfile         # Container configuration
├── docker-compose.yml      # Multi-container orchestration
├── test.py                # Testing script
└── README.md              # ไฟล์นี้
```

## 🔐 Authentication

โปรเจกต์ใช้ **Bearer Token Authentication**

**Token ที่ถูกต้อง:** `makemehappy`

ทุกคำขอไปยัง Gateway จำเป็นต้องมี Header:
```
Authorization: Bearer makemehappy
```

## 🚀 เริ่มต้นใช้งาน

### สิ่งที่ต้องติดตั้งก่อน
- Docker
- Docker Compose
- Python 3.10+ (สำหรับ test.py)
- curl หรือ httpx (สำหรับการทดสอบ)

### การติดตั้งและตั้งค่า

1. **Clone Repository**
   ```bash
   git clone https://github.com/themoon1203/-Upgrade-Security-Quiz-ai4thai-hacktron-2025.git
   cd -Upgrade-Security-Quiz-ai4thai-hacktron-2025
   ```

2. **Build และ Run Services**
   ```bash
   docker-compose up --build
   ```

3. **ตรวจสอบว่า Services ทำงานแล้ว**
   ```bash
   docker-compose ps
   ```

## 🔧 API Endpoints

### Gateway Service (Port 5000)

#### GET /messages
ดึงข้อความ default จาก Message Processor

**คำขอ:**
```bash
curl -X GET http://localhost:5000/messages -H "Authorization: Bearer makemehappy"
```

**ผลลัพธ์:**
```json
{
  "answer": "Hello from make me happy",
  "request_id": "REQ-20250720143052-123",
  "timestamp": 1721467852.123
}
```

#### POST /messages (พร้อม payload)
ส่งข้อความไปยัง Message Processor

**คำขอ:**
```bash
curl -X POST http://localhost:5000/messages -H "Authorization: Bearer makemehappy" -H "Content-Type: application/json" -d "{\"message\": \"ทดสอบข้อความ\"}"
```

**ผลลัพธ์:**
```json
{
  "answer": "สวัสดีจาก User!",
  "request_id": "REQ-20250720143052-456",
  "timestamp": 1721467852.456
}
```

#### POST /messages (ไม่มี payload หรือ payload ว่าง)
ส่งคำขอแบบ POST โดยไม่ส่งข้อมูล จะได้ค่า default

**คำขอ:**
```bash
curl -X POST http://localhost:5000/messages -H "Authorization: Bearer makemehappy" -H "Content-Type: application/json" -d "{}"
```

**ผลลัพธ์:**
```json
{
  "answer": "Hello from make me happy",
  "request_id": "REQ-20250720143052-789",
  "timestamp": 1721467852.789
}
```

#### GET /health
ตรวจสอบสถานะ Gateway

**คำขอ:**
```bash
curl http://localhost:5000/health
```

**ผลลัพธ์:**
```json
{
  "status": "Gateway Up!"
}
```

### Message Processor Service (Port 5001)
*เป็น Internal Service - ไม่สามารถเข้าถึงจากภายนอก Docker Network ได้โดยตรง*

## 🧪 การทดสอบ

### ใช้ Test Script (แนะนำ)
```bash
# ติดตั้ง dependencies สำหรับ test script
pip install httpx

# รัน test script
python test.py
```

### ใช้ curl

**ทดสอบ GET request:**
```bash
curl -X GET http://localhost:5000/messages -H "Authorization: Bearer makemehappy"
```

**ทดสอบ POST request พร้อม message:**
```bash
curl -X POST http://localhost:5000/messages -H "Authorization: Bearer makemehappy" -H "Content-Type: application/json" -d "{\"message\": \"ทดสอบข้อความ\"}"
```

**ทดสอบ POST request ไม่มี message:**
```bash
curl -X POST http://localhost:5000/messages -H "Authorization: Bearer makemehappy" -H "Content-Type: application/json" -d "{}"
```

**ทดสอบ Authentication ผิด:**
```bash
curl -X POST http://localhost:5000/messages -H "Authorization: Bearer wrongtoken" -H "Content-Type: application/json"
```

### ใช้ Postman
1. **GET Request**: 
   - URL: `http://localhost:5000/messages`
   - Headers: `Authorization: Bearer makemehappy`

2. **POST Request**: 
   - URL: `http://localhost:5000/messages`
   - Method: POST
   - Headers: 
     - `Authorization: Bearer makemehappy`
     - `Content-Type: application/json`
   - Raw body (Optional): `{"message":"ข้อความที่ต้องการทดสอบ"}`

## 📊 การติดตามและ Logs

ดู Logs แบบ Real-time พร้อมสี:

```bash
# ทุก Services
docker-compose logs -f

# Service เฉพาะ
docker-compose logs -f gateway
docker-compose logs -f message_processor
```

**รูปแบบ Log:**
- **Gateway**: ข้อความสีฟ้า (INFO)
- **Message Processor**: ข้อความสีเหลือง (INFO)

## 🛠️ Technical Details

### Dependencies

**Gateway Service:**
```
fastapi
httpx
uvicorn
pydantic
python-dotenv
colorlog
```

**Message Processor Service:**
```
fastapi
uvicorn
colorlog
```

### Docker Configuration
- **Python Version**: 3.10-slim
- **Port Mapping**: Gateway:5000, Processor:5001
- **Dependencies**: Gateway depends_on Message Processor
- **Factory Pattern**: ใช้ App Factory Pattern สำหรับ FastAPI

### Response Format
ทุก response จาก Message Processor จะมี:
- `answer`: ข้อความตอบกลับ
- `request_id`: ID เฉพาะสำหรับแต่ละคำขอ (รูปแบบ: REQ-YYYYMMDDHHMMSS-XXX)
- `timestamp`: Unix timestamp

## 🔍 แก้ไขปัญหา

### ปัญหาที่พบบ่อย

1. **Authentication Error (403)**:
   ```bash
   # ตรวจสอบ token ให้ถูกต้อง
   curl -H "Authorization: Bearer makemehappy" http://localhost:5000/messages
   ```

2. **Port conflicts**: 
   ```bash
   sudo lsof -i :5000
   sudo lsof -i :5001
   ```

3. **Service ไม่ตอบสนอง**:
   ```bash
   docker-compose ps
   docker-compose logs gateway
   docker-compose logs message_processor
   ```

4. **Build ล้มเหลว**:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

## 🚨 Security Features

- **Bearer Token Authentication**: ป้องกันการเข้าถึงโดยไม่ได้รับอนุญาต
- **Internal Network**: Message Processor ไม่เปิดให้เข้าถึงจากภายนอก
- **Request ID Tracking**: ติดตามและ audit การใช้งาน
- **Input Validation**: ใช้ Pydantic สำหรับ validation
- **Error Handling**: จัดการ error อย่างเหมาะสม

## 🏆 บริบทของการแข่งขัน

โปรเจกต์นี้พัฒนาสำหรับ **AI4Thai Hacktron 2025** เพื่อสาธิต:
- Secure Microservices Architecture
- Modern API Development กับ FastAPI
- Authentication และ Authorization
- Container Security Best Practices
- Structured Logging และ Monitoring
- API Gateway Pattern
- Async HTTP Communication

## 🧪 Test Coverage

Test script ครอบคลุม:
- ✅ POST request พร้อม payload
- ✅ POST request ไม่มี payload (default message)
- ✅ GET request
- ✅ Invalid token authentication
- ✅ Async HTTP client testing

## 👥 ทีม

**ชื่อทีม:** Make me happy  
**การแข่งขัน:** AI4Thai Hacktron 2025

## 📄 สิทธิการใช้งาน

โปรเจกต์นี้เป็นส่วนหนึ่งของการแข่งขัน AI4Thai Hacktron 2025

---

*🔒 Built with Security & ❤️ by Team Make me happy*
