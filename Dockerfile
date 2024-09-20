# Usar una imagen base de Python
FROM python:3.9-slim

# Instalar dependencias del sistema necesarias (como PostgreSQL y gcc)
RUN apt-get update && apt-get install -y libpq-dev gcc

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación
COPY . /app

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usará Flask (5000 por defecto)
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python", "app.py"]
