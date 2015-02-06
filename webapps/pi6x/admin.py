from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    pass
    
# Register your models here.

admin.site.register(Author, AuthorAdmin)