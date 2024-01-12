from django.db import models

def assignment_upload_path(instance, filename):
    return f'Sassignments/{instance.key}/{filename}'


class Assingment(models.Model):
    Tname = models.CharField(max_length=50)
    T_iD = models.CharField(max_length=50)
    Aname = models.CharField(max_length=50)
    key = models.CharField(max_length=6, unique=True)
    deadline = models.DateTimeField()
    document = models.FileField(upload_to='assignments/')

    def __str__(self):
        return self.Tname


class Students_Assigments(models.Model):
    Sname = models.CharField(max_length=50)
    S_iD = models.CharField(max_length=50)
    key = models.CharField(max_length=6)
    document = models.FileField(upload_to=assignment_upload_path)

    def __str__(self):
        return self.Sname