from rest_framework import serializers
from products.models import Product_Size_Color, Category, Size, Color, Product, Product_Images
from reviews.models import Reviews
from reviews.api.serializers import ReviewSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('__all__')


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('__all__')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Images
        fields = ('__all__')


class ProductSizeColorSerializer(serializers.ModelSerializer):
   # supplier=serializers.RelatedField(source="product__supplier",read_only=True)
    class Meta:
        model = Product_Size_Color
        fields = (
            "id",
            "price",
            "quantity",
            "size",
            "color",
        )


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    product_size_color_set = ProductSizeColorSerializer(many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'brand', 'staffRecommended',
                  'discount', 'description', 'product_size_color_set', 'reviews')

    def create(self, validated_data):
        details = validated_data.pop('product_size_color_set')
        categories = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        for i in categories:
            product.category.add(i)
        #product= Product.objects.create(**validated_data)
        for product_size_color_data in details:
            product_size_color_data['product'] = product
            Product_Size_Color.objects.create(**product_size_color_data)
        return product

    def update(self, instance, validated_data):
        product_size_color_data = validated_data.pop('product_size_color_set')
        categories = validated_data.pop('category')
        product_size_color = (instance.product_size_color_set).all()
        product_size_color = list(product_size_color)
        instance.name = validated_data.get('name', instance.name)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.staffRecommended = validated_data.get(
            'staffRecommended', instance.staffRecommended)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.discount = validated_data.get('discount', instance.discount)

        for i in categories:
            if i not in instance.category.all():
                instance.category.add(i)
        for j in instance.category.all():
            if j not in categories:
                instance.category.remove(j)
        instance.save()

        for p in product_size_color_data:
            # psc="Null"
            if len(product_size_color) > 0:
                psc = product_size_color.pop(0)
                psc.price = p.get('price', psc.price)
                psc.quantity = p.get('quantity', psc.quantity)
                psc.size = p.get('size', psc.size)
                psc.color = p.get('color', psc.color)
                psc.save()
            else:
                p['product'] = instance
                Product_Size_Color.objects.create(**p)

        return instance

# https://stackoverflow.com/questions/37713901/django-rest-framework-how-to-post-nested-object-with-parent-object
# https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc?hl=en
