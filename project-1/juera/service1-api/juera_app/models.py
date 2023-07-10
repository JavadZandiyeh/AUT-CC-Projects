from django.db import models


class Upload(models.Model):
    email = models.EmailField(max_length=100)
    inputs = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    enable = models.BooleanField(default=0)


class Job(models.Model):
    NONE = 'none'
    EXECUTED = 'executed'
    STATUS = [
        (NONE, 'none'),
        (EXECUTED, 'executed')
    ]

    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    job = models.CharField(max_length=10000)
    status = models.CharField(max_length=100, choices=STATUS, default=NONE)


class Result(models.Model):
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    STATUS = [
        (IN_PROGRESS, 'in_progress'),
        (DONE, 'done')
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    output = models.CharField(max_length=10000)
    status = models.CharField(max_length=100, choices=STATUS, default=IN_PROGRESS)
    executed_date = models.DateTimeField(auto_now_add=True)
