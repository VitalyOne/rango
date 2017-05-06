from django.conf.urls import url
from rango import views

urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'^about/', views.about, name='about'),
url(r'^test/', views.test, name='test'),
url(r'^add_category/$', views.add_category, name='add_category'),
url(r'^register/$', views.register, name='register'),
url(r'^login/$', views.login_user, name='login_user'),
url(r'^about/$', views.about, name='about'),
url(r'^logout/$', views.logout_user, name='logout_user'),
url(r'category/(?P<category_name_slug>[\w\-]+)/add_page/', views.add_page, name="add_page"),
url(r'goto/', views.track_url, name="goto"),
url(r'gotoc/', views.track_cat, name="gotoc"),
url(r'category/(?P<category_name_slug>[\w\-]+)/$', views.category, name="category")
]
