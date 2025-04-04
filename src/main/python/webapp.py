"""Main file for repomanager-web where route handlers are defined."""
import os
import json
from enum import Enum
from pricing_service.service import LocalListingService, OpenAIService, EbayService, FacebookService, CraigslistService, \
    SystemService, MarketMetadataService
from pricing_service.model.db import LocalListing
from pydantic import Field, BaseModel
from typing import Optional
from quart import Quart, request
from quart_schema import tag, QuartSchema, Info, hide, document_response, document_request, document_querystring, \
    security_scheme, validate_querystring


app = Quart(__name__, static_folder=None)
app.config["PROVIDE_AUTOMATIC_OPTIONS"] = True
# noinspection PyTypeChecker
QuartSchema(
    app=app,
    info=Info(version=os.getenv('DD_VERSION', 'N/A'), title='Pricing Service'),
    tags=[
        {'name': 'system', 'description': 'Endpoints for monitoring and administrative use'},
        {'name': 'pricing', 'description': 'Endpoints related to pricing'},
        {'name': 'local-markets', 'description': 'endpoints related to local markets'},
        {'name': 'local-listings', 'description': 'display local listings'},
        {'name': 'inventory', 'description': 'endpoints related to inventory'},
        {'name': 'acquisitions', 'description': 'endpoints related to acquisitions'},
    ],
    security_schemes={
        'api-token': {'type': 'apiKey', 'name': 'X-AUTH-TOKEN', 'in_': 'header'}
    },
)


class FBCategory(Enum):
    VEHICLES = 'vehicles'
    PROPERTY_RENTALS = 'propertyrentals'
    APPAREL = 'apparel'
    ELECTRONICS = 'electronics'
    ENTERTAINMENT = 'entertainment'
    FAMILY = 'family'
    FREE_STUFF = 'freestuff'
    GARDEN = 'garden'
    HOBBIES = 'hobbies'
    HOME_GOODS = 'homegoods'
    HOME_IMPROVEMENT = 'homeimprovement'
    HOME_SALES = 'homesales'
    MUSICAL_INSTRUMENTS = 'musicalinstruments'
    OFFICE_SUPPLIES = 'officesupplies'
    PET_SUPPLIES = 'petsupplies'
    SPORTING_GOODS = 'sportinggoods'
    TICKETS = 'tickets'
    TOYS = 'toys'
    VIDEO_GAMES = 'videogames'


class CraigslistCategory(Enum):
    ANTIQUES = "ata"             # Antiques
    APPLIANCES = "ppa"           # Appliances
    ARTS_CRAFTS = "ara"          # Arts & Crafts
    ATV_UTV_SNOWMOBILES = "sna"  # ATVs, UTVs, Snowmobiles
    AUTO_PARTS = "pta"           # Auto Parts
    AVIATION = "ava"             # Aviation
    BABY_KID = "baa"             # Baby & Kid Stuff
    BARTER = "bar"               # Barter
    BICYCLES = "bia"             # Bicycles
    BOATS = "bpa"                # Boats
    BOOKS = "bka"                # Books & Magazines
    BUSINESS = "bfa"             # Business
    CARS_TRUCKS = "cta"          # Cars & Trucks
    CDS_DVDS_VHS = "ema"         # CDs / DVDs / VHS
    CELL_PHONES = "moa"          # Cell Phones
    CLOTHES_ACCESSORIES = "cla"  # Clothing & Accessories
    COLLECTIBLES = "cba"         # Collectibles
    COMPUTER_PARTS = "syp"       # Computer Parts
    COMPUTERS = "sya"            # Computers
    ELECTRONICS = "ela"          # Electronics
    FARM_GARDEN = "gra"          # Farm & Garden
    FREE = "zip"                 # Free Stuff
    FURNITURE = "fua"            # Furniture
    GARAGE_SALES = "gms"         # Garage & Moving Sales
    GENERAL = "foa"              # General
    HEALTH_BEAUTY = "hba"        # Health & Beauty
    HEAVY_EQUIPMENT = "hva"      # Heavy Equipment
    HOUSEHOLD = "hsa"            # Household Items
    JEWELRY = "jwa"              # Jewelry
    MATERIALS = "maa"            # Materials
    MOTORCYCLES = "mca"          # Motorcycles & Scooters
    MOTORCYCLE_PARTS = "mpa"     # Motorcycle Parts
    MUSICAL_INSTRUMENTS = "msa"  # Musical Instruments
    PHOTO_VIDEO = "pha"          # Photo & Video
    RECREATIONAL_VEHICLES = "rva" # Recreational Vehicles
    SPORTING_GOODS = "sga"       # Sporting Goods
    TICKETS = "tia"              # Tickets
    TOOLS = "tla"                # Tools
    TOYS_GAMES = "taa"           # Toys & Games
    TRAILERS = "tra"             # Trailers
    VIDEO_GAMING = "vga"         # Video Gaming
    WANTED = "waa"               # Wanted


class FbSearch(BaseModel):
    query: str = Field(description="query", default="Fender")
    days: int = Field(description="days back", default=5)
    city: str = Field(description="city", default="la")


class FBListing(BaseModel):
    url: str = Field(description="url")


class FbBrowse(BaseModel):
    category: FBCategory = Field(description="category", default="instruments")
    city: str = Field(description="city", default="la")


class CraigslistBrowse(BaseModel):
    category: CraigslistCategory = Field(description="category", default="instruments")
    primary_location: str = Field(description="primary location", default="honolulu")
    secondary_location: str = Field(description="secondary location", default="mau")


class CraigslistDetail(BaseModel):
    url: str = Field(description="url of listing",
                     default="https://honolulu.craigslist.org/mau/msg/d/pukalani-shure-psm-200-in-ear-monitor/7830136686.html")


class GoogSearch(BaseModel):
    query: str = Field(description="query", default="Fender")
    site: str = Field(description="site", default="ebay.com")


class OpenAISearch(BaseModel):
    product_info: str = Field(description="product_info", default="Vitamix")


class KnownProducts(BaseModel):
    brand: str = Field(description="brand of item")
    model: Optional[str] = Field(description="brand of item")


# SYSTEM ENDPOINTS
@app.route('/health')
@tag(['system'])
async def health():
    """Get current pricing-service API info/status"""
    return "OK"


@app.route('/market-metadata')
@tag(['local-markets'])
async def market_metadata():
    return MarketMetadataService().get("")

@app.route('/fbm_search')
@tag(['local-markets'])
@document_querystring(FbSearch)
@validate_querystring(FbSearch)
async def fb_market_search(query_args: FbSearch):
    return FacebookService().search_fb(query_args.days, query_args.query, query_args.city)


@app.route('/fb_browse')
@tag(['local-markets'])
@document_querystring(FbBrowse)
@validate_querystring(FbBrowse)
async def browse_fbm(query_args: FbBrowse):
    return FacebookService().browse_fb(query_args.category.value, query_args.city)


@app.route('/craigslist_browse')
@tag(['local-markets'])
@document_querystring(CraigslistBrowse)
@validate_querystring(CraigslistBrowse)
async def browse_cl(query_args: CraigslistBrowse):
    return CraigslistService().browse_craigslist(query_args.category.value, query_args.primary_location, query_args.secondary_location)


@app.route('/craigslist_detail')
@tag(['local-markets'])
@document_querystring(CraigslistDetail)
@validate_querystring(CraigslistDetail)
async def cl_detail(query_args: CraigslistDetail):
    return CraigslistService().craigslist_detail(query_args.url)


@app.route('/fbm_listing')
@tag(['local-markets'])
@document_querystring(FbSearch)
@validate_querystring(FbSearch)
async def fbm_listing(query_args: FbSearch):
    return FacebookService().search_fb(query_args.days, query_args.query, query_args.city)


@app.route('/fbm_listing_detail')
@tag(['local-markets'])
@document_querystring(FBListing)
@validate_querystring(FBListing)
async def fbm_extract_info(query_args: FBListing):
    return FacebookService().fbm_listing_detail(query_args.url)


@app.route('/openai_price_search')
@tag(['pricing'])
@document_querystring(OpenAISearch)
@validate_querystring(OpenAISearch)
async def openai_search(query_args: OpenAISearch):
    return OpenAIService().search_price(query_args.product_info)


@app.route('/openai_image_search')
@tag(['pricing'])
@document_querystring(OpenAISearch)
@validate_querystring(OpenAISearch)
async def openai_img_search(query_args: OpenAISearch):
    return OpenAIService().image_description(query_args.product_info)


@app.route('/known_products')
@tag(['pricing'])
async def known_products():
    with open('src/main/resources/updated-with-shipping.json', 'r') as file:
        data = json.load(file)
    return data

@app.route('/inventory')
@tag(['inventory'])
async def inventory():
    with open('src/test/resources/inventory.json', 'r') as file:
        data = json.load(file)
    return data


@app.route('/local-listings')
@tag(['local-listings'])
async def local_listings():
    service = LocalListingService()
    return service.get()


@app.route('/local-listings/ingest')
@tag(['local-listings'])
async def ingest_local_listings():
    service = LocalListingService()
    with open('src/test/resources/cl-listings.json', 'r') as file:
        data = json.load(file)

    records = [
        LocalListing(
             market_name="cl",
             url=x['Link'],
             title=x['Title'],
             review_score=-1,
             thumbnail=x['thumbnail'])
          for x in data
    ]
    service.insert_many(records)
    return service.get()


@app.route('/ebay-test')
@tag(['pricing'])
async def ebay_test():
    ebay = EbayService()
    return await ebay.wrapper()


@app.route('/geo-ip')
@tag(['system'])
async def geoip():
    SystemService().get_geo_location()
    return []


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
