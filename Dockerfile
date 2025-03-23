#usa un'immagine base ufficiale di python
FROM python:3.11-slim

#imposta una directory all'interno del containar
WORKDIR /app

#copia i file requirement.txt e main.py nella directory di lavoro
COPY requirements.txt .
COPY main.py .
COPY privkey.pem .
COPY fullchain.pem .

#installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt 

#esporto le variabili d'ambiente
EXPOSE 8443

#comando per avviare l'app
#CMD [ "python3", "bot.py" ]


