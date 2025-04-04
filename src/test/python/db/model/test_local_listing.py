from pricing_service.model.db import LocalListing, LocalListingDao


def test_fetch_all_products_empty(local_listing_dao):
    """
    Test fetching products from an empty database.
    """
    products = local_listing_dao.fetch_all()
    assert products == []  # Expect an empty list


def test_insert_and_fetch_product(test_db, local_listing_dao):
    """
    Test inserting a product and then retrieving it.
    """
    # Insert a test product
    new_product = LocalListing(market_name="cl", title="product a", url="abc.com")

    local_listing_dao.insert(new_product)

    # Fetch products
    products = local_listing_dao.fetch_all()
    assert len(products) == 1
    assert products[0].market_name == "cl"


def test_multiple_product_fetch(test_db, local_listing_dao):
    """
    Test inserting multiple products and verifying retrieval.
    """
    # Insert multiple products
    local_listing_dao.insert_many([
        LocalListing(market_name="cl", title="product a", url="abc.com"),
        LocalListing(market_name="cl", title="product b", url="abcb.com"),
    ])

    # Fetch products
    products = local_listing_dao.fetch_all()
    assert len(products) == 2
    assert products[0].title == "product a"
    assert products[1].title == "product b"
