from re import M
from django.db import models


class netmask(models.Model):
    input = models.GenericIPAddressField('Введенные данные', max_length=40, help_text='Адрес айпи с маской подсети')
    name = models.CharField('Название подсети', max_length=100, help_text='Название посети')
    mask = models.IntegerField('Значение Маски', default=None, help_text='Номер маски подсети')

    def __str__(self):
        return self.input

    class Meta:
        ordering = ["id"]
        verbose_name_plural = 'Адреса с маской подсети'


class Local_Scanner(models.Model):
    STATUS = (
        ('R', 'Red'),
        ('G', 'Green'),
        ('B', 'Blue'),
    )
    ip = models.CharField('Айпи адрес', max_length=100, help_text='Адресс IP')
    hostname = models.CharField('Имя хоста', max_length=100, default='-', help_text='Имя хоста')
    os = models.CharField('Операцонная система', max_length=100, default='N/a', help_text='OS')
    status = models.CharField('Статус', max_length=1, choices=STATUS, help_text='Статус')
    delay = models.FloatField('Задержка', default=0.000, help_text='Значение пинга в мс')
    mac = models.CharField('Мак адрес', max_length=100, default='None', help_text='Мак адрес')
    date = models.DateTimeField(auto_now_add=True)
    net = models.ForeignKey(netmask, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ip)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = 'Сканирование локальной сети'


class groupUp(models.Model):
    ip = models.CharField('Айпи адрес', default=None, max_length=100, help_text='Адресс IP')
    bool = models.BooleanField('Статус значения', default=True, help_text='Статус значения списка')

    def __str__(self):
        return str(self.ip)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = 'Групировка по подсетям для сканирования'