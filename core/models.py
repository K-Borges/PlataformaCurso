from django.db import models


# Create your models here.
class ListaExercicios(models.Model):
    titulo = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to="listas/")
    materia = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
