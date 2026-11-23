from django.db import models
from django.contrib.auth.models import User







class Leauge(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)





class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='images')
    description = models.TextField()
    stadium = models.CharField(max_length=100)
    stadium_image = models.ImageField(upload_to='images')
    coach = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    league = models.ForeignKey(Leauge, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    STATUS = (
        ('not_started', 'Not started'),
        ('live', 'Live'),
        ('finished', 'Finished'),
    )

    TICKET_STATUS = {
        "available" : "Available",
        "out_sale": "Out of sale",
        "unvailable": "Unvailable" 
    }

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_games')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_games')
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='not_started')
    image = models.ImageField(upload_to='images')
    video = models.FileField(upload_to='videos', blank=True, null=True)
    stadium = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    tickets = models.IntegerField()
    tickets_status = models.CharField(max_length=20, choices=TICKET_STATUS, default="available")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    count = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.game}'

