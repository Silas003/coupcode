from rest_framework import serializers
from .models import *


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bet
        fields=(
            "id",
            "date_time",
            "pc_selection",
            "result",
            "selection",
            "stake",
            "user",
            "stake_return",
        )
        # fields="__all__"
        read_only_fields=(
            "id",
            "date_time",
            "pc_selection",
            "result",
            "stake_return",
        )


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=History
        fields="__all__"
   