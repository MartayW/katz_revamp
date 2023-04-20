from django.contrib import admin
from .models import Cat
from .models import CatTest
from .models import User
from .models import Transaction
from .models import Breeder


# Register your models here.
admin.site.register(CatTest)
admin.site.register(User)
admin.site.register(Transaction)

