from django.contrib import admin


# Register your models here.

from team.models import Player


@admin.action(description="Change position to Goal Keeper")
def change_position_goalkeeper(modeladmin, request, queryset):
    queryset.update(position="goalkeeper")
@admin.action(description="Change position to Forward")
def change_position_forward(modeladmin, request, queryset):
    queryset.update(position="forward")
@admin.action(description="Change position to Defense")
def change_position_midfielder(modeladmin, request, queryset):
    queryset.update(position="defense")
@admin.action(description="Change position to Striker")
def change_position_defence(modeladmin, request, queryset):
    queryset.update(position="striker")
@admin.action(description="Change position to Substitute")
def change_position_substitute(modeladmin, request, queryset):
    queryset.update(position="substitute")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "age"]
    search_fields = ["name", "position"]
    list_filter = ["position", "age"]
    list_display_links = list_display
    actions = [change_position_goalkeeper,
               change_position_forward,
               change_position_midfielder,
               change_position_defence,
               change_position_substitute]
 