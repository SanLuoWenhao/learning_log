from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Topic(models.Model):
    """
    用户学习主题
    """
    ower = models.ForeignKey(User, on_delete=False)
    test = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """s
        返回模型的字符串表示
        :return:
        """
        return self.test

class Entry(models.Model):
    """
    学到的有关某个主题的具体知识
    """
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text