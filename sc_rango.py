import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import *
def add_cat(name, views=0, likes=0):
	c = Category.objects.get_or_create(name=name)[0]
	c.views=views
	c.likes=likes
	c.save()
	return c

def add_page(cat, title, url, views=0):
	p = Page.objects.get_or_create(category=cat, title=title)[0]
	p.url=url
	p.views=views
	p.save()
	return p

def populate():
	python_cat = add_cat(name='Python', views=128, likes=64)

	add_page(cat=python_cat, title='Python Tutorial', url='python.org', views = 500)
	add_page(cat=python_cat, title='Python for DUMMIES', url='dummies-python.ru', views = 200)
	add_page(cat=python_cat, title='Python 10 min', url='life-10.ru')

	django_cat = add_cat(name='Django', views=64, likes=32)

	add_page(cat=django_cat, title='tango_with_django_project', url='tango_with_django_project.org', views=600)
	add_page(cat=django_cat, title='tango tutorial', url='django.org', views = 300)
	add_page(cat=django_cat, title='Django 1.10', url='django-hard.ru')

	frame_cat = add_cat(name='Other frameworks', views=32, likes=16)

	add_page(cat=frame_cat, title='Flask', url='flask.org', views = 400)
	add_page(cat=frame_cat, title='Bottle', url='Bottle.ru')

	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print(str(c)+' - ' + str(p))

if __name__== '__main__':
	print('Start sc to complete db...')
	populate()