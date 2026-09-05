# راهنمای دپلوی روی Vercel

پروژه برای Python 3.13 و پشتیبانی مستقیم Django در Vercel تنظیم شده است.

## ۱. وارد کردن ریپازیتوری

در Vercel از **Add New → Project** ریپازیتوری زیر را Import کنید:

https://github.com/amiraliDamirchilo/alireza-abdulali

- **Framework Preset:** `Django`
- **Root Directory:** ریشهٔ پروژه (`./`)
- **Build Command:** از `vercel.json` خوانده می‌شود: `python manage.py migrate --noinput`
- **Install Command** و **Output Directory:** روی مقدار پیش‌فرض بمانند.

Vercel وابستگی‌ها را از `requirements.txt` نصب می‌کند، نسخهٔ پایتون را از `.python-version` می‌خواند و با استفاده از `STATIC_ROOT` به‌صورت خودکار `collectstatic` را اجرا می‌کند. درخواست‌ها به برنامهٔ ASGI و فایل‌های استاتیک به CDN هدایت می‌شوند.

## ۲. متغیرهای محیطی قبل از Deploy

در **Project Settings → Environment Variables** این مقادیر را تنظیم کنید:

| نام | مقدار |
| --- | --- |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_SECRET_KEY` | یک مقدار تصادفی و ثابت برای محیط Production |
| `DATABASE_URL` | آدرس اتصال PostgreSQL، ترجیحاً pooled، همراه با `sslmode=require` |
| `DJANGO_ALLOWED_HOSTS` | برای دامنهٔ اختصاصی: نام دامنه بدون `https://`؛ چند دامنه با ویرگول |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | برای دامنهٔ اختصاصی: آدرس کامل با `https://` و بدون اسلش انتهایی؛ چند آدرس با ویرگول |

دامنه‌های خود Vercel از `VERCEL_URL`، `VERCEL_PROJECT_PRODUCTION_URL` و `VERCEL_BRANCH_URL` شناسایی می‌شوند. گزینهٔ **Automatically expose System Environment Variables** باید فعال باشد. برای دامنهٔ اختصاصی دو متغیر مربوط به دامنه را نیز تنظیم کنید.

آدرس اتصال موجود پروژه در فایل محلی `.env` نگهداری شده و به گیت‌هاب ارسال نمی‌شود. مقدار `DATABASE_URL` را از آن فایل به بخش Environment Variables منتقل کنید. فایل نمونه فقط نام متغیرها را نشان می‌دهد؛ مقادیر خالی یا نمونه را به‌عنوان اطلاعات واقعی وارد نکنید. `.env` محلی ممکن است `DJANGO_DEBUG=1` داشته باشد؛ روی Vercel حتماً `0` تنظیم کنید.

برای ساخت کلید تصادفی:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

فایل `.env`، `.env.local`، دیتابیس SQLite، تصاویر آپلودشده و محیط مجازی در گیت قرار نمی‌گیرند. Vercel اطلاعات دیتابیس را از تنظیمات پروژه می‌خواند.

## ۳. دیتابیس و اولین اجرا

با زدن **Deploy**، migrationها در مرحلهٔ ساخت اجرا می‌شوند. اگر اتصال PostgreSQL نامعتبر باشد، ساخت متوقف می‌شود. SQLite برای اجرای محلی است و روی Vercel پذیرفته نمی‌شود.

برای Preview از دیتابیس یا شاخهٔ جداگانهٔ Neon استفاده کنید و `DATABASE_URL` آن را در محیط **Preview** قرار دهید؛ هر دپلوی migrationهای همان محیط را اجرا می‌کند. هنگام تغییر متغیرهای محیطی، یک Redeploy انجام دهید.

داده‌های SQLite محلی خودکار منتقل نمی‌شوند. migrationها فقط جداول و داده‌های اولیهٔ تعریف‌شده در پروژه را ایجاد می‌کنند. اگر اطلاعات موجود در SQLite لازم است، انتقال داده را جداگانه انجام دهید.

برای ساخت مدیر، با محیط مجازی فعال و اتصال `.env` به دیتابیس Production اجرا کنید:

```powershell
python manage.py createsuperuser
```

سپس به `https://YOUR_DOMAIN/studio-control/` بروید. اطلاعات ورود مدیر در کد یا متغیرهای build ذخیره نمی‌شود.

## ۴. ذخیرهٔ دائمی تصاویر پروژه

برای آپلود کاور از پنل مدیریت، ابتدا یک فضای ذخیره‌سازی S3-compatible مانند Amazon S3 یا Cloudflare R2 متصل کنید. دیسک Vercel محل ذخیرهٔ دائمی فایل‌های آپلودی نیست. نمایش سایت، ویدیوهای YouTube و فرم تماس به این تنظیم وابسته نیستند؛ آپلود کاور بدون آن روی Vercel قابل استفاده نیست.

| نام | کاربرد |
| --- | --- |
| `AWS_STORAGE_BUCKET_NAME` | نام bucket؛ با تنظیم آن ذخیره‌سازی ابری فعال می‌شود |
| `AWS_ACCESS_KEY_ID` | کلید دسترسی به bucket |
| `AWS_SECRET_ACCESS_KEY` | کلید محرمانه |
| `AWS_S3_REGION_NAME` | منطقهٔ S3؛ برای R2 مقدار `auto` |
| `AWS_S3_ENDPOINT_URL` | برای R2: `https://ACCOUNT_ID.r2.cloudflarestorage.com`؛ برای AWS معمولاً خالی |
| `AWS_S3_CUSTOM_DOMAIN` | اختیاری: دامنهٔ عمومی متصل به bucket، بدون پروتکل و اسلش انتهایی |

به‌صورت پیش‌فرض URLهای امضاشده برای فایل‌های خصوصی استفاده می‌شوند. اگر دامنهٔ عمومی تنظیم می‌کنید، دسترسی خواندن تصاویر از آن دامنه نیز باید برقرار باشد. فایل‌ها در مسیر `media/projects/` ذخیره می‌شوند. تصاویر قدیمی پوشهٔ `media/` در صورت نیاز باید با همان مسیر به bucket منتقل شوند.

## ۵. بررسی پس از انتشار

- صفحهٔ اصلی، فونت‌ها، CSS، JavaScript و تصویر پرتره را بررسی کنید.
- وارد `/studio-control/` شوید و یک پیام آزمایشی از فرم تماس بفرستید؛ باید در Inbox ذخیره شود.
- پس از اتصال storage، یک کاور آزمایشی آپلود کنید و پس از Redeploy هم نمایش آن را بررسی کنید.

مراجع: [Django در Vercel](https://vercel.com/docs/frameworks/full-stack/django)، [Python Runtime](https://vercel.com/docs/functions/runtimes/python)، [تنظیمات S3 در django-storages](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html).
