from django.shortcuts import render

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please login to access the chat system")
        return redirect('chat_app:login')
    else:
        return render(request, 'chat/index.html')

def room(request, room_name):
    if not request.user.is_authenticated:
        messages.info(request, "Please login to access the chat system")
        return redirect('chat_app:login')
    else:
        context = {}
        context['room_name'] = room_name
        return render(request, 'chat/room.html', context=context)



# requirements form user creation and releating form
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
# redirect after registration/login for egsample
from django.shortcuts import redirect

from django.contrib import messages

# import custom registration form
from chat.forms import NewUserForm

def register(request):

    # return if from submit from page
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            # save form data as user in db
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            # login user after registration and redirect to home
            login(request, user)
            messages.info(request, f"You are now logged in as : {username}")
            return redirect('chat_app:index')
        else:
            # display errors if form not valid
            # for msg in form.error_messages:
            #     messages.error(request, f"{msg}: {form.error_messages[msg]}")
            #     print(form.error_messages[msg])
            print(len(form.errors.as_data()))
            for msg in form.errors:
                messages.error(request, f"{form.errors[msg]}")
                print(f"{msg}: {form.errors[msg]}")


    # normal return for request to page
    form = NewUserForm
    context = {'form':form}
    return render(request, './chat/register.html', context = context)

def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('chat_app:index')

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Successfulle logged in, Welcom {username}")
                return redirect('chat_app:index')
            else:
                for msg in form.errors:
                    messages.error(request, f"{form.errors[msg]}")
        else:
            for msg in form.errors:
                messages.error(request, f"{form.errors[msg]}")

    form = AuthenticationForm
    context = {'form':form}
    return render(request, './chat/login.html', context = context)

# password reset
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})
