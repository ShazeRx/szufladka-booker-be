from rest_framework import serializers

from szufladka_app.models import Ksiazka


class KsiazkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ksiazka
        fields = "__all__"
        read_only_fields = ('id',)

    def to_representation(self, instance: Ksiazka):
        """Wyciecie pola posiadacza (wieksze security)"""
        odpowiedz = super(KsiazkaSerializer, self).to_representation(instance)
        odpowiedz.pop('posiadacz')
        return odpowiedz
