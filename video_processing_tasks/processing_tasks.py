from video_processing_tasks.celery_init import celery
import ffmpeg

@celery.task
def processing_video_resize(pathfilename,width,height):
    ffmpeg.input(pathfilename).filter('scale',w=width,h=height).output(pathfilename).overwrite_output().run()
    return "success"