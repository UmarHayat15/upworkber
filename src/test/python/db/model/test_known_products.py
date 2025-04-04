from pricing_service.model.db import KnownProduct, KnownProductDao


def test_fetch_all_products_empty(known_products_dao):
    """
    Test fetching products from an empty database.
    """
    products = known_products_dao.fetch_all()
    assert products == []  # Expect an empty list


def test_insert_and_fetch_product(test_db, known_products_dao):
    """
    Test inserting a product and then retrieving it.
    """

    # Insert a test product
    new_product = KnownProduct(name="Test Laptop", brand="TestBrand")
    known_products_dao.insert(new_product)

    # Fetch products
    products = known_products_dao.fetch_all()
    assert len(products) == 1
    assert products[0].name == "Test Laptop"
    assert products[0].brand == "TestBrand"


def test_multiple_product_fetch(test_db, known_products_dao):
    """
    Test inserting multiple products and verifying retrieval.
    """

    # Insert multiple products
    known_products_dao.insert_many([
        KnownProduct(name="Laptop", brand="Dell"),
        KnownProduct(name="Phone", brand="Apple"),
        KnownProduct(name="Monitor", brand="Samsung")
    ])

    # Fetch products
    products = known_products_dao.fetch_all()
    assert len(products) == 3
    assert products[0].name == "Laptop"
    assert products[1].name == "Phone"
    assert products[2].name == "Monitor"
