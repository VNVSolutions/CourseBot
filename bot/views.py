import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .conf import bot
from .models import Start, WhyWe, Resume, LaborMarket, Interview, Contact, UserProfile
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Offer
from django.db.models import ObjectDoesNotExist
from django.db.models import Q


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
        return HttpResponse('')
    return HttpResponse('Invalid request method')


@bot.message_handler(commands=['start'])
def start(message):
    start_obj = Start.objects.first()
    name = message.chat.username
    chat_id = message.chat.id

    # Перевірка, чи існує користувач у базі даних за його telegram_id
    try:
        user = UserProfile.objects.get(telegram_id=chat_id)
    except UserProfile.DoesNotExist:
        # Якщо користувач не існує, створюємо нового користувача
        user = UserProfile.objects.create(telegram_id=chat_id, username=name)

    if start_obj:
        bot.send_message(message.chat.id, start_obj.text, reply_markup=create_reply_markup())

def create_reply_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    send_resume = KeyboardButton('👨‍💻 Надіслати резюме ')
    work_market = KeyboardButton('📊 Аналіз ринку праці ')
    interview = KeyboardButton('📌 Лайфхаки для співбесіди  ')
    contact = KeyboardButton('👋 Зв\'язатися з рекрутером ')
    why_we = KeyboardButton('🤔 Чому ми? 🤔')
    markup.add(send_resume, work_market, interview, contact, why_we)
    return markup


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Надіслати резюме для опрацювання':
        bot.send_message(message.chat.id, "Надішліть будь ласка своє резюме")
    elif message.text == 'Дізнатися що відбувається на ринку праці':
        labor_market = LaborMarket.objects.first()
        if labor_market:
            bot.send_message(message.chat.id, labor_market.text)
    elif message.text == 'Лайфхаки, як підготуватися до співбесіди':
        interview = Interview.objects.first()
        if interview:
            bot.send_message(message.chat.id, interview.text)
    elif message.text == 'Зв\'язатися з рекрутером':
        bot.send_message(message.chat.id, "Надішліть свій контакт")
        bot.register_next_step_handler(message, handle_contact)
    elif message.text == 'Чому ми?':
        why_we = WhyWe.objects.first()
        if why_we:
            bot.send_message(message.chat.id, why_we.text)


@bot.message_handler(content_types=['document', 'photo'])
def handle_resume(message):
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = os.path.join(settings.MEDIA_ROOT, message.document.file_name)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        user_name = message.from_user.username

        # Створення стану (state)
        button_options = [
            'Колектив',
            'Корпоративна культура',
            'Заробітна плата',
            'Локація',
            "Кар'єрний ріст",
            'Наявність навчання',
            'Робота без досвіду'
        ]
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for option in button_options:
            markup.add(KeyboardButton(option))
        markup.add(KeyboardButton('Зберегти вибір'))
        bot.send_message(message.chat.id, "Дякую! Поки опрацьовую, вкажи, що найголовніше для тебе в пошуках роботи",
                         reply_markup=markup)
        bot.register_next_step_handler(message, handle_resume_options, user_name, file_path, [], button_options)
    else:
        bot.send_message(message.chat.id, "Надішліть будь ласка у вигляді файлу")




def handle_resume_options(message, user_name, file_path, selected_options, button_options):
    preference = message.text

    if preference == 'Зберегти вибір':
        if len(selected_options) == 0:
            bot.send_message(message.chat.id, "Будь ласка, оберіть хоча б один варіант.")
            return
        selected_options_text = ", ".join(selected_options)
        resume_obj = Resume.objects.create(user=user_name, resume_file=file_path)
        resume_obj.preference = selected_options_text
        resume_obj.save()

        bot.send_message(message.chat.id, f"Ви обрали наступні варіанти: {selected_options_text}. Дякую!")

        button_options_skills = [
            'Комунікабельність (на)',
            'Швидко навчаюся',
            'Стресостійкість',
            'Багатозадачність',
            'Впевнений користувач ПК',
            'Володію знанням CRM',
            'Грамотна мова',
            'Робота в команді',
            'Володіння фотошопом',
            'Вирішення конфліктних ситуацій',
            'Критичне мислення',
            'Вміння досягати поставлених цілей',
            'Самодисципліна',
            'Пунктуальність'
        ]
        markup_skills = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for option in button_options_skills:
            markup_skills.add(KeyboardButton(option))
        markup_skills.add(KeyboardButton('Зберегти навички'))
        bot.send_message(message.chat.id, "Оберіть ваші навички", reply_markup=markup_skills)
        bot.register_next_step_handler(message, handle_resume_skills, user_name, file_path, [], button_options_skills)

        return

    selected_options.append(preference)
    button_options.remove(preference)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for option in button_options:
        markup.add(KeyboardButton(option))
    markup.add(KeyboardButton('Зберегти вибір'))
    bot.send_message(message.chat.id, "Оберіть ще один варіант або натисніть 'Зберегти вибір'", reply_markup=markup)
    bot.register_next_step_handler(message, handle_resume_options, user_name, file_path, selected_options,
                                   button_options)


def handle_resume_skills(message, user_name, file_path, selected_skills, button_options_skills):
    skill = message.text

    if skill == 'Зберегти навички':
        if len(selected_skills) == 0:
            bot.send_message(message.chat.id, "Будь ласка, оберіть хоча б одну навичку.")
            return
        selected_skills_text = ", ".join(selected_skills)

        try:
            resume = Resume.objects.filter(user=user_name, resume_file=file_path).last()
            resume.skills = selected_skills_text
            resume.save()
        except ObjectDoesNotExist:
            resume = Resume.objects.create(user=user_name, resume_file=file_path, skills=selected_skills_text)

        bot.send_message(message.chat.id, f"Ваші навички були збережені: {selected_skills_text}. Дякую!")
        bot.send_message(message.chat.id, f"Вкажи знання іноземних мов. Для багатьох компаній це плюс")
        bot.register_next_step_handler(message, handle_tongue, user_name)
        return

    selected_skills.append(skill)

    if skill in button_options_skills:
        button_options_skills.remove(skill)

    markup_skills = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for option in button_options_skills:
        markup_skills.add(KeyboardButton(option))
    markup_skills.add(KeyboardButton('Зберегти навички'))
    bot.send_message(message.chat.id, "Оберіть ще одну навичку або натисніть 'Зберегти навички'",
                     reply_markup=markup_skills)
    bot.register_next_step_handler(message, handle_resume_skills, user_name, file_path, selected_skills,
                                   button_options_skills)


def handle_tongue(message, user_name):
    tongue_info = message.text

    try:
        resume = Resume.objects.filter(user=user_name).last()
        resume.tongue = tongue_info
        resume.save()
        bot.send_message(message.chat.id, "Дякую! Ваша заяка успушно створена, очікуйте зворотньої відповіді")
        start(message)
    except ObjectDoesNotExist:
        bot.send_message(message.chat.id, "Помилка: не вдалося створити резюме спробуйте ще раз")


def handle_contact(message):
    user_name = message.from_user.username
    contact_info = message.text

    contact_obj = Contact.objects.create(user=user_name, contact=contact_info)

    bot.send_message(message.chat.id, "Дякую! Ваш контакт збережено.")


@receiver(post_save, sender=Offer)
def send_offer_notification(sender, instance, created, **kwargs):
    if created:
        message_text = f"📥 Повідомлення 📥\n\n{instance.text}\n"

        keyboard = InlineKeyboardMarkup()
        contact_button = InlineKeyboardButton("Зв'язатися з рекрутером", callback_data='contact_recruiter')
        keyboard.add(contact_button)

        bot.send_message(instance.user.telegram_id, message_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'contact_recruiter')
def contact_recruiter_callback(call):
    bot.send_message(call.message.chat.id, "Надішліть свій контакт")
    bot.register_next_step_handler(call.message, handle_text)


def handle_text(message):
    user_name = message.from_user.username
    contact_info = message.text

    contact_obj = Contact.objects.create(user=user_name, contact=contact_info)

    bot.send_message(message.chat.id, "Дякую! Ваш контакт збережено.")
