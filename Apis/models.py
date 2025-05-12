from django.db import models
# from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=80)
    img_url = models.URLField()
    content = models.TextField()
    likes = models.IntegerField(default=0)
    # owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title[0:20] + "..." if len(self.title) > 20 else self.title