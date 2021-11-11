FROM python:3.9.7
WORKDIR /app 
COPY . .
RUN pip install .
ENTRYPOINT ["wav2csv"]
