FROM python:3.9
WORKDIR /app

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./child .
RUN mkdir -p database
COPY database/database.py /app/database/database.py
EXPOSE 9000

# Set the entrypoint command to run both Flask apps
CMD ["python", "app.py"]

