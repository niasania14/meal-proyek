# Menggunakan image python sebagai base
FROM python:3.9-slim

# Menetapkan direktori kerja di dalam container
WORKDIR /app

# Menyalin file requirements.txt ke dalam container
COPY requirements.txt /app/

# Menginstal dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode sumber ke dalam container
COPY . /app/

# Menentukan perintah untuk menjalankan aplikasi Flask
CMD ["python", "app.py"]

# Expose port untuk akses ke aplikasi
EXPOSE 5000
