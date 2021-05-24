import csv
import os
import sys
import django


os.chdir(".")

print("Current dir=", end=""), print(os.getcwd())
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print("BASE_DIR=", end=""), print(BASE_DIR)
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "b2tech.settings")	# 1. 여기서 프로젝트명.settings입력
django.setup()

from projects.models import *

LOCATION_CSV_PATH = 'homes.csv'

def location_uploader():
    with open(LOCATION_CSV_PATH, newline='', encoding='utf8') as csvfile:	# 4. newline =''
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            location = Location.objects.create(		# 5. class명.objects.create
                name = row['name'],
                address = row['address'],
                latitude = row['latitude'],
                longitude = row['longitude'],
                range = row['range'],
                plan = row['plan'],
                type = row['type']
            )
            location.site.add(Site.objects.get(pk=row['site_id']))
            location.resource.add(Resource.objects.get(pk=row['resource_id']))

# def main_category_uploader():
#     with open(MAIN_CATEGORY_CSV_PATH, newline='', encoding='utf8') as csvfile:
#         data_reader = csv.DictReader(csvfile)
#         for row in data_reader:
#             MainCategory.objects.create(
#                 name = row['name'],
#                 menu_id = row['menu_id']
#                 )
#
# def sub_category_uploader():
#     with open(SUB_CATEGORY_CSV_PATH, newline='', encoding='utf8') as csvfile:
#         data_reader = csv.DictReader(csvfile)
#         for row in data_reader:
#             SubCategory.objects.create(
#                 name = row['name'],
#                 main_category_id = row['main_category_id']
#                 )
#
# def product_uploader():
#     with open(PRODUCT_CSV_PATH, newline='', encoding='utf8') as csvfile:
#         data_reader = csv.DictReader(csvfile)
#         for row in data_reader:
#             Product.objects.create(
#                 name = row['name'],
#                 main_category_id = row['main_category_id'],
#                 sub_category_id = row['sub_category_id'],
#                 price = row['price'],
#                 hashtag = row['hashtag'],
#                 )
#
# def product_image_uploader():
#     with open(PRODUCT_IMAGE_CSV_PATH, newline='', encoding='utf8') as csvfile:
#         data_reader = csv.DictReader(csvfile)
#         for row in data_reader:
#             ProductImage.objects.create(
#                 product_id = row['product_id'],
#                 image_url = row['image_url'],
#                 thumbnail_status = row['thumbnail_status']
#                 )
#
# def product_option_uploader():
#     with open(PRODUCT_OPTION_CSV_PATH, newline='', encoding='utf8') as csvfile:
#         data_reader = csv.DictReader(csvfile)
#         for row in data_reader:
#             ProductOption.objects.create(
#                 product_id = row['product_id'],
#                 weight = row['weight'],
#                 extra_cost = row['extra_cost']
#                 )
#
# def order_status_uploader():
#     with open(ORDER_STATUS_CSV_PATH, newline='', encoding='utf8') as csvfile:
#         data_reader = csv.DictReader(csvfile)
#         for row in data_reader:
#             OrderStatus.objects.create(
#                 status = row['status']
#                 )

# menu_uploader()
# main_category_uploader()
# sub_category_uploader()
# product_uploader()
# product_image_uploader()
# product_option_uploader()
# order_status_uploader()

location_uploader()