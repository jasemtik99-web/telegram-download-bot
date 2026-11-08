from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
import asyncio
import datetime
import os

# --- إعدادات الحساب الخاصة بك ---
api_id = 32251310
api_hash = '055612b7ab440bae2c5ef96440c17737'

# سلسلة الجلسة الخاصة بك التي أضفتها
string_session = 'AgHsHa4ASadFi903MuDVw7f0z7ZclCHawQhW94sRdRsnRvCToiEY43rIfH7O7sdnaOlitgZfPT93uZ4avrz01fJu8neBeEHseNfTPlaeIMLZJKt0lePM_qECpkR_gSodAaJMTi9wjDU5SbscvZNOc-AE-Vq0kHZ1i0h2j6j4A-CVTKnDebJu4ysd9jF0rcPFzxo2_ShOh-cCfdWR0RxNgq7ct-6wW8uJ4rfmDhhiygAbDjHAaMeavaSNoqD6Fm4HJFcLyREr_TNlKRYYZDKekb6P27Fb4cfAzSQ4SKJx2b1rOL0jq2r31zXs7FeWBZEUqPjQLV8BbVo-fnwFwDnoAjC8gf4J1AAAAAH7Q5fAAA'

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# متغيرات النظام (Global Variables)
private_lock = False
whitelisted_users = []
warnings = {}
storage_chat = None
auto_save_media = False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. القوائم والواجهات (Menus)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@client.on(events.NewMessage(outgoing=True, pattern=r'\.امر'))
async def main_menu(event):
    menu_text = """⚡ **سورس نوح - النسخة المتكاملة**

━━━━━━━━━━━━━━━━━━

• `.م1` ⬅️ النشر والتكرار

• `.م2` ⬅️ الحماية والخصوصية

• `.م4` ⬅️ الحالات الوهمية

• `.م5` ⬅️ حفظ الذاتية

• `.م6` ⬅️ مراقبة الأشخاص

• `.م7` ⬅️ التخزين والمستودع

━━━━━━━━━━━━━━━━━━

• `.حذف` ⇠ تنظيف رسائلك هنا

• `.فحص` ⇠ حالة اتصال السورس

━━━━━━━━━━━━━━━━━━

👤 المطور: نوح محمد ابراهيم"""
    await event.edit(menu_text)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.م1'))
async def sub_menu_m1(event):
    text = """**قسم النشر والتكرار (.م1)**

━━━━━━━━━━━━━━━━━━

• `.ن` + عدد + ثواني + اسم الجروب

• `.مجموعاتي` ⬅️ عرض الأسماء والايديات"""
    await event.edit(text)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.م2'))
async def sub_menu_m2(event):
    text = """**قسم الحماية والخصوصية (.م2)**

━━━━━━━━━━━━━━━━━━

• `.قفل` ⬅️ قفل الخاص

• `.فتح` ⬅️ إلغاء قفل الخاص

• `.قبول` ⬅️ (بالرد) السماح للشخص

• `.تحذير` ⬅️ (بالرد) نظام التحذيرات"""
    await event.edit(text)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.م4'))
async def sub_menu_m4(event):
    text = """**قسم الحالات الوهمية (.م4)**

━━━━━━━━━━━━━━━━━━

• `.لعب` + ثواني ⬅️ يظهر "يلعب الآن"

• `.تسجيل` + ثواني ⬅️ يظهر "يسجل صوتية" """
    await event.edit(text)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.م5'))
async def sub_menu_m5(event):
    text = """**قسم حفظ الذاتية (.م5)**

━━━━━━━━━━━━━━━━━━

• `.تفعيل_ذاتيه` ⬅️ حفظ تلقائي للميديا

• `.ضيم` ⬅️ (بالرد) حفظ الميديا المقيدة"""
    await event.edit(text)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.م7'))
async def sub_menu_m7(event):
    text = """**التخزين والمستودع (.م7)**

━━━━━━━━━━━━━━━━━━

• `.تخزين` ⬅️ جعل المجموعة الحالية مستودعاً

(يتم حفظ أي تاغ عليك هنا تلقائياً)"""
    await event.edit(text)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. الدوال البرمجية (Logic)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# --- [قسم م1: النشر ومجموعاتي] ---
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ن (\d+) (\d+) (.+)'))
async def auto_post_logic(event):
    count, delay, group_target = int(event.pattern_match.group(1)), int(event.pattern_match.group(2)), event.pattern_match.group(3).strip()
    found = False
    async for dialog in client.iter_dialogs():
        if group_target in dialog.name or group_target == str(dialog.id):
            found = True
            await event.delete()
            for i in range(count):
                await client.send_message(dialog.id, f"⚡ سورس نوح للنشر التلقائي\nالرسالة رقم: {i+1}")
                await asyncio.sleep(delay)
            break
    if not found: await event.edit(f"❌ لم يتم العثور على الجروب: {group_target}")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.مجموعاتي'))
async def list_groups(event):
    output = "**قائمة مجموعاتك:**\n"
    async for dialog in client.iter_dialogs():
        if dialog.is_group: output += f"• `{dialog.name}` | `{dialog.id}`\n"
    await event.edit(output)

# --- [قسم م2: الحماية والتحذير] ---
@client.on(events.NewMessage(outgoing=True, pattern=r'\.قفل'))
async def lock_pm(event):
    global private_lock
    private_lock = True
    await event.edit("🔒 تم قفل الخاص بنجاح.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.فتح'))
async def unlock_pm(event):
    global private_lock
    private_lock = False
    await event.edit("🔓 تم فتح الخاص.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.تحذير'))
async def warning_system(event):
    reply = await event.get_reply_message()
    if not reply: return await event.edit("⚠️ قم بالرد على الشخص لتحذيره")
    user_id = reply.sender_id
    warnings[user_id] = warnings.get(user_id, 0) + 1
    if warnings[user_id] >= 3:
        await client(functions.contacts.BlockRequest(user_id))
        await event.edit("🚫 تم حظره لتجاوز 3 تحذيرات.")
    else:
        await event.edit(f"⚠️ تحذير رقم ({warnings[user_id]}/3)")

# --- [قسم م4: الحالات الوهمية] ---
@client.on(events.NewMessage(outgoing=True, pattern=r'\.(لعب|تسجيل) (\d+)'))
async def fake_status(event):
    action, duration = event.pattern_match.group(1), int(event.pattern_match.group(2))
    status = types.SendMessageGamePlayAction() if action == "لعب" else types.SendMessageRecordAudioAction()
    await event.delete()
    async with client.action(event.chat_id, status):
        await asyncio.sleep(duration)

# --- [قسم م5: حفظ الذاتية] ---
@client.on(events.NewMessage(outgoing=True, pattern=r'\.تفعيل_ذاتيه'))
async def toggle_media_save(event):
    global auto_save_media
    auto_save_media = not auto_save_media
    await event.edit(f"📥 حفظ الميديا الذاتية: {'✅ مفعل' if auto_save_media else '❌ معطل'}")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.ضيم'))
async def save_restricted(event):
    reply = await event.get_reply_message()
    if reply and (reply.photo or reply.video or reply.voice):
        await event.edit("⏳ جاري الحفظ...")
        file = await reply.download_media()
        await client.send_file('me', file, caption="✅ تم حفظ الميديا بنجاح")
        await event.delete()
        if os.path.exists(file): os.remove(file)
    else: await event.edit("⚠️ رد على ميديا مقيدة أولاً.")

# --- [قسم م7: التخزين والمستودع] ---
@client.on(events.NewMessage(outgoing=True, pattern=r'\.تخزين'))
async def set_storage(event):
    global storage_chat
    storage_chat = event.chat_id
    await event.edit("✅ تم تعيين هذه المجموعة كمستودع للتاغات.")

# --- [مراقبات الخلفية (Watchers)] ---
@client.on(events.NewMessage(incoming=True))
async def global_watcher(event):
    # مراقب قفل الخاص
    if private_lock and event.is_private and event.sender_id not in whitelisted_users:
        if not (await event.get_sender()).bot: await event.delete()
    
    # مراقب المستودع (التاغات)
    if storage_chat and event.mentioned:
        await event.forward_to(storage_chat)
    
    # مراقب الميديا الذاتية
    if auto_save_media and event.is_private and (event.photo or event.video):
        file = await event.download_media()
        await client.send_file('me', file, caption="📸 ميديا ذاتية تم حفظها.")
        if os.path.exists(file): os.remove(file)

# --- [أوامر عامة: فحص وحذف] ---
@client.on(events.NewMessage(outgoing=True, pattern=r'\.فحص'))
async def ping(event):
    start = datetime.datetime.now()
    await event.edit("• جارٍ الفحص...")
    ms = (datetime.datetime.now() - start).microseconds / 1000
    await event.edit(f"✅ سورس نوح يعمل بنجاح | الاستجابة: `{ms}ms`")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.حذف'))
async def purge_msgs(event):
    await event.delete()
    async for msg in client.iter_messages(event.chat_id, from_user='me', limit=100):
        await msg.delete()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# تشغيل السورس وحفظ الجلسة
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("--- Noah Userbot is running ---")
client.start()
client.run_until_disconnected()