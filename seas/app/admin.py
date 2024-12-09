from django.contrib import admin

from seas.app.models import (
    CustomerEntity,
    CustomerMatchSeatEntity,
    MatchEntity,
    SeatEntity,
    SeatPriceEntity,
    SessionEntity,
    StadiumEntity,
)

admin.site.register(CustomerEntity)
admin.site.register(SessionEntity)
admin.site.register(MatchEntity)
admin.site.register(SeatEntity)
admin.site.register(StadiumEntity)
admin.site.register(SeatPriceEntity)
admin.site.register(CustomerMatchSeatEntity)
