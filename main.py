from telethon import TelegramClient
from telethon.sessions import StringSession
from getpass import getpass
import asyncio

async def main():
    print("=== Telethon String Session Generator ===\n")

    # User inputs
    api_id = int(input("Enter API ID: ").strip())
    api_hash = input("Enter API Hash: ").strip()
    phone = input("Enter Phone Number (with country code): ").strip()

    use_2fa = input("Is 2FA enabled? (y/n): ").lower().strip()
    password = None
    if use_2fa == "y":
        password = getpass("Enter 2FA Password (hidden): ")

    # Create client with StringSession
    client = TelegramClient(StringSession(), api_id, api_hash)

    # Start login
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input("Enter OTP received on Telegram: ").strip()
        try:
            await client.sign_in(phone=phone, code=code)
        except Exception:
            if password:
                await client.sign_in(password=password)
            else:
                raise RuntimeError("2FA enabled but password not provided")

    # Get string session
    string_session = client.session.save()

    # Prepare message
    message = f"""
📌 **Telethon String Session Details**

📱 Phone Number:
{phone}

🆔 API ID:
{api_id}

🔑 API Hash:
{api_hash}

🔐 2FA Password:
{password if password else "Not Enabled"}

🧵 String Session:
{string_session}

⚠️ **Keep this information PRIVATE**
"""

    # Send to Saved Messages
    await client.send_message("me", message)

    print("\n✅ String session generated and sent to Saved Messages.")
    print("⚠️ Keep it secure. Anyone with this can access your Telegram.")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
