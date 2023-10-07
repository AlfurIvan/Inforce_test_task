import datetime

from rest_framework import views, response, permissions

from user import models as user_models
from user.authentication import CustomUserAuthentication
from . import models as menu_models
from . import serializer as menu_serializer


class MenuUploadApi(views.APIView):
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        user = request.user
        try:
            menus_obj = menu_models.Menu.objects.filter(restaurant=user.restaurant).all()
            serializer = menu_serializer.MenuSerializer(menus_obj, many=True)
            return response.Response(serializer.data)
        except menu_models.Menu.DoesNotExist:
            return response.Response({"error": "No menu history yet"})

    def post(self, request):
        user = request.user

        try:
            description = request.data["description"]
        except KeyError:
            return response.Response(data={'error': 'Incorrect input'})
        else:
            user_obj = (user_models.User.objects
                        .prefetch_related("restaurant")
                        .get(id=user.id))
            new_menu = menu_models.Menu(
                date=datetime.date.today(),
                description=description,
                restaurant=user_obj.restaurant
            )
            new_menu.save()

            return response.Response(menu_serializer.MenuSerializer(new_menu).data)


class OrdersAmountApi(views.APIView):
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        user = request.user
        try:
            orders = (menu_models.Order.objects
                      .filter(selected_menu__restaurant=user.restaurant, date=datetime.date.today())
                      .all())
            serializer = menu_serializer.OrderSerializer(orders, many=True)
            return response.Response(
                {
                    "total_amount_of_orders_today": len(orders),
                    "orders": serializer.data
                }
            )
        except menu_models.Order.DoesNotExist:
            return response.Response({"error": "Your restaurant do not have orders today"})


class MenuFetchOrderApi(views.APIView):
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            menus_obj = (menu_models.Menu.objects
                         .filter(date=datetime.date.today())
                         .all())
            serializer = menu_serializer.MenuSerializer(menus_obj, many=True)
            return response.Response(serializer.data)
        except menu_models.Menu.DoesNotExist:
            return response.Response({"error": "No menus here yet"})

    def post(self, request):

        try:
            order = (menu_models.Order.objects
                     .filter(date=datetime.date.today(), user=request.user)
                     .get())
            return response.Response(menu_serializer.OrderSerializer(order).data)
        except menu_models.Order.DoesNotExist:
            pass

        try:
            sel_id = request.data['sel_id']
        except KeyError:
            return response.Response(data={'error': 'Incorrect input'})
        try:
            sel_menu = (menu_models.Menu.objects
                        .filter(id=sel_id)
                        .get())
        except menu_models.Menu.DoesNotExist:
            return response.Response(data={'error': 'No such menu with current id'})
        order = menu_models.Order(
            date=datetime.datetime.now(),
            user=request.user,
            selected_menu=sel_menu
        )
        order.save()
        return response.Response(menu_serializer.OrderSerializer(order).data)
