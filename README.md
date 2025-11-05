# Cybernetic AI Core Showcase

โปรเจกต์นี้ประกอบด้วยตัวอย่างสำหรับสร้างบรรยากาศพลังงานดิจิทัลแบบไซเบอร์เนติก ได้แก่

- หน้าเว็บ HTML/CSS สำหรับโชว์แกนกลาง AI ที่มีแอนิเมชันเรืองแสง (`index.html`)
- สคริปต์ Python สำหรับสุ่มสร้างภาพพลังงานดิจิทัลในรูปแบบสนามพลัง (`digital_energy.py`)
- โค้ด JavaScript สำหรับแสดงเอฟเฟกต์วงแหวนพลังงานบน `<canvas>` (`power_ring.js`)

## วิธีใช้งาน

### 1. หน้าเว็บ Cybernetic AI Core
เปิดไฟล์ `index.html` ในเบราว์เซอร์เพื่อดูแอนิเมชันและเอฟเฟกต์ของแกนกลาง AI

### 2. สุ่มสร้างภาพพลังงานดิจิทัลด้วย Python
ติดตั้งไลบรารีที่จำเป็นก่อน (เช่น `matplotlib` และ `numpy`):

```bash
pip install matplotlib numpy
```

จากนั้นรันสคริปต์:

```bash
python digital_energy.py
```

จะมีหน้าต่างกราฟิกแสดงภาพพลังงานที่สุ่มสร้างขึ้นใหม่ทุกครั้งที่รัน

### 3. เอฟเฟกต์วงแหวนพลังด้วย JavaScript
นำเข้าโมดูลและเรียกใช้ในโปรเจกต์เว็บของคุณ:

```html
<canvas id="energy-ring" width="400" height="400"></canvas>
<script type="module">
  import { createEnergyRing } from './power_ring.js';
  const canvas = document.getElementById('energy-ring');
  createEnergyRing(canvas);
</script>
```

เมื่อหน้าเว็บโหลดเสร็จจะเห็นเอฟเฟกต์วงแหวนพลังงานเคลื่อนไหวอยู่ภายในแคนวาส
