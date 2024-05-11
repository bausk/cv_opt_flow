from typing import Optional
import click

from preprocessing.video_slicing import MP4VideoPreprocessor


@click.command()
@click.option('--image_path', required=True, type=str, help='Path to the input video file')
@click.option('--step', required=False, type=float, help='Interval between captured frames in seconds, each frame if not specified')
# @click.option('--crop', required=False, type=float, help='Percent of HFOV to retain, 100 percent by default')
# @click.option('--resize', required=False, type=int, help='Downsample ')
def main(image_path: str, step: Optional[float]):
    """
    Usage:
    $ python preprocess_video.py --image_path=xxx.MP4 --step=50
    Will produce video and images timelapsed with 50 seconds interval
    """
    preprocessor = MP4VideoPreprocessor(image_path, increment=step)
    preprocessor.process()

if __name__ == '__main__':
    main()
