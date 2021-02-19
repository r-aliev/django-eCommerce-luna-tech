FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /ecom
COPY requirements.txt /ecom/
RUN pip install -r requirements.txt
RUN pip install Pillow
COPY . /ecom/