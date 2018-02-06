from django.db import models

class AdminData(models.Model):
    welcome = models.CharField(max_length=1000, default="Witamy")
    thanks = models.CharField(max_length=1000, default="Dziękujemy")
    gilSessionTrainingDescription = models.CharField(max_length=1000, default="Witamy")
    gilSessionTrainingLengthSeconds = models.IntegerField(default=60)
    gilSessionMeasurementDescription = models.CharField(max_length=1000, default="Witamy")
    gilSessionMeasurementLengthSeconds = models.IntegerField(default=60)
    cardSessionTrainingDescription = models.CharField(max_length=1000, default="Witamy")
    cardSessionTrainingLengthSeconds = models.IntegerField(default=60)
    cardSessionMeasurementDescription = models.CharField(max_length=1000, default="Witamy")
    cardSessionMeasurementLengthSeconds = models.IntegerField(default=60)
    redBackgroundTimeSeconds = models.IntegerField(default=3)

class CardResult(models.Model):
    name = models.CharField(max_length=100)
    taskNumber = models.CharField(max_length=100)
    result = models.CharField(max_length=100)
    solutionTime = models.CharField(max_length=100)
    times = models.CharField(max_length=1000)

class Player(models.Model):
    SEX_CHOICES = (
        ('MAN', 'MAN'),
        ('WOMAN', 'WOMAN')
    )

    name = models.CharField(max_length=100, primary_key=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default="MAN")
    age = models.IntegerField()
    active = models.BooleanField()
    gilSessionTimes = models.CharField(max_length=1000, default="")