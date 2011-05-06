import models

class Hero(models.Model):
    Name = models.TextField(default='kailash')
    Type = models.TextField(default='Hero')

class Movie(models.Model):
    Name = models.TextField(default='3Idiots')
    Hero = models.RelationField(relation='MEMBER', cls = Hero)

m = Movie()
h = Hero()
m.Hero = h
m.save()
