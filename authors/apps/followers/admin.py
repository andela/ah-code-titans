from django.contrib import admin

from authors.apps.followers.models import Follower

admin.site.register(Follower)
