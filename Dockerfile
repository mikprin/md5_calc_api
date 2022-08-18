# 
FROM python:3.10
# 
WORKDIR /api/src
# 
COPY requirements.txt /api/requirements.txt
#
COPY .env  /api
#
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
# 
COPY src /api/src
#
COPY .env /api/.env
#
RUN mkdir -p /api/appdata
#
RUN mkdir  -p /api/logs
#
# CMD ["uvicorn", "main_upload_api:app", "--host", "0.0.0.0", "--port", "8000"]