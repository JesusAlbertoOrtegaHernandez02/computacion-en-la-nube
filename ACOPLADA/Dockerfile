
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el fichero de dependencias y lo instalamos
COPY app/requirements.txt .

# Instalación sin caché para reducir tamaño
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente de la aplicación
COPY app/ .

# Variable de entorno opcional (modo producción)
ENV FLASK_ENV=production

# Puerto donde Flask escuchará
EXPOSE 8080

# Comando de arranque
CMD ["python", "main.py"]
