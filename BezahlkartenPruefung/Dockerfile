# Verwenden Sie ein schlankes Python-Image als Basis
FROM python:3.12

# Installieren Sie die notwendigen Pakete (Chromium, ChromeDriver und andere Abhängigkeiten)
# Installieren Sie die notwendigen Pakete (Chromium, ChromeDriver, Xvfb und andere Abhängigkeiten)
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    xvfb \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libnspr4 \
    libnss3 \
    xdg-utils \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*


# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die Anforderungen in den Container
COPY requirements.txt /app/

# Installieren Sie die Abhängigkeiten global
RUN pip install --upgrade pip && pip install -r requirements.txt

# Kopieren Sie den Rest des Codes in den Container
COPY . /app

# Setzen Sie die Umgebungsvariablen für den Headless-Browser
ENV DISPLAY=:99

# Port für den Zugriff definieren
#EXPOSE 5000

## Führen Sie die Flask-App aus
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 & /usr/local/bin/python app.py"]
