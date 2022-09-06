from video_processing_tasks.celery_init import celery
import os
from pathlib import Path
from repository.services import update_fileinfo_redis_start_processing,update_fileinfo_processing_ready
import ffmpeg

@celery.task
def processing_video_resize(key,fileinfo,width,height):
    pathfilename = fileinfo["pathfilename"]
    path_object = Path(pathfilename)
    stem = path_object.stem+"1"
    suffix = path_object.suffix
    parent = path_object.parent
    output_pathfilename = os.path.join(parent,f"{stem}{suffix}")
    update_fileinfo_redis_start_processing(key,fileinfo)
    vid = ffmpeg.input(pathfilename).video.filter('scale',width,height,force_original_aspect_ratio='decrease').filter('pad', str(width), str(height), '(ow-iw)/2', '(oh-ih)/2')
    aud = ffmpeg.input(pathfilename).audio
    aspect = ffmpeg.concat(vid,aud,v=1,a=1)
    out = ffmpeg.output(vid,aud,output_pathfilename)
    out.run()
    os.remove(pathfilename)
    os.rename(output_pathfilename,pathfilename)
    update_fileinfo_processing_ready(key,fileinfo)

    return "success"