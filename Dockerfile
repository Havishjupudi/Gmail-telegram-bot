# Use an official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg

# Add Google Chrome repository & install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg && \
    echo 'deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    wget -q "https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip" -O chromedriver.zip && \
    unzip chromedriver.zip && \
    chmod +x chromedriver && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver.zip

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && pip install selenium webdriver-manager chromedriver-autoinstaller

# Expose the port (if needed for Telegram bot)
EXPOSE 8080

# Start the bot
CMD ["python", "bot.py"]
