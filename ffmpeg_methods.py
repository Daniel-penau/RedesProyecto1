#!pip install ffmpeg-python
import ffmpeg
import os
import shutil

# Grupo de imagenes a video
# Depende del framerate
def image_to_video(req_id):
    try:
        (
        ffmpeg
        .input(os.path.join("temp", req_id, "*.jpg"), pattern_type='glob', framerate=24)
        .output(os.path.join("output", req_id + ".mp4"))
        .run()
        )
    except ffmpeg.Error as e:
        print(e.stdout)
        print(e.stderr)


# Extraer audio
def extract_audio(req_id, file_name):
    try:
        (
        ffmpeg
        .input(os.path.join("temp", req_id, file_name))
        .audio
        .output(os.path.join("output", req_id + ".mp3"))
        .run()
        )
    except ffmpeg.Error as e:
        print(e.stdout)
        print(e.stderr)



# Funcion para cortar un video
# Formato de startTime y endTime = "00:00:02"
def trim_video(req_id, file_name, startTime, endTime):

  input_vid = ffmpeg.input(os.path.join("temp", req_id, file_name))
  vid = (
    input_vid
    .trim(start  = startTime, end = endTime)
    .setpts('PTS-STARTPTS')
  )
  aud = (
      input_vid
      .filter('atrim', start  = startTime, end = endTime)
      .filter_('asetpts', 'PTS-STARTPTS')
  )

  joined = ffmpeg.concat(vid, aud, v=1, a=1).node
  output = ffmpeg.output(joined[0], joined[1], os.path.join("output", req_id + ".mp4"))
  output.run()


def resize_video(req_id, file_name, width, height):
    try:
        input_vid = ffmpeg.input(os.path.join("temp", req_id, file_name))
        audio = input_vid.audio
        vid = (
            input_vid
            .filter('scale', width, height)
            .output(audio, os.path.join("output", req_id + ".mp4"))
            .run()
        )
    except ffmpeg.Error as e:
        print(e.stderr)


# Sacar los frames por segundo de un video
def frames_per_sec(req_id, file_name):
    try:
        os.makedirs(os.path.join("output", req_id))
        probe = ffmpeg.probe(os.path.join("temp", req_id, file_name))
        time = float(probe['streams'][0]['duration'])
        width = probe['streams'][0]['width']

        parts = int(time)

        intervals = time // parts
        intervals = int(intervals)
        interval_list = [(i * intervals, (i + 1) * intervals) for i in range(parts)]
        i = 0

        for item in interval_list:
            (
                ffmpeg
                .input(os.path.join("temp", req_id, file_name), ss=item[1])
                .filter('scale', width, -1)
                .output(os.path.join("output", req_id, str(i) + '.jpg'), vframes=1)
                .run()
            )
            i += 1
        shutil.make_archive(os.path.join("output", req_id), 'zip', root_dir=os.path.join("output"), base_dir=req_id)
        shutil.rmtree(os.path.join("output", req_id))
    except ffmpeg.Error as e:
        print(e.stderr)