from django.http import HttpResponse
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filters import (
    CarFilter, RoleFilter, DriverLicenseFilter, UserFilter,
    ParkingAddressFilter, StatusFilter, NotificationFilter,
    BookingFilter, ServiceFilter
)
from .forms import (
    ParkingAddressForm, StatusForm, CarForm, ServiceForm,
    CustomAuthenticationForm
)
from .models import (
    Role, DriverLicense, User, Notification, ParkingAddress,
    Status, Car, Booking, Service, InspectionCar, CustomUser
)
from .serializers import (
    CarSerializer, ParkingAddressSerializer,
    StatusSerializer, CustomUserSerializer
)


def car_list_view(request):
    cars = Car.objects.all()
    context = {
        'cars': cars,
    }
    return render(request, 'car_list.html', context)


def filtered_car_list_view(request):
    cars = Car.objects.all()
    car_filter = CarFilter(request.GET, queryset=cars)
    context = {
        'filtered_cars': car_filter.qs,
    }
    return render(request, 'filtered_cars_list.html', context)


class RoleListView(FilterView):
    model = Role
    filterset_class = RoleFilter
    template_name = 'generic_list.html'
    context_object_name = 'roles'
    paginate_by = 10


class DriverLicenseListView(FilterView):
    model = DriverLicense
    filterset_class = DriverLicenseFilter
    template_name = 'driver_license_list.html'
    context_object_name = 'licenses'
    paginate_by = 10


class UserListView(FilterView):
    model = User
    filterset_class = UserFilter
    template_name = 'user_list.html'
    context_object_name = 'users'
    paginate_by = 10


class ParkingAddressListView(FilterView):
    model = ParkingAddress
    filterset_class = ParkingAddressFilter
    template_name = 'parking_address_list.html'
    context_object_name = 'parking_addresses'
    paginate_by = 10


class StatusListView(FilterView):
    model = Status
    filterset_class = StatusFilter
    template_name = 'status_list.html'
    context_object_name = 'statuses'
    paginate_by = 10


class NotificationListView(FilterView):
    model = Notification
    filterset_class = NotificationFilter
    template_name = 'notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 10


class BookingListView(FilterView):
    model = Booking
    filterset_class = BookingFilter
    template_name = 'booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10


class ServiceListView(FilterView):
    model = Service
    filterset_class = ServiceFilter
    template_name = 'service_list.html'
    context_object_name = 'services'
    paginate_by = 10


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(
                {"message": "Login successful"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
        )


class BaseListView(ListView):
    template_name = 'generic_list.html'


class BaseCreateView(CreateView):
    template_name = 'generic_form.html'
    success_url = reverse_lazy('role_list')


class BaseUpdateView(UpdateView):
    template_name = 'generic_form.html'
    success_url = reverse_lazy('role_list')


class BaseDeleteView(DeleteView):
    template_name = 'generic_confirm_delete.html'
    success_url = reverse_lazy('role_list')


# Role views
# views.py


class RoleListView(ListView):
    model = Role
    template_name = 'generic_list.html'  # Укажите нужный шаблон
    context_object_name = 'object_list'


class RoleCreateView(BaseCreateView):
    model = Role
    fields = ['name_role']


class RoleUpdateView(BaseUpdateView):
    model = Role
    fields = ['name_role']


class RoleDeleteView(BaseDeleteView):
    model = Role


# DriverLicense views
class DriverLicenseListView(BaseListView):
    model = DriverLicense


class DriverLicenseCreateView(BaseCreateView):
    model = DriverLicense
    fields = ['user_name', 'surname', 'date_of_birth', 'validity_period', 'series_and_number', 'categories']


class DriverLicenseUpdateView(BaseUpdateView):
    model = DriverLicense
    fields = ['user_name', 'surname', 'date_of_birth', 'validity_period', 'series_and_number', 'categories']


class DriverLicenseDeleteView(BaseDeleteView):
    model = DriverLicense


# User views
class UserListView(BaseListView):
    model = User


class UserCreateView(BaseCreateView):
    model = User
    fields = ['driverlicense', 'role', 'user_name', 'surname']


class UserUpdateView(BaseUpdateView):
    model = User
    fields = ['driverlicense', 'role', 'user_name', 'surname']


class UserDeleteView(BaseDeleteView):
    model = User


# Notification views
class NotificationListView(BaseListView):
    model = Notification


class NotificationCreateView(BaseCreateView):
    model = Notification
    fields = ['user', 'messages']


class NotificationUpdateView(BaseUpdateView):
    model = Notification
    fields = ['user', 'messages']


class NotificationDeleteView(BaseDeleteView):
    model = Notification


# ParkingAddress views
class ParkingAddressListView(BaseListView):
    model = ParkingAddress


class ParkingAddressCreateView(BaseCreateView):
    model = ParkingAddress
    fields = ['name_street', 'numbers_home']


class ParkingAddressUpdateView(BaseUpdateView):
    model = ParkingAddress
    fields = ['name_street', 'numbers_home']


class ParkingAddressDeleteView(BaseDeleteView):
    model = ParkingAddress


# Status views
class StatusListView(BaseListView):
    model = Status


class StatusCreateView(BaseCreateView):
    model = Status
    fields = ['name_status']


class StatusUpdateView(BaseUpdateView):
    model = Status
    fields = ['name_status']


class StatusDeleteView(BaseDeleteView):
    model = Status


# Car views
class CarListView(BaseListView):
    model = Car


class CarCreateView(BaseCreateView):
    model = Car
    fields = ['parking', 'status', 'brand', 'model', 'number_car']


class CarUpdateView(BaseUpdateView):
    model = Car
    fields = ['parking', 'status', 'brand', 'model', 'number_car']


class CarDeleteView(BaseDeleteView):
    model = Car


# Booking views
class BookingListView(BaseListView):
    model = Booking


class BookingCreateView(BaseCreateView):
    model = Booking
    fields = ['user', 'car', 'start_date', 'end_date']


class BookingUpdateView(BaseUpdateView):
    model = Booking
    fields = ['user', 'car', 'start_date', 'end_date']


class BookingDeleteView(BaseDeleteView):
    model = Booking


# Service views
class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'object_list'


# Вьюха для создания нового сервиса
class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_form.html'
    success_url = reverse_lazy('service_list')  # Перенаправление после успешного добавления


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_form.html'
    success_url = reverse_lazy('service_list')


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service_confirm_delete.html'
    success_url = reverse_lazy('service_list')


# InspectionCar views
class InspectionCarListView(BaseListView):
    model = InspectionCar


class InspectionCarCreateView(BaseCreateView):
    model = InspectionCar
    fields = ['user', 'car']


class InspectionCarUpdateView(BaseUpdateView):
    model = InspectionCar
    fields = ['user', 'car']


class InspectionCarDeleteView(BaseDeleteView):
    model = InspectionCar


# DriverLicense
class DriverLicenseListView(ListView):
    model = DriverLicense
    template_name = 'driver_license_list.html'
    context_object_name = 'driver_licenses'


class DriverLicenseCreateView(CreateView):
    model = DriverLicense
    template_name = 'driver_license_form.html'
    fields = ['user_name', 'surname', 'date_of_birth', 'validity_period', 'series_and_number',
              'categories']  # замените на поля вашей модели

    def get_success_url(self):
        # Перенаправление на список всех водительских прав после успешного создания
        return reverse_lazy('driverlicense_list')


class DriverLicenseUpdateView(UpdateView):
    model = DriverLicense
    template_name = 'driver_license_form.html'
    fields = ['user_name', 'surname', 'validity_period', 'series_and_number',
              'categories']  # замените на поля вашей модели

    def get_success_url(self):
        # Перенаправление на список всех водительских прав после успешного создания
        return reverse_lazy('driverlicense_list')


class DriverLicenseDeleteView(DeleteView):
    model = DriverLicense
    template_name = 'driver_license_confirm_delete.html'
    success_url = reverse_lazy('driverlicense_list')


# Users
# views.py
class UserListView(ListView):
    model = User
    template_name = 'user_list.html'  # Шаблон для отображения списка пользователей
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    template_name = 'user_form.html'  # Шаблон для создания пользователя
    fields = ['driver_license', 'role', 'user_name', 'surname']  # Замените на ваши поля

    def get_success_url(self):
        return reverse_lazy('user_list')  # Перенаправление на список пользователей после создания


class UserUpdateView(UpdateView):
    model = User
    template_name = 'user_form.html'  # Шаблон для редактирования пользователя
    fields = ['driver_license', 'role', 'user_name', 'surname']  # Замените на ваши поля

    def get_success_url(self):
        return reverse_lazy('user_list')  # Перенаправление на список пользователей после обновления


class UserDeleteView(DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'  # Шаблон для подтверждения удаления
    context_object_name = 'user'

    def get_success_url(self):
        return reverse_lazy('user_list')  # Перенаправление на список пользователей после удаления


# Notifications

class NotificationListView(ListView):
    model = Notification
    template_name = 'notification_list.html'  # Шаблон для отображения списка уведомлений
    context_object_name = 'notifications'


class NotificationCreateView(CreateView):
    model = Notification
    template_name = 'notification_form.html'  # Шаблон для создания уведомления
    fields = ['user', 'messages']  # Замените на ваши поля

    def get_success_url(self):
        return reverse_lazy('notification_list')  # Перенаправление на список уведомлений после создания


class NotificationUpdateView(UpdateView):
    model = Notification
    template_name = 'notification_form.html'  # Шаблон для редактирования уведомления
    fields = ['user', 'messages']  # Замените на ваши поля

    def get_success_url(self):
        return reverse_lazy('notification_list')  # Перенаправление на список уведомлений после обновления


class NotificationDeleteView(DeleteView):
    model = Notification
    template_name = 'notification_confirm_delete.html'  # Шаблон для подтверждения удаления
    context_object_name = 'notification'

    def get_success_url(self):
        return reverse_lazy('notification_list')  # Перенаправление на список уведомлений после удаления


# ParkingAddress

class ParkingAddressListView(ListView):
    model = ParkingAddress
    template_name = 'parking_address_list.html'  # Шаблон для отображения списка парковочных адресов
    context_object_name = 'parking_addresses'


class ParkingAddressCreateView(CreateView):
    model = ParkingAddress
    form_class = ParkingAddressForm
    template_name = 'parking_address_form.html'

    def get_success_url(self):
        return reverse_lazy('parkingaddress_list')  # Замените на ваши поля

    def get_success_url(self):
        return reverse_lazy('parking_address_list')  # Перенаправление на список парковочных адресов после создания


class ParkingAddressUpdateView(UpdateView):
    model = ParkingAddress
    template_name = 'parking_address_form.html'  # Шаблон для редактирования парковочного адреса
    fields = ['name_street', 'numbers_home']  # Замените на ваши поля

    def get_success_url(self):
        return reverse_lazy('parking_address_list')  # Перенаправление на список парковочных адресов после обновления


class ParkingAddressDeleteView(DeleteView):
    model = ParkingAddress
    template_name = 'parking_address_confirm_delete.html'  # Шаблон для подтверждения удаления
    context_object_name = 'parking_address'

    def get_success_url(self):
        return reverse_lazy('parking_address_list')


# Status
class StatusListView(ListView):
    model = Status
    form_class = StatusForm
    template_name = 'status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status_form.html'

    def get_success_url(self):
        return reverse_lazy('status_list')  # Перенаправление на список после создания статуса


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status_form.html'

    def get_success_url(self):
        return reverse_lazy('status_list')  # Перенаправление на список статусов после обновления


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'status_confirm_delete.html'  # Шаблон для подтверждения удаления
    context_object_name = 'status'

    def get_success_url(self):
        return reverse_lazy('status_list')


# Cars
class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'  # Шаблон для отображения списка автомобилей
    context_object_name = 'cars'


class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'

    def form_valid(self, form):
        # Данные успешно сохранены, перенаправляем на список машин
        form.save()
        return redirect('car_list')


class CarUpdateView(UpdateView):
    model = Car
    template_name = 'car_form.html'  # Шаблон для редактирования автомобиля
    fields = ['parking', 'status', 'brand', 'model', 'number_car']  # Замените на ваши поля

    def get_success_url(self):
        return reverse_lazy('car_list')  # Перенаправление на список автомобилей после обновления


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'  # Шаблон для подтверждения удаления
    context_object_name = 'car'

    def get_success_url(self):
        return reverse_lazy('car_list')


# Booking
class BookingListView(ListView):
    model = Booking
    template_name = 'booking_list.html'  # Шаблон для отображения всех бронирований
    context_object_name = 'bookings'


class BookingCompleteView(DetailView):
    model = Booking
    template_name = 'booking_complete.html'  # Шаблон для завершения бронирования
    context_object_name = 'booking'

    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        # Завершаем аренду, например, обновляем статус аренды
        booking.status = 'Completed'  # Убедитесь, что у вас есть такой статус
        booking.save()
        return redirect('booking_list')


def parking_address_list(request):
    parking_addresses = ParkingAddress.objects.all()
    return render(request, 'parking_address_list.html', {'parking_addresses': parking_addresses})


def export_full_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="car_park_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Отчёт о состоянии автопарка'])
    writer.writerow([])

    # ParkingAddress
    writer.writerow(['Парковочные адреса'])
    writer.writerow(['ID', 'Улица', 'Дом'])
    for item in ParkingAddress.objects.all():
        writer.writerow([item.id, item.name_street, item.numbers_home])

    writer.writerow([])

    # Cars
    writer.writerow(['Автомобили'])
    writer.writerow(['ID', 'Парковка', 'Статус', 'Бренд', 'Модель', 'Номер'])
    for item in Car.objects.select_related('parking', 'status'):
        writer.writerow([
            item.id,
            item.parking.name_street if item.parking else '—',
            item.status.name_status if item.status else '—',
            item.brand,
            item.model,
            item.number_car
        ])

    writer.writerow([])

    # Users
    writer.writerow(['Пользователи'])
    writer.writerow(['ID', 'Имя', 'Фамилия', 'Роль', 'Водительское удостоверение'])
    for user in User.objects.select_related('role', 'driver_license'):
        writer.writerow([
            user.id,
            user.user_name,
            user.surname,
            user.role.name_role if user.role else '—',
            user.driver_license.series_and_number if user.driver_license else '—'
        ])

    writer.writerow([])

    # Services
    writer.writerow(['Услуги'])
    writer.writerow(['ID', 'Тип аренды', 'Сумма'])
    for service in Service.objects.all():
        writer.writerow([service.id, service.type_of_rental, service.amount])

    writer.writerow([])

    # Booking
    writer.writerow(['Бронирования'])
    writer.writerow(['ID', 'Пользователь', 'Автомобиль', 'Дата начала', 'Дата окончания'])
    for booking in Booking.objects.select_related('user', 'car'):
        writer.writerow([
            booking.id,
            booking.user.user_name if booking.user else '—',
            booking.car.number_car if booking.car else '—',
            booking.start_date,
            booking.end_date
        ])

    return response


# API для получения списка автомобилей


# ViewSet для автомобиля
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


# ViewSet для парковки
class ParkingAddressViewSet(viewsets.ModelViewSet):
    queryset = ParkingAddress.objects.all()
    serializer_class = ParkingAddressSerializer


# ViewSet для статуса
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
