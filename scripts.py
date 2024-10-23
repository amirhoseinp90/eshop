import random
from products.models import SmartPhone, Category
from products.enums import *


smartphone_category, created = Category.objects.get_or_create(slug='smart-phone', defaults={
    'title': 'Smart Phones',
    'title_fa': 'گوشی‌های هوشمند'
})


titles = [
    'گوشی موبایل اپل مدل iPhone 13 CH دو سیم‌ کارت ظرفیت 128 گیگابایت و رم 4 گیگابایت - نات اکتیو',
    'گوشی موبایل اپل مدل iPhone 12 ZA/A دو سیم‌ کارت ظرفیت 256 گیگابایت و رم 4 گیگابایت - نات اکتیو',
    'گوشی موبایل اپل مدل iPhone 13 Pro ZAA دو سیم‌ کارت ظرفیت 128 گیگابایت و رم 6 گیگابایت - نات اکتیو ریفربیش پارت نامبر F',
    'گوشی موبایل اپل مدل iPhone 13 CH دو سیم‌ کارت ظرفیت 256 گیگابایت و رم 4 گیگابایت به همراه شارژر 20 وات اپل - نات اکتیو',
    'گوشی موبایل اپل مدل iPhone 13 Pro ZAA دو سیم‌ کارت ظرفیت 512 گیگابایت و رم 6 گیگابایت - نات اکتیو ریفربیش پارت نامبر F'
]

descriptions = [
    'اپل همواره توانسته است گوشی‌های هوشمند قدرتمند و بسیار باکیفیتی را روانه بازار کند و پرچمداران سری 13 هم توانستند با بهره بردن از مشخصات فنی قدرتمند، نه‌تنها به نسبت نسل قبلی یعنی خانواده iPhone12، بلکه به نسبت پرچمداران مدعی دیگر هم عملکرد بسیار درخشانی داشته باشند. iPhone 13 Pro از لحاظ مشخصات فنی در نظر گرفته شده چیزی کم از گل سرسبد این سری یعنی iPhone 13 Pro Max ندارد. در نمای روبه‌رویی این گوشی به صفحه‌نمایش با ابعاد 6.1 اینچ و رزولوشن 2532x1170 از نوع Super Retina XDR OLED مجهز شده است. صفحه‌نمایش بسیار باکیفیت که از جمله قابلیت‌های قدرتمند آن، می‌توانیم به نرخ بروزرسانی 120 هرتز و البته حداکثر روشنایی 1200 نیت (nits) اشاره کنیم. در بخش سنسور‌های دوربین هم قرارگیری سه سنسور با رزولوشن 12 مگاپیکسل به ترتیب از نوع عریض، تله‌فوتو و فوق عریض یا همان ultrawide هستیم که البته سنسور TOF 3D LiDAR هم با عملکردی مشابه با سنسورهای سنجش عمق و البته بهتر، این گوشی را همراه می‌کنند. برای دوربین سلفی هم سنسور با رزولوشن 12 مگاپیکسل در نظر گرفته شده است. در بخش فیلمبرداری هم مثل همیشه این بار اما به لطف توانایی ضبط ویدیو با نهایت کیفیت 4K و سرعت 60 فریم در ثانیه برای سنسور عریض و سلفی، این گوشی عملکرد بی‌نظیری را به شما ارائه می‌کند که کمتر پرچمداری توانایی رقابت با آن را دارد. حضور پردازنده قدرتمند Apple A15 هم سبب شده تا این گوشی به‎‌راحتی از پس اجرای سنگین‌ترین بازی‌های روز دنیا بربیاید. باتری با میزان ظرفیت 3095 میلی‌آمپر‌ساعت از دیگر مشخصات در نظر گرفته شده است. البته باید بدانید که خبری از آداپتور شارژر نیست. این گوشی موبایل با سری F(Not Active) توسط کمپانی اپل عرضه می‌شود. گوشی‌های سری F به علت نقص نرم‌افزاری به نمایندگی‌های اپل برای تعمیر تحویل داده شده‌اند و بدنه این کالاها کاملا نو است و همچنین دارای گارانتی جهانی اپل هستند. گوشی‌های اپل با پارت نامبر(Active) 5L به عنوان کالاهای تعمیر شده توسط کمپانی اپل (از نظر سخت افزاری یا نرم‌افزاری) است اما گارانتی جهانی اپل را ندارند. گوشی های اپل با پارت نامبر 5C(Active)، کالاهایی هستند که توسط شرکت‌هایی غیر از کمپانی اپل تعمیر و عرضه می‌شوند و مورد تایید اپل نیستند.',
    ] * 5

prices = [random.randint(50000000, 100000000)
          for _ in range(5)]  # Random prices between 150 and 1500

for i in range(5):
    smart_phone = SmartPhone.objects.create(
        title=titles[i],
        description=descriptions[i],
        price=prices[i],
        category=smartphone_category,
        weight=f"{random.randint(150, 200)} grams",
        dimensions=f"{random.randint(5, 6)}.5 x {random.randint(2, 3)}.0 x {random.randint(0, 1)}.0 cm",
        sim_cart_number=f"{random.randint(1, 2)} SIM card",
        cpu=f"CPU {random.choice(['Snapdragon', 'Exynos', 'MediaTek'])} {random.randint(1, 3)} GHz",
        cpu_frequency=f"{random.randint(1, 8)} cores",
        gpu=f"GPU {random.choice(['Adreno', 'Mali', 'PowerVR'])}",
        internal_space=random.choice(
            [capacity for capacity in Capacity.choices]),
        ram=random.choice([capacity for capacity in Capacity.choices]),
        refresh_rate=random.choice([rate for rate in RefreshRate.choices]),
        screen_technology=random.choice(
            [tech for tech in ScreenTechnology.choices]),
        radio=random.choice([True, False]),
        number_of_back_camera=random.choice(
            [num for num in CameraNumber.choices]),
        os=random.choice([os for os in OS.choices])
    )


