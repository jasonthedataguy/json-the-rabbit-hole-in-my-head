"""Encode an existing local scene-loop video as a fixed-palette, infinite-loop GIF."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import tempfile
from fractions import Fraction
from PIL import Image, ImageChops, ImageStat


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video')
    parser.add_argument('--output', required=True)
    parser.add_argument('--ffmpeg', required=True)
    parser.add_argument('--duration', type=float, default=8)
    parser.add_argument('--fps', type=float, default=12.5)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    count = round(args.duration*args.fps)
    duration_ms = round(1000/args.fps)
    if count<2 or abs(duration_ms/10-round(duration_ms/10))>.0001:
        raise ValueError('Use a GIF cadence representable in 10ms ticks, such as 12.5 fps.')
    with tempfile.TemporaryDirectory(prefix='json-living-loop-') as directory:
        frame_dir = Path(directory)
        probe = Path(args.ffmpeg).with_name('ffprobe'+Path(args.ffmpeg).suffix)
        metadata = json.loads(subprocess.run([str(probe),'-v','error','-select_streams','v:0',
                              '-show_entries','stream=avg_frame_rate','-of','json',args.video],
                              capture_output=True,text=True,check=True).stdout)
        source_fps = float(Fraction(metadata['streams'][0]['avg_frame_rate']))
        decoded_count = round(args.duration*source_fps)
        # The bundled compositor FFmpeg omits the fps filter. Decode at native
        # cadence, then sample deterministically instead of requiring a new binary.
        subprocess.run([args.ffmpeg,'-v','error','-y','-i',args.video,
                        '-frames:v',str(decoded_count),str(frame_dir/'frame-%04d.png')],check=True)
        decoded_files = sorted(frame_dir.glob('frame-*.png'))
        if len(decoded_files)!=decoded_count:
            raise ValueError('Decoded loop frame count differs from requested duration.')
        files = [decoded_files[round(index*source_fps/args.fps)] for index in range(count)]
        frames = [Image.open(path).convert('RGB') for path in files]
        # One scene-wide palette prevents each frame choosing new colors.
        swatches = Image.new('RGB',(800,107*((count+4)//5)))
        for index,image in enumerate(frames):
            thumb = image.copy()
            thumb.thumbnail((160,107))
            swatches.paste(thumb,((index%5)*160,(index//5)*107))
        palette = swatches.quantize(colors=255,method=Image.Quantize.MEDIANCUT)
        # Error diffusion would amplify tiny codec differences into moving grain.
        # A fixed nearest-color palette plus transparent delta optimization keeps
        # the illustration stable and avoids storing a complete painting per frame.
        encoded = [image.quantize(palette=palette,dither=Image.Dither.NONE) for image in frames]
        colors = palette.getpalette()
        nearest_black = min(range(255),key=lambda index:sum(value*value for value in colors[index*3:index*3+3]))
        remap = list(range(255))+[nearest_black]
        encoded = [frame.point(remap) for frame in encoded]
        # Reserve index 255 for unchanged pixels. Explicit delta frames also work
        # with older Pillow versions whose optimize flag only shrinks palettes.
        delta_frames = [encoded[0]]
        for previous,current in zip(encoded,encoded[1:]):
            a = Image.frombytes('L',current.size,previous.tobytes())
            b = Image.frombytes('L',current.size,current.tobytes())
            unchanged = ImageChops.difference(a,b).point(lambda value:255 if value==0 else 0)
            delta = current.copy()
            delta.paste(255,mask=unchanged)
            delta_frames.append(delta)
        delta_frames[0].save(output,save_all=True,append_images=delta_frames[1:],duration=duration_ms,
                             loop=0,disposal=1,transparency=255,optimize=False)
        with Image.open(output) as gif:
            assert gif.n_frames==count and gif.info['loop']==0
            durations=[]
            decoded=[]
            for frame in range(gif.n_frames):
                gif.seek(frame)
                durations.append(gif.info['duration'])
                decoded.append(gif.convert('RGB'))
        for expected,actual in zip(encoded,decoded):
            assert ImageChops.difference(expected.convert('RGB'),actual).getbbox() is None,'GIF delta encoding changed scene pixels.'
        scores=[sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3 for a,b in zip(decoded,decoded[1:])]
        seam=sum(ImageStat.Stat(ImageChops.difference(decoded[-1],decoded[0])).mean)/3
        assert all(value>0 for value in scores),'GIF has repeated frozen frames.'
        assert sum(durations)==round(args.duration*1000),'GIF duration changed.'
        assert seam < max(scores)*2,'Loop boundary has a larger jump than ordinary frame motion.'
        report={'status':'pass','video':str(Path(args.video).resolve()),'video_sha256':digest(args.video),
                'gif':str(output.resolve()),'gif_sha256':digest(output),'frames':count,'resolution':list(decoded[0].size),
                'duration_ms':sum(durations),'frame_duration_ms':duration_ms,'infinite_loop':True,
                'fixed_palette':True,'minimum_adjacent_frame_difference':min(scores),
                'median_adjacent_frame_difference':statistics.median(scores),'maximum_adjacent_frame_difference':max(scores),
                'last_to_first_frame_difference':seam,'author_quality_approved':False,'public_release_approved':False}
        Path(args.report).parent.mkdir(parents=True,exist_ok=True)
        Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
