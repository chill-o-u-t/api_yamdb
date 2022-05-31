from rest_framework import viewsets
#from .permissions import IsAdminOrReadOnly

from reviews.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    pass
