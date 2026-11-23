from django.contrib import admin
from game_tickets.models import*


@admin.register(Game)
class AdminGame(admin.ModelAdmin):
    list_display = ("id", "team1", "team2", "category")
    list_display_links = ["id", "team1", "team2"]
    search_fields = ["category", "team1", "team2"]
    list_filter = ["team1", "team2", "status"]


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ("id", "user", "count", "game")
    list_display_links = ["id", "user", "game"]
    search_fields = ["user", "game"]
    list_filter = ["count", "id", "user"]



@admin.register(Team)
class AdminTeam(admin.ModelAdmin):
    list_display = ("id", "name", "coach")
    list_display_links = ["id", "name"]
    search_fields = ["name", "coach", "stadium"]
    list_filter = ["name", "id"]



@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ["id", "name"]
    search_fields = ["name"]
    list_filter = ["name", "id"]