from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

    #Register
    url(r'^register_professors/$', professors_view.register_professors),
    url(r'^register_students/$', students_view.register_students),

    #Login
    url(r'^login_professor/$', professors_view.login),
    url(r'^login_student/$', students_view.login),



]

urlpatterns = format_suffix_patterns(urlpatterns)
