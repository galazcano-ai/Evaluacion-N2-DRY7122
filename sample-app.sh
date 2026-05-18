#!/bin/bash

echo "Limpiando entorno anterior..."
docker stop samplerunning 2>/dev/null
docker rm samplerunning 2>/dev/null
docker rmi sampleapp 2>/dev/null
rm -rf tempdir
 
echo "Creando estructura temporal..."
mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static
 
echo "Copiando archivos de la aplicación..."
cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.
 
echo "Creando Dockerfile..."
echo "FROM python:3.10-slim" > tempdir/Dockerfile
echo "RUN pip install --no-cache-dir --progress-bar off flask" >> tempdir/Dockerfile
echo "COPY ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY sample_app.py /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 9999" >> tempdir/Dockerfile
echo "CMD python3 /home/myapp/sample_app.py" >> tempdir/Dockerfile
 
echo "Mostrando Dockerfile generado..."
cat tempdir/Dockerfile
 
echo "Construyendo imagen Docker..."
cd tempdir
docker build -t sampleapp .
 
echo "Ejecutando contenedor..."
docker run -t -d -p 9999:9999 --name samplerunning sampleapp
 
echo "Mostrando contenedores..."
docker ps -a
