# راه‌اندازی دیتابیس و پیامک مدلت

1. در supabase.com یک پروژه بسازید و فایل `schema.sql` را در SQL Editor اجرا کنید (جدول کاربران، کدها و نشست‌ها).
2. در kavenegar.com (یا هر سرویس پیامک ایرانی) یک «قالب تأیید» با متن مثل «کد ورود مدلت: %token» بسازید.
3. تابع `index.ts` را با نام `modelet-auth` در Edge Functions دیپلوی کنید و این Secretها را خودتان در داشبورد ست کنید:
   KAVENEGAR_KEY، KAVENEGAR_TEMPLATE، OTP_PEPPER (یک رشتهٔ تصادفی بلند)، ALLOW_ORIGIN (آدرس سایت).
4. در صفحهٔ سایت، قبل از اسکریپت اصلی بگذارید:
   `<script>window.MODELET_API="https://<project>.supabase.co/functions/v1/modelet-auth"</script>`
   با این کار حالت نمایشی خاموش و کد فقط پیامک می‌شود.

کلیدها را داخل چت یا کد سایت نگذارید.
