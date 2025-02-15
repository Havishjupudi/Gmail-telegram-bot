# Use an official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install system dependencies for Chrome & ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    google-chrome-stable && \
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    wget -q "https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip" -O chromedriver.zip && \
    unzip chromedriver.zip && \
    chmod +x chromedriver && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver.zip

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port (if needed for webhook-based Telegram bot)
EXPOSE 8080

# Start the bot
CMD ["python", "bot.py"]
