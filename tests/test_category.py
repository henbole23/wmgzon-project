from bs4 import BeautifulSoup


def test_music_page_loads(client, app, sample_product_data):
    """Function for checking whether the music page loads correctly"""

    response = client.get('/category/music')

    # Check load status is success
    assert response.status_code == 200
    # Check music page is loaded into the page and therefore music category loads
    assert b'music Page' in response.data
    # Check product data is loaded into the product page
    assert b'Music Test Product' in response.data


def test_individual_product_loads(client, app, sample_product_data):
    """Function for checking whether an individual product page loads with correct data"""

    response = client.get('/category/music')

    # Check load status is success
    assert response.status_code == 200

    # Retrieves the response html data
    soup = BeautifulSoup(response.data, 'html.parser')
    # Finds the product 1 a tag
    product_page_link = soup.find('a', {'id': 'product 1'})
    # Finds the link for the individual product page
    product_link_href = product_page_link.attrs['href']
    # Sends get request for product page
    response = client.get(product_link_href)

    # Check load status is success
    assert response.status_code == 200
    # Check artist data is loaded into the page
    assert b'Test Artist 1' in response.data
    # Check artist bio is loaded into the page
    assert b'Test Artist 1 is an artist' in response.data


def test_product_filter_redirect(client, app, sample_product_data):
    """Function for checking that filter function works"""
    response = client.post('/category/music', data={'artist': 1, 'genre': 1})

    # Check the post request has successfully redirected user
    assert response.status_code == 302


def test_product_filter_loads_data(client, app, sample_product_data):
    """Function for checking that the filter page loads the required data"""
    response = client.get('category/filters?artist=1&genre=1')

    # Check load status is success
    assert response.status_code == 200
    # Check 1 product loaded
    assert b'1 Result' in response.data
    # Check Test Product 1 is in the HTML data
    assert b'Test Product 1' in response.data
    # Check Test Product 2 is not in HTML data
    assert b'Test Product 2' not in response.data
