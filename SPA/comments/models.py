import os
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
    def reduce_gif(self):
        # Open the GIF as a sequence of frames
        frames = []
        gif_image = Image.open(BytesIO(self.image.read()))
        try:
            while True:
                gif_image.seek(gif_image.tell() + 1)
                frames.append(gif_image.copy())
        except EOFError:
            pass
        # Resize each frame proportionally to fit within 320x240 box
        resized_frames = []
        for frame in frames:
            frame.thumbnail((320, 240), resample=Image.LANCZOS)
            frame.info = gif_image.info
            resized_frames.append(frame)
        # Save the resized frames as an animated GIF
        buffers = []
        for frame in resized_frames:
            buffer = BytesIO()
            frame.save(buffer, format='GIF')
            buffers.append(buffer)
        buffers[0].seek(0)
        resized_frames[0].save(
            self.image.name,
            save_all=True,
            append_images=resized_frames[1:],
            format='GIF',
            disposal=2,
            loop=0,
            optimize=True,
            transparency=0,
            duration=100,
            disposal_method=2,
            save_all_add=False,
            include_color_table=True,
        )
        self.image.save(self.image.name, ContentFile(buffers[0].getvalue()), save=False)

    def reduce_image_other_formats(self, ext):
        thumbnail_image = Image.open(BytesIO(self.image.read()))
        thumbnail_image.thumbnail((320, 240))
        buffer = BytesIO()
        thumbnail_image.save(buffer, format=ext)
        self.image.save(self.image.name, ContentFile(buffer.getvalue()), save=False)

    def reduce_image(self, ext):
        if ext == '.jpg':
            ext = '.jpeg'
        if ext == '.gif':
            self.reduce_gif()
        else:
            self.reduce_image_other_formats(ext.upper()[1:])

    def save(self, *args, **kwargs):
        if self.image:
            filename, extension = os.path.splitext(self.image.name)
            self.reduce_image(extension)

        if self.parent:
            self.level = self.parent.level + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.body[:50]

    def get_replies(self):
        return Comment.objects.filter(parent=self)

    class Meta:
        ordering = ['-created_time']
