from functools import update_wrapper
from django.db import models
from django.db.models import Q



class TimeStamped(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cuisines(models.Model):

    title = models.CharField(  max_length=256)

    def __str__(self) -> str:
        return self.title

class RestaurantQuerySet(models.QuerySet):         
    """
        Custom get_query_set , based on the lookups provided
    """
    def search(self,query):
        lookup = (Q(name__exact=query)|
                    Q(rating_text__exact=query)
                )

        return self.filter(lookup)



class RestaurantManager(models.Manager):
    def get_queryset(self):
        return RestaurantQuerySet(self.model , using = self._db)
     

    def search(self , query = None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class Address(models.Model):
    city = models.TextField()
    country_code = models.IntegerField()
    add = models.TextField()
    locality = models.TextField()
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)

    def __str__(self):
        return self.add
    

class Restaurant(TimeStamped):
    res_id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=256)
    address = models.ForeignKey(Address, related_name="address", null=True, blank=True , on_delete=models.SET_NULL)
    cuisines = models.ManyToManyField(Cuisines,related_name="cuisines", null=True, blank=True)
    avg_cost_for_two = models.DecimalField(max_digits=10, decimal_places=3)
    currency = models.CharField(max_length=50)
    has_table_booking = models.BooleanField()
    has_online_booking = models.BooleanField()
    agg_rating = models.IntegerField()
    rating_color =  models.CharField(max_length=200)
    rating_text = models.CharField(max_length=200)
    votes = models.IntegerField()

    objects = RestaurantManager()

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return "{0}-{1}".format(self.res_id, self.name)