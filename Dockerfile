FROM python:3.10


RUN mkdir -p  /home/video-test1
WORKDIR /home/video-test1

COPY . .
RUN pip install -r requrirements.txt

ENTRYPOINT [ "uvicorn","main:app","--reload"]