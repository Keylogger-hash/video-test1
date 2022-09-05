from video_processing_tasks.celery_init import celery
import redis 
from repository.services import update_fileinfo_redis_start_processing,update_fileinfo_processing_ready
import ffmpeg

@celery.task
def processing_video_resize(key,fileinfo,width,height):
    pathfilename = fileinfo["pathfilename"]
    update_fileinfo_redis_start_processing(key,fileinfo)
    ffmpeg.input(pathfilename).filter('scale',w=width,h=height).output(pathfilename).overwrite_output().run()
    update_fileinfo_redis_start_processing(key,fileinfo)

    return "success"