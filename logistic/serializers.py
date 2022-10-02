from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price'] #'stock',


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    # настройте сериализатор для склада
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']


    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            product_info = position["product"]
            quantity_info = position["quantity"]
            price_info = position["price"]
            StockProduct.objects.create(stock=stock, product=product_info, quantity=quantity_info, price=price_info) #
        return stock


    def update_or_create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().update_or_create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            # stock_info = position["stock"]
            product_info = position["product"]
            quantity_info = position["quantity"]
            price_info = position["price"]
            StockProduct.objects.update_or_create(product=product_info, quantity=quantity_info, price=price_info) #stock=stock_info,

        return stock
    #
    # def update(self, instance, validated_data):
    #     # достаем связанные данные для других таблиц
    #     positions = validated_data.pop('positions')
    #
    #     # обновляем склад по его параметрам
    #     stock = super().update(instance, validated_data)
    #
    #     # здесь вам надо обновить связанные таблицы
    #     # в нашем случае: таблицу StockProduct
    #     # с помощью списка positions
    #     for position in positions:
    #         # stock_info = position["stock"]
    #         product_info = position["product"]
    #         quantity_info = position["quantity"]
    #         price_info = position["price"]
    #         StockProduct.objects.update(product=product_info, quantity=quantity_info, price=price_info) #stock=stock_info,
    #
    #     return stock
