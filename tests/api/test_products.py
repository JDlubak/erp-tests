# import pytest
#
# pytestmark = pytest.mark.api
#
#
# @pytest.mark.smoke
# def test_get_product_by_id_positive(api):
#     products = api.get_products()
#     assert products.status_code == 200
#     product_id = products.json()["data"][0]["id"]
#
#     response = api.get_product(product_id)
#
#     assert response.status_code == 200
#     assert response.json()["id"] == product_id
#
#
# def test_get_product_by_non_existing_id_negative(api):
#     response = api.get_product("00000000000000000000000000")
#
#     assert response.status_code == 404
