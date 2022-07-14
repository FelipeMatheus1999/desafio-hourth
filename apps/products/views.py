from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from apps.products.models import Products
from apps.products.serializer import ProductsSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = [ProductsSerializer]

    @staticmethod
    def get_year(date, date_to_compare=None):
        if date is not None:
            year = str(date)[:4]
            return year

        year = str(date_to_compare)[:4]
        return year

    @staticmethod
    def get_month(date, date_to_compare=None):
        if date is not None:
            month = str(date)[5:7]
            return month

        month = str(date_to_compare)[5:7]
        return month

    @staticmethod
    def get_day(date, date_to_compare=None):
        if date is not None:
            day = str(date)[8:10]
            return day

        day = str(date_to_compare)[8:10]
        return day

    def get_all_days_in_data(self, date, date_to_compare=None):
        year = self.get_year(date, date_to_compare)
        month = self.get_month(date, date_to_compare)
        day_compare = self.get_day(date, date_to_compare)
        all_days = int(year * 365) + int(month * 30) + int(day_compare)

        return all_days

    def date_is_in_range(self, date_to_compare, init_date, finish_date):
        days_compare = self.get_all_days_in_data(date_to_compare)
        days_init = self.get_all_days_in_data(init_date, date_to_compare)
        days_finish = self.get_all_days_in_data(finish_date, date_to_compare)

        init_date_greater_than_finish_date = days_init > days_finish
        date_init_is_none = init_date is None
        date_finish_is_none = finish_date is None

        if init_date_greater_than_finish_date:
            return True

        if date_init_is_none or date_finish_is_none:
            return True

        if days_compare < days_init or days_compare > days_finish:
            return False

        return True

    def products_filter(self, products, init_date, finish_date):
        filtered_products = {}

        for product in products:
            product_name = product.product_url.split("products/")[1]
            has_key = filtered_products.get(product_name)
            consult_date = product.consult_date

            if not has_key:
                filtered_products[product_name] = []

            if self.date_is_in_range(consult_date, init_date, finish_date):
                filtered_products[product_name].append(product)

        return filtered_products

    @staticmethod
    def count_sales_of_products(filtered_products):
        counted_products = {}

        for products in filtered_products.values():
            for product in products:

                product_name = product.product_url.split("products/")[1]
                has_key = counted_products.get(product_name)

                if not has_key:
                    counted_products[product_name] = {
                        "product_url_image": product.product_url_image,
                        "product_url": product.product_url,
                        "product_url_created_at": product.product_url_created_at,
                        "total_sales": 0
                    }

                sales_date = str(product.consult_date)
                counted_products[product_name]["total_sales"] += \
                    product.sales_of_the_day
                counted_products[product_name][sales_date] = product.sales_of_the_day

        return [product for product in counted_products.values()]

    def create(self, request, *args, **kwargs):
        data = request.data

        if len(data) > 1:
            serializer = ProductsSerializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)

            product_data = [Products(**product) for product in data]
            products = Products.objects.bulk_create(product_data)

            data = ProductsSerializer(products, many=True).data
            return Response(data, status=status.HTTP_201_CREATED)

        serializer = ProductsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        product = Products.objects.create(**data)

        data = ProductsSerializer(product).data
        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        init_date = request.query_params.get("init_date")
        finish_date = request.query_params.get("finish_date")
        products = Products.objects.all()
        filtered_products = self.products_filter(products, init_date, finish_date)
        counted_products = self.count_sales_of_products(filtered_products)

        return Response(counted_products, status=status.HTTP_200_OK)
