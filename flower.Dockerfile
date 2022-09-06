FROM python:3.10.4-alpine3.15

# Get latest root certificates
RUN apk add --no-cache ca-certificates tzdata && update-ca-certificates &&\ 
    apk add ffmpeg  

EXPOSE 5555

RUN mkdir -p  /home/video-test1
WORKDIR /home/video-test1

COPY . .
RUN pip install -r requrirements.txt


CMD ["celery", "flower"]