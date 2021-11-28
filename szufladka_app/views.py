from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from szufladka_app.models import Ksiazka
from szufladka_app.serializers import KsiazkaSerializer


class KsiazkaView(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = KsiazkaSerializer
    queryset = Ksiazka.objects.all()

    def list(self, request, *args, **kwargs):
        """Wyswietla wszystkie ksiazki"""
        query_type = request.query_params.get('ktore')
        user = request.user
        if query_type == 'moje':
            lista_ksiazek = self.queryset.filter(posiadacz=user)
            serializer_data = self.get_serializer(lista_ksiazek, many=True).data
            return Response(serializer_data, 200)
        lista_ksiazek = self.queryset.filter(posiadacz__isnull=True)
        serializer_data = self.get_serializer(lista_ksiazek, many=True).data
        return Response(serializer_data, 200)

    @action(methods=['patch'], detail=True)
    def wez(self, request, *args, **kwargs):
        """Bierze ksiazke do profilu jezeli nie ma posiadacza"""
        ksiazka_id = kwargs.get('pk')
        ksiazka = self.queryset.filter(Q(indeks=ksiazka_id), Q(posiadacz__isnull=True)).first()
        if ksiazka:
            serializer = self.get_serializer(instance=ksiazka)
            ksiazka.posiadacz = self.request.user
            ksiazka.save(update_fields=['posiadacz'])
            return Response(serializer.data, 200)
        return Response(status=401)

    @action(methods=['patch'], detail=True)
    def oddaj(self, request, *args, **kwargs):
        """Oddaje ksiazke jezli ma ja posiadacz"""
        ksiazka_id = kwargs.get('pk')
        ksiazka = self.queryset.filter(Q(indeks=ksiazka_id),
                                       Q(posiadacz=self.request.user)).first()
        if ksiazka:
            serializer = self.get_serializer(instance=ksiazka)
            ksiazka.posiadacz = None
            ksiazka.save(update_fields=['posiadacz'])
            return Response(serializer.data, 200)
        return Response(status=401)
