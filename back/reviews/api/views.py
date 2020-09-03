from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken import views
from rest_framework import viewsets, status
from rest_framework.response import Response
from reviews.models import Reviews
from products.models import Product
from rest_framework.decorators import action
from rest_framework import mixins
from reviews.api.serializers import ReviewSerializer
from rest_framework import permissions


class OwnerPermission(permissions.BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj here is a UserProfile instance
        return obj.user == request.user


class ReviewViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request):
        try:
            product = Product.objects.get(id=request.data['id'])
        except:
            return Response({'status': 'fail'})
        user = self.request.user
        review = Reviews.objects.create(
            user=user, product=product, userrating=request.data['userrating'], detail=request.data['detail'])
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    # @action(detail=True,methods=['put',])
    def update(self, request, pk=None):
        review = self.get_object()
        if(request.user != review.user):
            return HttpResponse('you are not allowed')
        else:
            try:
                product = Product.objects.get(id=request.data['id'])
            except:
                return Response({'status': 'fail'})
            user = self.request.user

            review.userrating = request.data['userrating']
            review.detail = request.data['detail']
            review.save()
            serializer = ReviewSerializer(review)
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if(request.user != instance.user):
            return HttpResponse('you are not allowed')
        else:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

# https://www.amazon.in/Ikigai-H%C3%A9ctor-Garc%C3%ADa/dp/178633089X/ref=zg_bs_books_home_2?_encoding=UTF8&psc=1&refRID=B8ZGXHNRKWX4QVRZMC4R
