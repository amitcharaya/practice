from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from supply_chain.models import Demand
from supply_chain.serializers import DemandSerializer

class ReadCreateDemandViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    """
    Allows listing, viewing details, and creating demands. 
    Updates (PUT/PATCH) and deletion (DELETE) are completely disabled.
    """
    queryset = Demand.objects.all()
    serializer_class = DemandSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )