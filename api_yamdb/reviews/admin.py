from django.contrib import admin

from .models import Comment, Review, Title, User


class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'score',
        'author',
        'title'
    )
    search_fields = ('text', 'author__username')
    list_filter = ('score', 'title')
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'bio',
        'confirmation_code'
    )
    search_fields = ('username', 'email')
    list_filter = ('role',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'review_title'
    )

    def review_title(self, obj):
        return f'''
            Произведение: {Comment.objects.get(id=obj.id).review.title}.
            Автор обзора - {Comment.objects.get(id=obj.id).review.author}.
        '''

    review_title.short_description = 'Комментарий к обзору на произведение'

    search_fields = ('author__username', 'text')
    list_filter = ['author', 'review__title']
    empty_value_dispaly = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'title'
    )


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(Title)
admin.site.register(User, UserAdmin)
