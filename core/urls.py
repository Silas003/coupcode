from rest_framework.routers import DefaultRouter
from .views import *


router=DefaultRouter()
app_name="core"

router.register("place-bet",BetView,basename="bet")
router.register("history",HistoryView,basename="history")

urlpatterns=[]

urlpatterns+=router.urls