FROM python:3-onbuild

WORKDIR C:/Users/User/Desktop/order_pineapple

COPY main.py .

RUN pip install requirements.txt

CMD ["python", "main.py"]