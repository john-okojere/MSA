# admin.py
from django.contrib import admin
from .models import Chat, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

class ChatAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    inlines = [MessageInline]

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message)
