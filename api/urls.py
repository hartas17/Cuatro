from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import auth, dogwalker_view, owner_view, service_view

urlpatterns = [

    # Register
    url(r'^register_owner/$', auth.register_owner),
    url(r'^register_dogwalker/$', auth.register_dogwalker),

    # Login
    url(r'^login_owner/$', auth.login_owner),
    url(r'^login_dogwalker/$', auth.login_dogwalker),

    # Password
    url(r'^change_password/$', auth.change_password),
    url(r'^forgot_password/$', auth.recover_password),
    url(r'^reset_password/$', auth.PasswordResetView.as_view()),

    # DogWalkers
    url(r'^dogwalker/$', dogwalker_view.dogwalker_list),
    url(r'^dogwalker/(?P<pk>[0-9]+)$', dogwalker_view.dogwalker_detail),
    #url(r'^dogwalker_geo/$',) url para obtener los cuidadores filtrados por distancias
    url(r'^dogwalker_favorite/$', dogwalker_view.dogwalker_favorite),
    url(r'^dogwalker_favorite/(?P<pk>[0-9]+)$', dogwalker_view.dogwalker_delete),

    # Dog-Owner
    url(r'^dogs/$',owner_view.dog_list),
    url(r'^dog_owner/$',owner_view.dog_owner),

    # Services
    url(r'^service/$',service_view.service_list),
    url(r'^service_dogwalker/(?P<pk>[0-9]+)$', service_view.service_dogwalker),
    url(r'^service_active/$',service_view.service_active),

]

urlpatterns = format_suffix_patterns(urlpatterns)
