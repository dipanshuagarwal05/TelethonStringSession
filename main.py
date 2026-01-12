import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)

async def main():
    print("=== Telethon String Session Generator (CLI) ===\n")

    # ---- INPUTS ----
    try:
        api_id = int(input("Enter API_ID: ").strip())
    except ValueError:
        print("❌ API_ID must be an integer")
        return

    api_hash = input("Enter API_HASH: ").strip()
    phone = input("Enter PHONE NUMBER (with country code): ").strip()

    client = TelegramClient(StringSession(), api_id, api_hash)

    try:
        await client.connect()
        await client.send_code_request(phone)
        print("📨 OTP sent")
    except ApiIdInvalidError:
        print("❌ Invalid API_ID / API_HASH")
        return
    except PhoneNumberInvalidError:
        print("❌ Invalid phone number")
        return

    otp = input("Enter OTP (example: 1 2 3 4 5): ").replace(" ", "")

    two_fa_password = "NOT ENABLED"

    try:
        await client.sign_in(phone, otp)
    except PhoneCodeInvalidError:
        print("❌ Invalid OTP")
        return
    except PhoneCodeExpiredError:
        print("❌ OTP expired")
        return
    except SessionPasswordNeededError:
        two_fa_password = input("Enter 2FA password: ")
        try:
            await client.sign_in(password=two_fa_password)
        except PasswordHashInvalidError:
            print("❌ Invalid 2FA password")
            return

    # ---- STRING SESSION ----
    string_session = client.session.save()

    # ---- MESSAGE CONTENT ----
    text = f"""
🔐 **TELETHON STRING SESSION (FULL DETAILS)**

📱 **Phone Number**
`{phone}`

🆔 **API ID**
`{api_id}`

🔑 **API HASH**
`{api_hash}`

🔒 **2FA Password**
`{two_fa_password}`

🧵 **STRING SESSION**
`{string_session}`

⚠️ **DELETE THIS MESSAGE AFTER SAVING**
"""

    # ---- SEND TO SAVED MESSAGES ----
    await client.send_message("me", text)

    print("\n✅ Session generated successfully")
    print("\n📌 STRING SESSION:\n")
    print(string_session)
    print("\n📨 Full details sent to Saved Messages")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
