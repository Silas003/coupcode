from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from .models import *
from helper.utils import shuffle
from accounts.models import Profile
from django.db import transaction

class BetView(viewsets.ModelViewSet):
    """
    A viewset for handling bets.
    """
    queryset = Bet.objects.all()
    serializer_class = BetSerializer

    @transaction.atomic
    def perform_create(self, serializer: BetSerializer):
        """
        Perform the creation of a bet.
        
        This method is responsible for:
        - Saving the bet instance
        - Determining the result of the bet (won or lost)
        - Updating the user's profile with the stake return
        - Creating a new history entry for the user
        """
        instance = serializer.save()
        self._determine_bet_result(instance)
        self._update_user_profile(instance)
        self._create_history_entry(instance)
        return instance

    def _determine_bet_result(self, instance):
        """
        Determine the result of the bet (won or lost) and update the instance accordingly.
        """
        shuffled = shuffle()
        instance.pc_selection = shuffled
        if instance.selection == shuffled:
            instance.result = Bet.Results.WON
            instance.stake_return = instance.stake * 2
        else:
            instance.result = Bet.Results.LOST
            instance.stake_return = 0.0
        instance.save()

    def _update_user_profile(self, instance):
        """
        Update the user's profile with the stake return.
        """
        user_profile = Profile.objects.filter(user=instance.user).first()
        if user_profile:
            user_profile.amount_won += instance.stake_return
            user_profile.save()

    def _create_history_entry(self, instance):
        """
        Create a new history entry for the user.
        """
        history = History.objects.create(user=instance.user)
        history.previous_bets.set([instance])
        history.save()


class HistoryView(viewsets.ModelViewSet):
    """
    A viewset for viewing previous bets of authenticated users.
    """
    serializer_class=HistorySerializer
    queryset=History.objects.all()