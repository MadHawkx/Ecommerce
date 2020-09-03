from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )

    class Meta:
        model = Category


class ProductInline(admin.TabularInline):
    model = Product_Size_Color

# class  Product_Size_ColorAdmin(admin.ModelAdmin):
#     inline=[
#         ProductInline,
#     ]
#     list_display = ['__unicode__', 'price']
#     list_filter = ('price', 'quantity',)
#     list_editable = ('price', 'quantity', )

#     class Meta:
#         model=Product_size_color


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    inlines = [
        ProductInline,
    ]


admin.site.register(Product, ProductAdmin)

admin.site.register(Product_Size_Color)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Product_Images)
admin.site.register(Product_History)
