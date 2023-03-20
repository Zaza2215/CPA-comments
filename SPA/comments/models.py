import os
import io
import datetime
import time

from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User


def get_upload_path(instance, filename):
    """Generate upload path for ImageField"""
    filename, ext = os.path.splitext(filename)
    filename = int(time.time())
    return f'{instance.__class__.__name__}/{datetime.datetime.today().strftime("%Y/%m")}/image_{filename}{ext}'


def thumbnail_gif(path_file: str, save_path: str, resolution: tuple):
    gif_image = Image.open(path_file)
    # Get options of gif
    options = {
        'loop': gif_image.info['loop'],
        'duration': gif_image.info['duration']
    }
    frames = []

    # Iterate over each frame in the GIF
    for frame in range(gif_image.n_frames):
        # Seek to the current frame
        gif_image.seek(frame)

        # Convert the current frame to JPEG format
        jpg_image = gif_image.convert("RGB")
        jpg_image.thumbnail(resolution)
        frames.append(jpg_image)

    frames[0].save(
        save_path,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        **options
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    level = models.PositiveIntegerField(default=0)

    # TODO: If the .gif's resolution is greater than 320x240 the animation will disappear

    def reduce_image_other_formats(self, ext):
        thumbnail_image = Image.open(BytesIO(self.image.read()))
        thumbnail_image.thumbnail((320, 240))
        buffer = BytesIO()
        thumbnail_image.save(buffer, format=ext)
        self.image.save(self.image.name, ContentFile(buffer.getvalue()), save=False)

    def reduce_image(self, ext):
        if ext == '.jpg':
            ext = '.jpeg'
        if ext != '.gif':
            self.reduce_image_other_formats(ext.upper()[1:])

    def save(self, *args, **kwargs):
        if self.image:
            filename, extension = os.path.splitext(self.image.name)
            self.reduce_image(extension)

        if self.parent:
            self.level = self.parent.level + 1

        super().save(*args, **kwargs)
        if extension == '.gif' and (self.image.width > 360 or self.image.height > 240):
            thumbnail_gif(str(self.image.path), str(self.image.path), (320, 240))

    def __str__(self):
        return self.body[:50]

    def get_replies(self):
        return Comment.objects.filter(parent=self)

    class Meta:
        ordering = ['-created_time']
