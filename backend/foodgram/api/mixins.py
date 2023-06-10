from rest_framework import mixins, viewsets


class OnlyGetViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    pass
