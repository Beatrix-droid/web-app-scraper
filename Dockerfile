FROM python:3-alpine
RUN mkdir /kubernetes_flask_app
WORKDIR /kubernetes_flask_app
COPY requirements.txt /kubernetes_flask_app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /kubernetes_flask_app
EXPOSE 5000
CMD [ "python", "main.py" ]
