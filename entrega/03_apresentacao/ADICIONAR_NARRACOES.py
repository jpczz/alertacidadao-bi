"""Add the students' actual recordings to the 4:55 visual base. Never synthesizes voices."""
import argparse,json,subprocess,shutil,sys,tempfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--audio-dir',required=True);p.add_argument('--base',default=str(Path(__file__).with_name('Pitch_Base_Visual_4m55.mp4')));p.add_argument('--output',default='Pitch_Final_AlertaCidadao.mp4');a=p.parse_args()
if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):p.error('Install FFmpeg/ffprobe on PATH before running.')
if not Path(a.base).is_file():p.error('Visual base MP4 not found.')
segments=[('01_problema',45),('02_solucao',45),('03_demo',90),('04_negocio',60),('05_impacto',30),('06_time',25)]
inputs=[]
for stem,seconds in segments:
 files=[x for x in Path(a.audio_dir).glob(stem+'.*') if x.suffix.lower() in ('.wav','.mp3','.m4a','.aac','.mp4')]
 if len(files)!=1:p.error('Provide exactly one actual recording named '+stem+' with supported audio/video extension.')
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(files[0])],text=True))
 if not any(s['codec_type']=='audio' for s in info['streams']):p.error(stem+' has no audio track. Record the real participant.')
 duration=float(info['format']['duration'])
 if duration>seconds+.05:p.error(f'{stem} is {duration:.2f}s; maximum is {seconds}s. Re-record or edit without changing meaning.')
 inputs.append(files[0])
with tempfile.TemporaryDirectory(prefix='alerta_pitch_') as tmp:
 tmp=Path(tmp);clips=[]
 for (stem,seconds),src in zip(segments,inputs):
  dst=tmp/(stem+'.wav')
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(src),'-vn','-af',f'loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad,atrim=0:{seconds}','-ac','2','-c:a','pcm_s16le',str(dst)],check=True);clips.append(dst)
 listing=tmp/'audio.txt';listing.write_text('\n'.join("file '"+str(x)+"'" for x in clips))
 audio=tmp/'narracao.m4a';subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c:a','aac','-b:a','192k',str(audio)],check=True)
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',a.base,'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy','-t','295','-movflags','+faststart',a.output],check=True)
print('Created',a.output)
print('Review all voices, synchronization and participation before publishing. This tool cannot confirm who recorded each clip.')
