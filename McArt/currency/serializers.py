from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from McArt.settings import DATE_INPUT_FORMATS
from currency.models import Currency, SumDate


class CurrencyListModelSerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class CurrencySumListModelSerializer(ModelSerializer):
    sum_date_1 = serializers.FloatField(read_only=True)
    sum_date_2 = serializers.FloatField(read_only=True)
    sum_date = serializers.FloatField(read_only=True)
    date_1 = serializers.DateField(write_only=True, input_formats=DATE_INPUT_FORMATS)
    date_2 = serializers.DateField(write_only=True, input_formats=DATE_INPUT_FORMATS)
    main_currency = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Currency.objects.all())

    class Meta:
        model = SumDate
        fields = ("id", "main_currency", "date_1", "date_2", "sum_date_1", "sum_date_2", "sum_date",)
