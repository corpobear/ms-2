FROM python:3.11.7-bookworm

WORKDIR /usr/src/application


# Install Git
RUN apt-get update && apt-get install -y git

ENV ENVIRONMENT=cloud

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN openssl pkey -in first_shoe.pem -out key.pem
# RUN openssl crl2pkcs7 -nocrl -certfile first_shoe.pem | openssl pkcs7 -print_certs -out cert.crt

EXPOSE 8000

# RUN python manage.py update


# Run uvicorn dev server with SSL
CMD ["uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
