FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /quiz_app

COPY requirements.txt /quiz_app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY quiz_app/ ./

#CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]


