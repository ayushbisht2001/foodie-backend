from django.core.management.base import BaseCommand
from numpy import add
import pandas as pd
from pandas.io.sql import has_table
from restaurant.models import *
from django.conf import settings
import os



MODE_REFRESH = 'refresh'
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing "

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    # logger.info("Delete Restaurants instances")
    Restaurant.objects.all().delete()


def create_restaurants(row):
    row = dict(row)
    # logger.info("Creating Restaurants")
    cus_lis = []
    try:
        for cui in row["cuisines"].split(','):
            c = Cuisines(title = cui)
            c.save()
            cus_lis.append(c)
    except:
        print("nan")

    add_payload = {
        "city" : row.get("city"),
        "country_code" : row.get("country_code"),
        "add" : row.get("address"),
        "locality" : row.get("locality"),
        "longitude" : row.get("longitude"),
        "latitude" : row.get("latitude"),
    }
    res_payload = {
       "res_id" : row.get("res_id"),
       "name" : row.get("name"), 
       "avg_cost_for_two" : row.get("avg_cost_for_two"), 
       "currency" : row.get("currency"), 
       "has_table_booking" : row.get("has_table_booking"), 
       "has_online_booking" : row.get("has_online_booking"), 
       "agg_rating" : row.get("agg_rating"), 
       "rating_color" : row.get("rating_color"), 
       "rating_text" : row.get("rating_text"), 
       "votes" : row.get("votes"), 

    }

    add = Address(**add_payload)
    add.save()
    res = Restaurant(**res_payload, address = add )
    res.save()
    res.cuisines.add(*cus_lis)
    res.save()

    # logger.info("{} res created.".format(res))
    return res

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    r_path = os.path.join(settings.BASE_DIR,'static/restaurant.csv')
    a_path = os.path.join(settings.BASE_DIR,'static/address.csv')

    restaurant = pd.read_csv(r_path)
    address = pd.read_csv(a_path)
    df = restaurant.merge(address, on = "Restaurant ID")
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return
    df.rename(
        columns = {'Restaurant ID': 'res_id', 'Country Code': 'country_code' , 'City' : 'city' , 'Address' : 'address', 'Locality' : 'locality',
        'Longitude' : 'longitude', 'Latitude' : 'latitude', 'Restaurant Name' : 'name', 'Cuisines' : 'cuisines', 'Average Cost for two' : 'avg_cost_for_two'
        ,'Currency' : 'currency', 'Has Table booking' : 'has_table_booking', 'Has Online delivery' : 'has_online_booking', 'Aggregate rating' : 'agg_rating',
        'Rating color' : 'rating_color', 'Rating text' : 'rating_text','Votes' : 'votes'  }, 
        inplace = True)
    df["has_table_booking"].replace({"Yes" : True, "No" : False}, inplace=True)
    df["has_online_booking"].replace({"Yes" : True, "No" : False}, inplace=True)

    print(df.head(10))

    for index, row in df.iterrows():
        create_restaurants(row)