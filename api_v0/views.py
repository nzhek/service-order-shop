from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import serializers
from public.models import Order, Customer


class StandardPageNumberPagination(PageNumberPagination):
    page_size = 50
    max_page_size = 1000


class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 1000


class CustomerView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializers
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CsrfExtemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class OrderView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializers
    pagination_class = StandardPageNumberPagination
    authentication_classes = (CsrfExtemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            self.queryset = self.queryset.filter(created__range=[start_date, end_date])

        return self.queryset


class OrderDateRange(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializers

    filterset_fields = {
        'created': ['lte', 'gte']
    }


@api_view(['GET'])
def orders_by_week(request):
    from django.db.models import Aggregate, CharField
    class Concat2(Aggregate):
        function = 'GROUP_CONCAT'
        template = '%(function)s(%(distinct)s%(expressions)s)'

        def __init__(self, expression, distinct=False, **extra):
            super(Concat2, self).__init__(
                expression,
                distinct='DISTINCT ' if distinct else '',
                output_field=CharField(),
                **extra)

    import datetime

    # исходя из тз не стал выдумывать, и сделал определение по текущему месяцу
    if request.GET.get('n_week', None):
        d = {
            "1": "2019-12-01",
            "2": "2019-12-02",
            "3": "2019-12-09",
            "4": "2019-12-16",
            "5": "2019-12-23",
            "6": "2019-12-30"
        }
        date = datetime.datetime.strptime(d[request.GET.get('n_week')], '%Y-%m-%d').date()
    else:
        date = datetime.date.today()

    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)

    from django.db.models import Count, Sum

    o = Order.objects.filter(created__date__range=[start_week, end_week]).values('created__date').annotate(
        **{
            'total': Count('created__date'),
            'customer': Concat2('customer__title'),
            'amount': Sum('amount_price')
        }).order_by('created__date')

    res = {
        "orders": [],
        "result": {
            "amount_price": 0,
            "customers": set()
        }
    }
    for entry in o:
        res["orders"].append({
            'created': entry['created__date'],
            'total': entry['total'],
            # 'customers': entry['customer'],
            'customers': "; ".join(sorted(set(entry['customer'].split(",")))),
            'amount': entry['amount']
        })
        res["result"]["customers"] = res["result"]["customers"].union(set(entry['customer'].split(",")))

    res["result"]["amount_price"] = sum(i["amount"] for i in res["orders"])
    res["result"]["customers"] = "; ".join(sorted(res["result"]["customers"]))

    return Response(res)
