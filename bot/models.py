from django.db import models


class UserProfile(models.Model):
    telegram_id = models.BigIntegerField(null=True)
    username = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f"User: {self.username}, ID: {self.telegram_id}"

    class Meta:
        db_table = "userprofile"


class Offer(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст пропозиції")

    def __str__(self):
        return f"Offer for {self.user.username}: {self.text}"

    class Meta:
        db_table = "offer"


class Start(models.Model):
    text = models.TextField(verbose_name="Старт", null=True)

    def __str__(self):
        return f"Text: {self.text}"

    class Meta:
        db_table = "start"


class WhyWe(models.Model):
    text = models.TextField(verbose_name="Чому ми?", null=True)

    def __str__(self):
        return f"Text: {self.text}"

    class Meta:
        db_table = "why_we"


class LaborMarket(models.Model):
    text = models.TextField(verbose_name="Ринок праці", null=True)
    img = models.ImageField(upload_to='resumes/', blank=True)

    def __str__(self):
        return f"Text: {self.text}"

    class Meta:
        db_table = "labor_market"


class Interview(models.Model):
    text = models.TextField(verbose_name="Підготовка до співбесіди", null=True)
    img = models.ImageField(upload_to='resumes/', blank=True)

    def __str__(self):
        return f"Text: {self.text}"

    class Meta:
        db_table = "interview"


class Contact(models.Model):
    user = models.CharField(verbose_name="Користувач", max_length=100)
    contact = models.TextField(verbose_name="Контакти", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Text: {self.contact}"

    class Meta:
        db_table = "contact"


class Resume(models.Model):
    user = models.CharField(max_length=100)
    resume_file = models.FileField(upload_to='resumes/', blank=True)
    preference = models.TextField(verbose_name="Найголовніше у пошуку роботи", null=True)
    skills = models.TextField(verbose_name="Навички", null=True)
    tongue = models.TextField(verbose_name="Володіння мовами", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user}, Job Preference: {self.preference}, Skills: {self.skills}, Tongue: {self.tongue}"