import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Update, MessageReactionUpdated
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Your Telegram Bot Token
TOKEN = "7847989857:AAFC5poynH1BAUQ1n3Gl5TBjLzPkmCOsLlM"
GROUP_ID = -4770819017  # Replace with your Telegram group ID

# Function to check Gmail availability
def check_gmail(username):
    """Check if a Gmail username is available."""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Fix issues on some systems
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://accounts.google.com/signup/v2/webcreateaccount")
        wait = WebDriverWait(driver, 10)
        email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        
        email_input.send_keys(username)
        time.sleep(2)

        error_elements = driver.find_elements(By.CSS_SELECTOR, "div[aria-live='polite']")
        for error in error_elements:
            if "That username is taken" in error.text:
                driver.quit()
                return False  # Username is taken

        driver.quit()
        return True  # Username is available

    except Exception as e:
        print(f"Error checking Gmail: {e}")
        driver.quit()
        return False

# Function to generate a random Gmail username
def generate_gmail():
    words = ["alpha", "gamma", "nova", "matrix", "vortex", "quantum", "omega", "cypher"]
    num_part = random.randint(1000, 99999)
    letters = ''.join(random.choices(string.ascii_lowercase, k=3))
    special_char = random.choice(["", ".", "_"])
    return f"{random.choice(words)}{special_char}{num_part}{letters}"

# Telegram command to fetch available Gmail usernames
async def get_gmails(update: Update, context: CallbackContext):
    try:
        num = int(context.args[0]) if context.args else 1
        if num <= 0:
            await update.message.reply_text("Please enter a valid number (e.g., /gmails 5)")
            return

        await update.message.reply_text(f"🔍 Checking {num} available Gmail usernames...")

        count = 0
        while count < num:
            email = generate_gmail()
            if check_gmail(email):  # Blocking call (runs synchronously)
                sent_message = await update.message.reply_text(email)
                await context.bot.forward_message(chat_id=GROUP_ID, from_chat_id=update.message.chat_id, message_id=sent_message.message_id)
                count += 1
            time.sleep(3)  # Prevent Google from blocking requests

    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /gmails <number> (e.g., /gmails 5)")

# Function to delete message on reaction
async def delete_on_reaction(update: Update, context: CallbackContext):
    """Deletes a message if a user reacts with a thumbs-up emoji 👍."""
    if isinstance(update, MessageReactionUpdated):
        if update.old_reaction and update.new_reaction:
            for reaction in update.new_reaction:
                if reaction.emoji == "👍":
                    await context.bot.delete_message(chat_id=update.chat_id, message_id=update.message_id)

# Main function to start the bot
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("gmails", get_gmails))
    app.add_handler(MessageHandler(filters.ALL, delete_on_reaction))  # Handles all messages and checks reactions

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
