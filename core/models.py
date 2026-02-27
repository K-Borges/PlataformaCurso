from django.db import models


class SubjectChoices(models.TextChoices):
    BIOLOGIA = "biologia", "Biologia"
    FISICA = "fisica", "Física"
    MATEMATICA = "matematica", "Matemática"
    QUIMICA = "quimica", "Química"
    HISTORIA = "historia", "História"
    GEOGRAFIA = "geografia", "Geografia"
    PORTUGUES = "portugues", "Língua Portuguesa"


class LiveConfig(models.Model):
    subject = models.CharField(
        max_length=20,
        choices=SubjectChoices.choices,
        unique=True,
    )
    live_url = models.URLField("Link da aula ao vivo", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuração de aula ao vivo"
        verbose_name_plural = "Configurações de aulas ao vivo"

    def __str__(self) -> str:
        return f"{self.get_subject_display()} - {self.live_url or 'sem link'}"


class Notice(models.Model):
    subject = models.CharField(
        max_length=20,
        choices=SubjectChoices.choices,
    )
    message = models.TextField("Mensagem")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Aviso"
        verbose_name_plural = "Avisos"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"[{self.get_subject_display()}] {self.message[:40]}"

