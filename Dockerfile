# 
FROM python:3.10
# 
WORKDIR /api/src
# 
COPY requirements.txt /api/requirements.txt
# 
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
# 
COPY src /api/src
#
RUN mkdir -p /api/appdata
# 
CMD ["uvicorn", "main_upload_api:app", "--host", "0.0.0.0", "--port", "8000"]