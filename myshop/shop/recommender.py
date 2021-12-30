import redis
from django.conf import settings
from .models import Product

# Connect to Redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

class Recommender(object):
    '''Recommender class allowing storing of product purchases and the 
    retrieval of product suggestions for a given product or products.
    '''
    
    def get_product_key(self, id):
        '''Function to build the Redis key for a product.
        
        Args:
            id: ID property of the Product object.
        
        Returns:
            Redis key for the sorted set.
        '''
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        '''Method that increments the score of a given products bought togehter.

        Args:
            products(list): A list of Product objects that have been bought together.
        
        The following tasks are performed in this method:
        1. For the given Product objects, retrieve the product ID's.
        2. Iterate over the list of product ID's. And for each ID itereate again over the list
            of product ID's, skipping the same product ID to retrieve the products bought together
            for each product.
        3. Use the get_product_key method to retrieve the product key for each product bought.
        4. For each product ID contained in the sorted set, increment the score by 1.

        Returns:
            None
        '''
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(
                        name=self.get_product_key(product_id),
                        amount=1,
                        value=with_id
                        )

    def suggest_products_for(self, products, max_results=6):
        '''Method that returns a sorted list of product objects bought together with the
        given list of products.
        
        Args:
            products (list): 
                List of Product objects to get recommendations for,
                can contain one or more products.
            max_results (int):
                An integer representing the maximum number of
                recommendations to return.

        Returns:
            Sorted list of Product objects bought together with the given list of products.
        '''
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0,
                -1,
                desc=True
            )[:max_results]
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products


    def clear_purchases(self):
        '''Method to clear recommendations.'''
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))

