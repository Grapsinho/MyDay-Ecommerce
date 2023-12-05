import json
from channels.generic.websocket import AsyncWebsocketConsumer
from inventory.models import *
from asgiref.sync import sync_to_async
from django.db.models import Q

class LiveSearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.current_search_query = ""

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        search_query = text_data.strip()

        search_results = await self.perform_product_search(search_query)  # Use await here

        # print("search results: ", search_results)

        # if search_query != self.current_search_query:
        #     self.current_search_query = search_query
        #     search_results = await self.perform_product_search(search_query)

        unique_dict_set = set()
        unique_list = []

        for d in search_results:
            # Create a frozenset of key-value pairs to use as a key for uniqueness check
            key = (d['product__name'], d['product__slug'], d["retail_price"])

            if key not in unique_dict_set:
                unique_dict_set.add(key)
                unique_list.append(d)

        search_result = [dict(x) for x in unique_list]


        if search_result:
            result_data = [{'name': product1["product__name"], "img": product1['media__img_url'] , 'slug': product1["product__slug"], "price": str(product1["retail_price"])} for product1 in search_result]
        else:
            result_data = [{'message': "No Products"}]


        await self.send(text_data=json.dumps({
            'search_results': result_data
        }))

        

    @sync_to_async
    def perform_product_search(self, search_query):
        # Use the sync_to_async decorator for the synchronous database query
        return list(ProductInventory.objects.filter(product__name__icontains=search_query, is_active=True).values("product__name", "product__slug", "retail_price", "media__img_url")[:4])


        
        
