# 🎬 مستخرج نصوص اليوتيوب - PWA

تطبيق ويب تقدمي (PWA) لاستخراج النصوص والترجمة من فيديوهات اليوتيوب مجاناً.

## ✨ المميزات

- 📱 **يعمل على جميع الأجهزة** - لابتوب، أندرويد، آيفون
- 🌐 **بدون قيود** - استخراج غير محدود ومجاني
- ⏰ **مع أو بدون توقيتات** - حسب اختيارك
- 🌍 **متعدد اللغات** - دعم أكثر من 20 لغة
- 💾 **تحميل متنوع** - TXT, SRT, JSON
- 📋 **نسخ سريع** - نسخ مباشر للحافظة
- 📚 **سجل محلي** - حفظ تاريخ عمليات الاستخراج
- 🔄 **عمل بدون نت** - للنتائج المحفوظة مسبقاً
- 🚀 **تثبيت كتطبيق** - يمكن تثبيته على الشاشة الرئيسية

## 🛠️ طريقة التثبيت

### الطريقة الأولى: التشغيل المحلي

1. **تحميل الملفات:**
   ```bash
   # إنشاء مجلد جديد
   mkdir youtube-transcript-app
   cd youtube-transcript-app
   
   # حفظ الملفات في هذا المجلد:
   # - index.html
   # - manifest.json
   # - sw.js
   # - app.py
   ```

2. **تثبيت Python (إذا لم يكن مثبت):**
   - تحميل من: https://www.python.org/downloads/
   - تأكد من تفعيل "Add Python to PATH"

3. **تثبيت المكتبات المطلوبة:**
   ```bash
   pip install flask flask-cors youtube-transcript-api requests
   ```

4. **تشغيل الخادم:**
   ```bash
   python app.py
   ```

5. **فتح التطبيق:**
   - افتح المتصفح واذهب لـ: http://localhost:5000
   - التطبيق جاهز للاستخدام!

### الطريقة الثانية: الاستضافة المجانية

1. **GitHub Pages (مجاني):**
   - إنشاء حساب على GitHub
   - إنشاء repository جديد
   - رفع الملفات (index.html, manifest.json, sw.js)
   - تفعيل GitHub Pages من Settings

2. **Netlify (مجاني):**
   - اذهب لـ netlify.com
   - سحب وإفلات الملفات
   - الموقع يصبح جاهز تلقائياً

3. **Vercel (مجاني):**
   - اذهب لـ vercel.com
   - ربط مع GitHub repository
   - النشر التلقائي

## 🔧 التكوين المتقدم

### الحصول على YouTube API Key (اختياري):

1. اذهب لـ: https://console.cloud.google.com/
2. إنشاء مشروع جديد
3. تفعيل YouTube Data API v3
4. إنشاء API Key
5. ضع المفتاح في ملف `app.py`:
   ```python
   YOUTUBE_API_KEY = "YOUR_API_KEY_HERE"
   ```

### إضافة الأيقونات:

إنشاء أيقونات بأحجام مختلفة (72x72, 96x96, 128x128, 144x144, 152x152, 192x192, 384x384, 512x512) وحفظها باسم:
- icon-72.png
- icon-96.png  
- icon-128.png
- icon-144.png
- icon-152.png
- icon-192.png
- icon-384x384.png
- icon-512.png

## 📱 طريقة الاستخدام

1. **إدخال الرابط:**
   - انسخ رابط أي فيديو يوتيوب
   - الصق الرابط في الحقل المخصص

2. **اختيار الإعدادات:**
   - ✅ إضافة التوقيتات (إذا كنت تريد)
   - 🌐 اختيار اللغة المطلوبة
   - 🔄 تفعيل الترجمة التلقائية (عند الحاجة)

3. **الاستخراج:**
   - اضغط "استخراج النص"
   - انتظر قليلاً...
   - النص جاهز!

4. **التحميل والمشاركة:**
   - 📋 نسخ النص مباشرة
   - 💾 تحميل ملف TXT
   - 🎬 تحميل ملف SRT للترجمة
   - 📚 حفظ في السجل المحلي

## 🔧 استكشاف الأخطاء

### مشاكل شائعة:

**"فشل في استخراج النص":**
- تأكد أن الفيديو يحتوي على ترجمة
- جرب تفعيل "ترجمة تلقائية"
- تأكد من اتصال الإنترنت

**"رابط اليوتيوب غير صحيح":**
- تأكد من أن الرابط يحتوي على معرف الفيديو
- الأشكال المقبولة:
  - https://www.youtube.com/watch?v=VIDEO_ID
  - https://youtu.be/VIDEO_ID
  - https://www.youtube.com/embed/VIDEO_ID

**"خطأ في الخادم":**
- تأكد أن Python يعمل بشكل صحيح
- تحقق من تثبيت جميع المكتبات المطلوبة
- أعد تشغيل الخادم

### رسائل خطأ Python:

**"ModuleNotFoundError":**
```bash
pip install youtube-transcript-api flask flask-cors requests
```

**"Port already in use":**
- غيّر رقم المنفذ في app.py:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # استخدم 5001 بدلاً من 5000
```

## 🌟 مميزات متقدمة

### تثبيت كتطبيق:
- افتح الموقع في Chrome أو Safari
- ابحث عن خيار "إضافة إلى الشاشة الرئيسية"
- التطبيق سيظهر كأيقونة عادية

### العمل بدون إنترنت:
- النتائج المستخرجة مسبقاً تُحفظ محلياً
- يمكن الوصول إليها بدون إنترنت
- تحديث تلقائي عند عودة الاتصال

### المشاركة:
- يمكن مشاركة روابط اليوتيوب مباشرة مع التطبيق
- فتح تلقائي لاستخراج النص

## 🔒 الخصوصية والأمان

- 🔐 **لا حفظ على الخوادم** - كل شيء يتم محلياً
- 🛡️ **لا تجميع بيانات** - خصوصيتك محمية
- 🔄 **مفتوح المصدر** - يمكن مراجعة الكود
- 🌐 **HTTPS فقط** - اتصال آمن دائماً

## 🤝 المساهمة

هذا المشروع مفتوح للتطوير والتحسين:

- 🐛 **الإبلاغ عن الأخطاء** - ساعد في تحسين التطبيق
- 💡 **اقتراح مميزات جديدة** - شاركنا أفكارك
- 🔧 **تطوير الكود** - المساهمة في البرمجة
- 🌍 **الترجمة** - إضافة لغات جديدة

## 📋 قائمة الملفات المطلوبة

```
youtube-transcript-app/
├── index.html          # الواجهة الرئيسية
├── manifest.json       # تكوين PWA
├── sw.js              # Service Worker
├── app.py             # الخادم الخلفي (Python)
├── requirements.txt    # المكتبات المطلوبة
├── README.md          # دليل الاستخدام
├── icons/             # مجلد الأيقونات
│   ├── icon-72.png
│   ├── icon-96.png
│   ├── icon-128.png
│   ├── icon-144.png
│   ├── icon-152.png
│   ├── icon-192.png
│   ├── icon-384.png
│   └── icon-512.png
└── screenshots/       # مجلد الصور التوضيحية
    ├── screenshot1.png
    └── screenshot2.png
```

## 📦 ملف requirements.txt

```txt
Flask==2.3.3
Flask-CORS==4.0.0
youtube-transcript-api==0.6.1
requests==2.31.0
```

## 🚀 سكريبت التشغيل السريع

### Windows (run.bat):
```batch
@echo off
echo 🚀 Starting YouTube Transcript Extractor...
echo.
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python from python.org
    pause
    exit
)

echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo Starting server...
echo 📱 App will be available at: http://localhost:5000
echo 🔧 Press Ctrl+C to stop the server
echo.
python app.py
pause
```

### Linux/Mac (run.sh):
```bash
#!/bin/bash
echo "🚀 Starting YouTube Transcript Extractor..."
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3"
    exit 1
fi

echo "✅ Python3 is installed"
echo

echo "Installing requirements..."
pip3 install -r requirements.txt

echo
echo "Starting server..."
echo "📱 App will be available at: http://localhost:5000"
echo "🔧 Press Ctrl+C to stop the server"
echo

python3 app.py
```

## 🛠️ تخصيص التطبيق

### تغيير الألوان:
في ملف `index.html`، ابحث عن:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```
واستبدل الألوان حسب تفضيلك.

### إضافة لغات جديدة:
في ملف `app.py`، أضف للقائمة:
```python
languages = [
    # ... اللغات الموجودة
    {'code': 'ur', 'name': 'Urdu', 'native': 'اردو'},
    {'code': 'fa', 'name': 'Persian', 'native': 'فارسی'},
]
```

### تغيير المنفذ:
في نهاية ملف `app.py`:
```python
app.run(
    host='0.0.0.0',
    port=8080,  # غيّر المنفذ هنا
    debug=True,
    threaded=True
)
```

## 🔍 تحسين الأداء

### تفعيل التخزين المؤقت:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.memoize(timeout=3600)  # تخزين لمدة ساعة
def get_video_info(video_id):
    # الكود الموجود
```

### ضغط الاستجابات:
```python
from flask_compress import Compress

Compress(app)
```

## 📊 إحصائيات الاستخدام (اختياري)

### إضافة Google Analytics:
في ملف `index.html`، أضف قبل `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🔐 تأمين التطبيق

### تشفير HTTPS (للإنتاج):
```python
from flask_talisman import Talisman

Talisman(app, force_https=True)
```

### حماية من CORS:
```python
CORS(app, origins=['https://yourdomain.com'])
```

### تحديد معدل الطلبات:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/transcript', methods=['POST'])
@limiter.limit("10 per minute")
def get_transcript():
    # الكود الموجود
```

## 🌐 النشر على الخوادم

### Heroku:
1. إنشاء ملف `Procfile`:
```
web: python app.py
```

2. إنشاء ملف `runtime.txt`:
```
python-3.9.17
```

3. نشر:
```bash
heroku create your-app-name
git push heroku main
```

### Railway:
1. ربط GitHub repository
2. اختيار Python template
3. النشر التلقائي

### PythonAnywhere:
1. رفع الملفات للحساب
2. إنشاء Web App جديد
3. تكوين WSGI file

## 📋 قائمة التحقق للنشر

- [ ] اختبار جميع المميزات محلياً
- [ ] التأكد من عمل PWA (التثبيت، Service Worker)
- [ ] اختبار على أجهزة مختلفة (هاتف، تابلت، لابتوب)
- [ ] التحقق من الاستجابة (Responsive Design)
- [ ] اختبار الأمان (HTTPS, CORS)
- [ ] تحسين الصور والملفات
- [ ] إضافة معالجة الأخطاء
- [ ] كتابة التوثيق
- [ ] اختبار الأداء

## 🆘 الدعم الفني

### مشاكل شائعة وحلولها:

**1. التطبيق لا يفتح:**
- تحقق من تشغيل خادم Python
- تأكد من المنفذ 5000 غير مستخدم
- افحص firewall settings

**2. لا يمكن استخراج النص:**
- تحقق من اتصال الإنترنت
- تأكد أن الفيديو عام (ليس خاص)
- جرب فيديو آخر للتأكد

**3. PWA لا يعمل:**
- تأكد من استخدام HTTPS أو localhost
- افحص console للأخطاء
- تحقق من ملف manifest.json

**4. بطء في الاستجابة:**
- تحقق من سرعة الإنترنت
- قم بإعادة تشغيل الخادم
- احذف cache المتصفح

### معلومات الاتصال:
- 📧 البريد الإلكتروني: support@yourapp.com
- 💬 التلجرام: @YourUsername  
- 🐛 الإبلاغ عن الأخطاء: GitHub Issues

## 📈 التطوير المستقبلي

### مميزات مخطط إضافتها:
- [ ] دعم تحميل ملفات الصوت
- [ ] تلخيص تلقائي للنصوص
- [ ] البحث داخل النص المستخرج
- [ ] تحويل النص إلى صوت (TTS)
- [ ] دعم منصات أخرى (Vimeo, Dailymotion)
- [ ] API منفصل للمطورين
- [ ] تطبيق موبايل أصلي
- [ ] قاعدة بيانات للنصوص المستخرجة
- [ ] مشاركة النصوص مع الآخرين
- [ ] ترجمة النصوص للغات أخرى

## 🎯 نصائح للاستخدام الأمثل

### للمعلمين:
- استخراج نصوص المحاضرات التعليمية
- تحويل فيديوهات الشرح إلى ملاحظات مكتوبة
- إنشاء أسئلة من المحتوى المرئي

### للصحفيين:
- تفريغ المقابلات المسجلة
- استخراج الاقتباسات المهمة
- ترجمة المحتوى الأجنبي

### للطلاب:
- تحويل المحاضرات إلى ملاحظات
- ترجمة المحتوى التعليمي
- البحث في محتوى الفيديوهات

### للباحثين:
- تحليل المحتوى المرئي
- جمع البيانات من المقابلات
- أرشفة المحتوى الصوتي

---

## 📜 الترخيص

MIT License

Copyright (c) 2025 YouTube Transcript Extractor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**🎬 مستخرج نصوص اليوتيوب - حلول ذكية لعالم رقمي**

*استمتع بالاستخدام واستخرج كل ما تحتاجه من المحتوى المرئي!* 🚀