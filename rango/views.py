from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import *
from django.shortcuts import redirect
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, TestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
	cont={}
	cat_list=Category.objects.order_by('-likes')[:5]
	cont['categories'] = cat_list
	pag_list=Page.objects.order_by('-views')[:5]
	cont['pages'] = pag_list

	#visits = int(request.COOKIES.get('visits'))
	"""if 'visits' in request.COOKIES:
		visits = int(request.COOKIES['visits'])
	else:
		visits = 1
	cont['visits'] = visits

	reset_last_visit_time = False


	response = render(request, 'index.html', cont)
	
	if 'last_visit' in request.COOKIES:
		last_visit = request.COOKIES['last_visit']
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		if (datetime.now() - last_visit_time).seconds > 0:
			visits = visits + 1
			cont['visits'] = visits
			reset_last_visit_time = True
	else:
		reset_last_visit_time = True
		cont['visits'] = visits
		response = render(request, 'index.html', cont)

	if reset_last_visit_time:
		response.set_cookie('last_visit', datetime.now())
		response.set_cookie('visits', visits)

	return response"""
	visits = request.session.get('visits')
	if not visits:
		visits = 1
	reset_last_visit_time = False
	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
			visits = visits + 1
            # ...and update the last visit cookie, too.
			reset_last_visit_time = True
	else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
		reset_last_visit_time = True

	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits
	cont['visits'] = visits


	response = render(request,'index.html', cont)

	return response


def category(request, category_name_slug):
	contex_dict={}

	try:
		category = Category.objects.get(slug=category_name_slug)
		contex_dict['category_name'] = category.name

		pages = Page.objects.filter(category = category).order_by('-views')
		contex_dict['pages'] = pages
		contex_dict['category'] = category
		contex_dict['category_name_slug'] = category_name_slug
	except Category.DoesNotExist:
		pass
	return render(request, 'category.html', contex_dict)


def about(request):
    return render(request, 'about.html', {'boldmessage': "about Rango"})

@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'add_page.html', context_dict)
def register(request):
	registered = False
	if request.method == 'POST':
		user_form=UserForm(data=request.POST)
		profile_form=UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()

			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form=UserForm()
		profile_form=UserProfileForm()
	return render(request, 'register.html', {'user_form': user_form, 'profile_form':profile_form, 'registered':registered})





def login_user(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:

			
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse('Ваша УЗ заблокирована')
		else:
			return HttpResponse('Пользователь с такой УЗ не существует')
	else:
		return render(request, 'login.html', {})


@login_required
def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/rango/")

def about(request):
	if request.session.get('visits'):
		count = request.session.get('visits')
	else:
		count = 0
	return render(request, 'about.html', {'count':count})



def track_url(request):
	page_id = None
	url = '/rango/'
	if request.method == "GET":
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			try:
				page = Page.objects.get(id=page_id)
				page.views +=1
				page.save()
				url = page.url 
			except:
				pass
	return redirect(url)




def track_cat(request):
	cat_sl = None
	url = '/rango/'
	if request.method == 'GET':

		if 'cat_sl' in request.GET:
			cat_sl = request.GET['cat_sl']
		
			cat = Category.objects.get(slug=cat_sl)
			cat.views+=1
			cat.save()
			url='/rango/category/'+str(cat_sl) + '/'
			print(url)
			return redirect(url)
		
	return redirect(url)


def test(request):
	last_val= Test.objects.all()
	con={}
	con['last_val'] = last_val
	if request.method == "POST":
		form = TestForm(request.POST)
		if form.is_valid:
			test = form.save(commit=True)
			test.save()
			return redirect('/rango/')


	else:

		con['form']= TestForm()
		return render(request, 'test.html', con)