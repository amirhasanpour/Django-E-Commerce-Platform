from django.contrib import admin
from .models import Comment, Scoring



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'commenting_user', 'comment_text', 'is_active']
    list_editable = ['is_active']
    
    
    
@admin.register(Scoring)
class ScoringAdmin(admin.ModelAdmin):
    list_display = ['product', 'scoring_user', 'score']
