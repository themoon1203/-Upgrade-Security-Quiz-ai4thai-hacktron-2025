# 📦 Simple Multi-API Project

โปรเจกต์นี้สาธิตการทำงานของ API 2 ตัวที่เชื่อมต่อกันผ่าน **Docker Compose**

---

## ⚙️ รายละเอียดการทำงาน

- **API1**
  - รับคำขอจาก **User** (GET และ POST)
  - ถ้า POST จะส่ง JSON ต่อไปให้ **API2**
  - ถ้า GET จะเรียก API2 แบบไม่ส่งข้อมูล
  - มี log แสดงการรับและส่งข้อมูล

- **API2**
  - รับคำขอจาก **API1** (GET และ POST)
  - POST จะตอบกลับข้อความจาก JSON
  - GET จะตอบกลับ `Hello from make me happy`
  - มี log ทุกครั้งที่รับคำขอ

---

## 🐳 รันด้วย Docker Compose

### ✅ โครงสร้างไฟล์

```
.
├── api1/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│
├── api2/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│
├── docker-compose.yml
└── README.md
```

### ✅ วิธีใช้งาน

1️⃣ สร้างไฟล์ตามโครงสร้างด้านบน  
โดยแต่ละ Service มี:
- `app.py` (ตามโค้ดที่ให้)
- `requirements.txt`  
  ```
  flask
  requests
  ```
  (API2 อาจไม่ต้องมี requests ถ้าไม่ได้เรียก API อื่น)

- `Dockerfile`
  ```dockerfile
  FROM python:3.10-slim

  WORKDIR /app

  COPY requirements.txt requirements.txt
  RUN pip install -r requirements.txt

  COPY . .

  CMD ["python", "app.py"]
  ```

2️⃣ ไฟล์ `docker-compose.yml`

```yaml
version: '3.8'

services:
  api1:
    build: ./api1
    ports:
      - "5000:5000"
    depends_on:
      - api2

  api2:
    build: ./api2
    ports:
      - "5001:5001"
```

3️⃣ รันโปรเจกต์

```
docker-compose up --build
```

---

## ✅ วิธีทดสอบ

### 📌 GET

```
curl http://localhost:5000/api1
```

ผลลัพธ์:
```
{ "answer": "Hello from make me happy" }
```

### 📌 POST

```
curl -X POST http://localhost:5000/api1 -H "Content-Type: application/json" -d '{"message":"Hello API2 from User!"}'
```

ผลลัพธ์:
```
{ "answer": "Hello API2 from User!" }
```

---

## 🗒️ หมายเหตุ

- API1 ใช้ `requests` เรียก API2 ภายใน Docker Network เดียวกัน
- ใช้ `depends_on` ให้ API2 รันก่อน
- log จะพิมพ์บน console ของทั้งสอง Container

---

## 🎉 เสร็จสิ้น
