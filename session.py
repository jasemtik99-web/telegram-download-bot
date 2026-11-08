from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# بيانات الحساب الخاصة بك
api_id = 32251310
api_hash = "055612b7ab440bae2c5ef96440c17737"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("\n=== نص الجلسة الخاص بك (انسخه كاملاً) ===")
    print(client.session.save())
    print("=========================================\n")