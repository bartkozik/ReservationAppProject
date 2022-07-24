from django.shortcuts import render, redirect
from django.views import View

import datetime

# Create your views here.
from conference_app.models import Room, User, Reservation


def index(request):
    return render(request, 'base.html')


def add_user(request):
    if request.method == 'GET':
        return render(request, 'add_user.html')
    username = request.POST['username']
    password = request.POST['password']
    re_password = request.POST['password2']
    if re_password == password:
        User.objects.create(username=username, password=password)
        return render(request, 'base.html', {'message': 'Dodano Użytkownika'})
    else:
        return render(request, 'add_user.html', {'username':username, 'message':'Błąd w podanym haśle!'})


def show_room(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = datetime.date.today() in reservation_dates

        return render(request, 'room_list.html', {'rooms':rooms})



class LoginView(View):

    def get(self, request):
        return render(request, 'login_form.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
            request.session['user'] = user.id
            return render(request, 'login_form.html', {'message':'Zalogowano poprawnie!'})
        except User.DoesNotExist:
            return render(request, 'login_form.html', {'message': 'Nie ma takiego użytkownika!'} )

class LogoutView(View):

    def get(self, request):
        if 'user' in request.session:
            del request.session['user']
        return redirect('/')


class AddRoom(View):

    def get(self,request):
        return render(request, 'add_room.html')

    def post(self, request):
        name = request.POST.get("room_name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        screen = request.POST.get("screen_availability") == 'on'
        if not name:
            return render(request, 'add_room.html', context={'error':'Nie podałeś nazwy sali'})
        if capacity <= 0:
            return render(request, 'add_room.html', context={'error': 'Nie podałeś pojemności'})
        if Room.objects.filter(name=name).first():
            return render(request, 'add_room.html', context={'error': 'Sala o podanej nazwie już istnieje!'})
        Room.objects.create(name=name, capacity=capacity, screen_avail=screen)
        return render(request, 'room_list.html', {'message': 'Dodano salę!'})



class DelRoom(View):

    def get(self, request, id):
        return render(request, 'delete_room.html',
                      {'user': Room.objects.get(pk=id)})

    def post(self, request, id):
        if request.POST['potwierdzenie'] == 'tak':
            u = Room.objects.get(pk=id)
            u.delete()
        return redirect('/')

class ModifyRoom(View):

    def get(self, request, room_id):
        return render(request, 'modify_room.html', {'room': Room.objects.get(id=room_id)})

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        name = request.POST.get("room_name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        screen = request.POST.get("screen_availability") == 'on'
        if not name:
            return render(request, 'add_room.html', context={'error': 'Nie podałeś nazwy sali'})
        if capacity <= 0:
            return render(request, 'add_room.html', context={'error': 'Nie podałeś pojemności'})
        if name != room.name and Room.objects.filter(name=name).first():
            return render(request, 'add_room.html', context={'error': 'Sala o podanej nazwie już istnieje!'})

        room.name = name
        room.capacity = capacity
        room.screen_avail = screen
        room.save()
        return render(request, 'room_list.html', {'message': 'Wyedytowano!'})

class RoomReservation(View):

    def get(self, request, room_id):
        return render(request, 'room_reservation.html', {'room': Room.objects.get(id=room_id)})

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        comment = request.POST.get('comment')
        date = request.POST.get('date')

        if Reservation.objects.filter(room_id=room, date=date):
            return render(request, 'room_reservation.html', {'error':'Sala jest niedostępna w tym terminie!'})
        if date < str(datetime.date.today()):
             return render(request, 'room_reservation.html', {'error': 'Data rezerwacji jest niepoprawna!'})
        Reservation.objects.create(room_id=room, date=date, comment=comment)
        return redirect('/all_rooms_reservations/')


def show_room_reservations(request):
    if request.method == 'GET':
        rooms = Reservation.objects.all().order_by('date')
        return render(request, 'room_reservation_list.html', {'rooms':rooms})
