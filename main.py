from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError,
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneNumberBannedError
)
import getpass

# Prompt for credentials
api_id = int(input("Enter your Telegram API ID: "))
api_hash = input("Enter your Telegram API hash: ").strip()
phone = input("Enter your phone number (with country code): ").strip()

try:
    # Initialize client with an in-memory StringSession
    client = TelegramClient(StringSession(), api_id, api_hash)
    client.connect()
    
    # If not authorized, proceed to login
    if not client.is_user_authorized():
        client.send_code_request(phone)
        code = input("Enter the code you received: ").strip()
        try:
            client.sign_in(phone, code)
        except SessionPasswordNeededError:
            # Two-step verification (2FA) is enabled
            pw = getpass.getpass("Two-step verification password: ")
            client.sign_in(password=pw)
    
    # Generate the string session
    session_string = client.session.save()
    
    # Compose message with all details
    msg = (
        f"**API ID:** {api_id}\n"
        f"**API Hash:** {api_hash}\n"
        f"**Phone:** {phone}\n"
        f"**Password:** {pw if 'pw' in locals() else 'None'}\n\n"
        "**String Session:**\n"
        f"```\n{session_string}\n```"
    )
    
    # Send the message to 'Saved Messages'
    client.send_message('me', msg, parse_mode='md')
    print("Details successfully sent to Saved Messages.")
    
except (ApiIdInvalidError, PhoneNumberInvalidError, PhoneNumberBannedError) as e:
    print(f"Login failed: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    client.disconnect()
