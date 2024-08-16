FROM python:3.10-slim-bullseye
COPY requirement.txt requirement.txt
RUN pip install --no-cache-dir -r requirement.txt
COPY . code
WORKDIR /code
EXPOSE 8000
RUN python 
# runs the production server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]