from urllib.request import urlopen

import bs4
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from currency.models import Currency, SumDate
from currency.serializers import CurrencyListModelSerializer, CurrencySumListModelSerializer


class CurrencyListModelViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencyListModelSerializer

    def get_queryset(self):
        soup = bs4.BeautifulSoup(urlopen("https://www.cbr.ru/scripts/XML_valFull.asp"), 'lxml')
        list_a = soup.find_all("item")
        for item in list_a:
            check = Currency.objects.filter(translate_name=item.find("name").text).first()
            if check:
                pass
            else:
                category = {"translate_name": item.find("name").text, "name": item.engname.text,
                            "nominal": item.nominal.text, "parent_code": item.get("id"),
                            "iso_num": item.iso_num_code.text, "iso_char": item.iso_char_code.text}
                Currency.objects.create(**category)
        return Currency.objects.all()


class CurrencySumListModelViewSet(ModelViewSet):
    queryset = SumDate.objects.all()
    serializer_class = CurrencySumListModelSerializer

    def create(self, request, *args, **kwargs):
        SumDate.objects.all().delete()
        request.POST._mutable = True
        date_1, date_2 = request.data["date_1"].split("-"), request.data["date_2"].split("-")
        date_1, date_2 = f"{date_1[2]}/{date_1[1]}/{date_1[0]}", f"{date_2[2]}/{date_2[1]}/{date_2[0]}"
        soup_1 = bs4.BeautifulSoup(urlopen(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date_1}"),
                                   'lxml')
        soup_2 = bs4.BeautifulSoup(urlopen(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date_2}"),
                                   'lxml')
        name = Currency.objects.filter(id=int(request.data["main_currency"])).first()
        search_sum_1 = soup_1.find(id=f"{name.parent_code}")
        search_sum_2 = soup_2.find(id=f"{name.parent_code}")
        req = {"sum_date_1": float(".".join(search_sum_1.value.text.split(","))),
               "sum_date_2": float(".".join(search_sum_2.value.text.split(","))),
               "sum_date": float(".".join(search_sum_1.value.text.split(","))) - float(
                   ".".join(search_sum_2.value.text.split(",")))}
        SumDate.objects.create(**req)
        return Response(data=req, status=status.HTTP_201_CREATED)
