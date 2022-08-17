# 
FROM python:3.10
# 
WORKDIR /code/api
# 
COPY requirements.txt /code/requirements.txt
# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# 
COPY src /code/api
# 
CMD ["uvicorn", "main_upload_api:app", "--host", "0.0.0.0", "--port", "8000"]