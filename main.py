import os
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# إعدادات الحساب والبيانات
API_ID = int(os.environ.get("API_ID", "32251310"))
API_HASH = os.environ.get("API_HASH", "055612b7ab440bae2c5ef96440c17737")
# جلب جلسة الحساب النصية من متغيرات البيئة في الاستضافة
SESSION_STRING = os.environ.get("SESSION", "")

# تشغيل العميل باستخدام الـ String Session
app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING if SESSION_STRING else None
)

# ==========================================
# الأداة 1: فحص حالة البوت والاستضافة (مع الحذف التلقائي)
# ==========================================
@app.on_message(filters.me & filters.command("فحص", prefixes="."))
async def ping_check(client: Client, message: Message):
    start_time = time.time()
    await message.edit("<b>⚡ جاري فحص الاتصال والاستضافة...</b>")
    end_time = time.time()
    
    ping_ms = round((end_time - start_time) * 1000, 2)
    
    response_text = (
        "<b>🟢 اليوزربوت والاستضافة يعملان بانسجام تام!</b>\n\n"
        f"<b>⏱️ سرعة الاستجابة (Ping):</b> <code>{ping_ms} ms</code>\n"
        "<b>⚙️ الحالة:</b> متصل وفعال بنجاح 🚀"
    )
    await message.edit(response_text)
    
    await asyncio.sleep(4)
    try:
        await message.delete()
    except Exception:
        pass


# ==========================================
# الأداة 2: حفظ الصور ذاتية التدمير (تعرض لمرة واحدة)
# ==========================================
@app.on_message(filters.private & (filters.photo | filters.video))
async def auto_save_disappearing_media(client: Client, message: Message):
    if message.ttl_seconds and message.ttl_seconds > 0:
        if getattr(client, "save_disappearing_active", False):
            try:
                file_path = await message.download()
                if message.photo:
                    await client.send_photo("me", photo=file_path, caption="📥 تم حفظ صورة ذاتية التدمير تلقائياً!")
                elif message.video:
                    await client.send_video("me", video=file_path, caption="📥 تم حفظ فيديو ذاتي التدمير تلقائياً!")
                
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"خطأ أثناء حفظ الوسائط ذاتية التدمير: {e}")

@app.on_message(filters.me & filters.command("تفعيل الذاتية", prefixes="."))
async def toggle_disappearing_save(client: Client, message: Message):
    current_state = getattr(client, "save_disappearing_active", False)
    client.save_disappearing_active = not current_state
    
    if client.save_disappearing_active:
        await message.edit("<b>✅ تم تفعيل ميزة حفظ الوسائط ذاتية التدمير في سحابتك الشخصية.</b>")
    else:
        await message.edit("<b>❌ تم إيقاف ميزة حفظ الوسائط ذاتية التدمير.</b>")
    
    await asyncio.sleep(4)
    try:
        await message.delete()
    except Exception:
        pass


# ==========================================
# الأداة 3: النشر التلقائي في المجموعات
# ==========================================
@app.on_message(filters.me & filters.command("نشر", prefixes="."))
async def auto_post_command(client: Client, message: Message):
    args = message.text.split(" ", 1)
    command_part = args[0]
    
    import re
    seconds_match = re.search(r'\d+', command_part)
    
    if not seconds_match and len(args) > 1:
        seconds_match = re.search(r'\d+', args[1])
        
    if not seconds_match:
        await message.edit("<b>⚠️ يرجى تحديد عدد الثواني بشكل صحيح. مثال:</b>\n<code>.نشر10</code> (بالرد على الرسالة)")
        await asyncio.sleep(4)
        try:
            await message.delete()
        except Exception:
            pass
        return
        
    interval = int(seconds_match.group())
    
    if not message.reply_to_message:
        await message.edit("<b>⚠️ يجب الرد على الرسالة أو الملصق المراد نشره تلقائياً!</b>")
        await asyncio.sleep(4)
        try:
            await message.delete()
        exceptException:
            pass
        return
        
    target_msg = message.reply_to_message
    chat_id = message.chat.id
    
    await message.edit(f"<b>🚀 بدأت عملية النشر التلقائي كل {interval} ثانية...\nأرسل .إيقاف النشر للإيقاف.</b>")
    
    await asyncio.sleep(4)
    try:
        await message.delete()
    except Exception:
        pass
    
    setattr(client, f"auto_posting_{chat_id}", True)
    
    while getattr(client, f"auto_posting_{chat_id}", False):
        try:
            await target_msg.copy(chat_id)
            await asyncio.sleep(interval)
        except Exception as e:
            print(f"خطأ في النشر التلقائي: {e}")
            break

@app.on_message(filters.me & filters.command("إيقاف النشر", prefixes="."))
async def stop_auto_post(client: Client, message: Message):
    chat_id = message.chat.id
    setattr(client, f"auto_posting_{chat_id}", False)
    await message.edit("<b>🛑 تم إيقاف النشر التلقائي في هذه المجموعة.</b>")
    
    await asyncio.sleep(4)
    try:
        await message.delete()
    except Exception:
        pass


# ==========================================
# الأداة 4: اللعب الوهمي (تغيير حالة النشاط إلى يلعب الآن)
# ==========================================
@app.on_message(filters.me & filters.command("وهمي", prefixes="."))
async def fake_playing_status(client: Client, message: Message):
    text_content = message.text.replace(".وهمي", "").strip()
    parts = text_content.rsplit(" ", 1)
    
    game_name = "لعبة وهمية"
    duration = 30
    
    if len(parts) == 2 and parts[1].isdigit():
        game_name = parts[0]
        duration = int(parts[1])
    elif len(parts) == 1 and parts[0].isdigit():
        duration = int(parts[0])
    elif len(parts) == 1 and parts[0]:
        game_name = parts[0]

    await message.edit(f"🎮 <b>جاري تفعيل حالة (يلعب الآن: {game_name}) لمدة {duration} ثانية...</b>")
    
    try:
        from pyrogram.raw.functions.account import UpdateStatus
        
        start_time = time.time()
        while time.time() - start_time < duration:
            await client.invoke(UpdateStatus(offline=False))
            await asyncio.sleep(10)
            
        await message.edit(f"✅ <b>انتهت مدة اللعب الوهمي ({game_name}).</b>")
        await asyncio.sleep(4)
        await message.delete()
    except Exception as e:
        await message.edit(f"❌ حدث خطأ أثناء تفعيل الحالة الوهمية: {e}")
        await asyncio.sleep(4)
        try:
            await message.delete()
        except Exception:
            pass


# تشغيل البوت
print("🤖 اليوزربوت يعمل الآن بكفاءة...")
app.run()