import os
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# إعدادات الحساب والبيانات
API_ID = int(os.environ.get("API_ID", "32251310"))
API_HASH = os.environ.get("API_HASH", "055612b7ab440bae2c5ef96440c17737")
SESSION_STRING = os.environ.get("SESSION", "AgHsHa4ASadFi903MuDVw7f0z7ZclCHawQhW94sRdRsnRvCToiEY43rIfH7O7sdnaOlitgZfPT93uZ4avrz01fJu8neBeEHseNfTPlaeIMLZJKt0lePM_qECpkR_gSodAaJMTi9wjDU5SbscvZNOc-AE-Vq0kHZ1i0h2j6j4A-CVTKnDebJu4ysd9jF0rcPFzxo2_ShOh-cCfdWR0RxNgq7ct-6wW8uJ4rfmDhhiygAbDjHAaMeavaSNoqD6Fm4HJFcLyREr_TNlKRYYZDKekb6P27Fb4cfAzSQ4SKJx2b1rOL0jq2r31zXs7FeWBZEUqPjQLV8BbVo-fnwFwDnoAjC8gf4J1AAAAAH7Q5fAAA")

app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING if SESSION_STRING else None
)

# قاموس مؤقت لتخزين عمليات النشر النشطة
active_custom_posts = {}

# ==========================================
# لوحة التحكم الرئيسية والأوامر
# ==========================================
@app.on_message(filters.me & filters.command(["لوحة", "الاوامر", "اوامر"], prefixes="."))
async def control_panel_command(client: Client, message: Message):
    panel_text = (
        "<b>🎛️ لوحة التحكم الرئيسية - اليوزربوت</b>\n\n"
        "• <code>.فحص</code> : فحص سرعة الاستجابة.\n"
        "• <code>.تفعيل الذاتية</code> : لحفظ الوسائط ذاتية التدمير.\n"
        "• <code>.تخصيص</code> : لعرض الكروبات المتاحة للنشر المخفي.\n"
        "• <code>.مخصص [الثواني] [معرف الكروب]</code> : بالرد على رسالة لبدء النشر الصامت.\n"
        "• <code>.إيقاف النشر</code> : لإيقاف النشر المخفي.\n"
        "• <code>.وهمي [الثواني]</code> : لتثبيت حالة (متصل الآن) مستمرة."
    )
    await message.edit(panel_text)


# ==========================================
# 1. أداة عرض الكروبات (.تخصيص)
# ==========================================
@app.on_message(filters.me & filters.command("تخصيص", prefixes="."))
async def list_user_chats(client: Client, message: Message):
    await message.edit("<b>🔍 جاري جلب المجموعات التي أنت فيها...</b>")
    
    chats_list = "<b>📂 الكروبات والمجموعات المشترك فيها:</b>\n\n"
    count = 0
    
    async for dialog in client.get_dialogs():
        if dialog.chat.type in ["supergroup", "group"]:
            count += 1
            chat_name = dialog.chat.title
            chat_id = dialog.chat.id
            chats_list += f"📌 <b>{chat_name}</b>\n🆔 المعرف: <code>{chat_id}</code>\n\n"
            if count >= 30:
                chats_list += "<i>... (تم إظهار أول 30 مجموعة فقط)</i>"
                break
                
    if count == 0:
        chats_list = "<b>⚠️ لست عضواً في أي مجموعات حالياً.</b>"
        
    await message.edit(chats_list)


# ==========================================
# 2. أداة النشر الصامت والمخصص (.مخصص)
# ==========================================
@app.on_message(filters.me & filters.command("مخصص", prefixes="."))
async def silent_custom_post(client: Client, message: Message):
    args = message.text.split()
    
    if len(args) < 3:
        await message.edit(
            "<b>⚠️ خطأ في الاستخدام. الصيغة الصحيحة بالرد على الرسالة:</b>\n"
            "<code>.مخصص [الثواني] [معرف الكروب]</code>\n"
            "مثال: <code>.مخصص 20 -100123456789</code>"
        )
        return
        
    try:
        interval = int(args[1])
        target_chat = int(args[2]) if args[2].startswith("-") else args[2]
    except ValueError:
        await message.edit("<b>⚠️ تأكد من أن الثواني ورقم الكروب أرقام صحيحة.</b>")
        return
        
    if not message.reply_to_message:
        await message.edit("<b>⚠️ يجب الرد على الرسالة المراد نشرها!</b>")
        return
        
    target_msg = message.reply_to_message
    
    try:
        await message.delete()
    except Exception:
        pass
        
    active_custom_posts[target_chat] = True
    
    while active_custom_posts.get(target_chat, False):
        try:
            await target_msg.copy(target_chat)
            await asyncio.sleep(interval)
        except Exception as e:
            print(f"خطأ في النشر المخصص للكروب {target_chat}: {e}")
            break


# إيقاف النشر المخفي
@app.on_message(filters.me & filters.command("إيقاف النشر", prefixes="."))
async def stop_silent_post(client: Client, message: Message):
    active_custom_posts.clear()
    await message.edit("<b>🛑 تم إيقاف جميع عمليات النشر المخصصة بنجاح.</b>")
    await asyncio.sleep(3)
    try:
        await message.delete()
    except Exception:
        pass


# ==========================================
# 3. فحص الاتصال (.فحص)
# ==========================================
@app.on_message(filters.me & filters.command("فحص", prefixes="."))
async def ping_check(client: Client, message: Message):
    start_time = time.time()
    await message.edit("<b>⚡ جاري فحص الاتصال...</b>")
    end_time = time.time()
    ping_ms = round((end_time - start_time) * 1000, 2)
    await message.edit(f"<b>🟢 اليوزربوت يعمل بكفاءة! (Ping: {ping_ms} ms)</b>")
    await asyncio.sleep(3)
    try:
        await message.delete()
    except Exception:
        pass


# ==========================================
# 4. الحفظ الذاتي للوسائط ذاتية التدمير
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
                print(f"خطأ: {e}")

@app.on_message(filters.me & filters.command("تفعيل الذاتية", prefixes="."))
async def toggle_disappearing_save(client: Client, message: Message):
    current_state = getattr(client, "save_disappearing_active", False)
    client.save_disappearing_active = not current_state
    state_text = "<b>✅ تم تفعيل حفظ الوسائط ذاتية التدمير.</b>" if client.save_disappearing_active else "<b>❌ تم إيقاف حفظ الوسائط.</b>"
    await message.edit(state_text)
    await asyncio.sleep(3)
    try:
        await message.delete()
    except Exception:
        pass


# ==========================================
# 5. النشاط الوهمي (تثبيت حالة متصل الآن بدون "يلعب")
# ==========================================
@app.on_message(filters.me & filters.command("وهمي", prefixes="."))
async def fake_playing_status(client: Client, message: Message):
    args = message.text.split()
    duration = 60  # المدة الافتراضية بالثواني إذا لم تُكتب
    
    if len(args) > 1 and args[1].isdigit():
        duration = int(args[1])

    try:
        await message.delete()
    except Exception:
        pass
        
    try:
        from pyrogram.raw.functions.account import UpdateStatus
        start_time = time.time()
        while time.time() - start_time < duration:
            await client.invoke(UpdateStatus(offline=False))
            await asyncio.sleep(10)
    except Exception as e:
        print(f"خطأ في تثبيت حالة الاتصال: {e}")


# تشغيل البوت
print("🤖 اليوزربوت يعمل الآن بكفاءة...")
app.run()