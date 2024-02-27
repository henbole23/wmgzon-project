import pytest
from app import create_app, db
from app.models import Products, Albums, Artists, AlbumGenre, Genres


@pytest.fixture()
# Configuration of the app test environment
def app():
    # Creates database in memory which saves teardown of database after each test
    app = create_app(database="sqlite://")
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
# Configuration of the mock client
def client(app):
    return app.test_client()


@pytest.fixture()
def sample_product_data(app):
    for product in range(1, 3):
        test_product = Products(name=f'Music Test Product {product}',
                                image=f'test{product}_test.jpg',
                                price=9.99,
                                type='music',
                                stock=50)

        test_product_artist = Artists(name=f'Test Artist {product}',
                                      bio=f'Test Artist {product} is an artist')

        test_product_album = Albums(name=f'Music Test Product {product}',
                                    year=2024 + product,
                                    fk_product_id=product,
                                    fk_artist_id=product)

        test_product_genre = Genres(name=f'Test Genre {product}')

        test_albumgenre = AlbumGenre(fk_album_id=product,
                                     fk_genre_id=product)

        with app.app_context():
            db.session.add(test_product)
            db.session.add(test_product_artist)
            db.session.add(test_product_album)
            db.session.add(test_product_genre)
            db.session.add(test_albumgenre)
            db.session.commit()

    yield

    with app.app_context():
        db.session.query(Products).delete()
        db.session.query(Artists).delete()
        db.session.query(Albums).delete()
        db.session.query(Genres).delete()
        db.session.query(AlbumGenre).delete()
        db.session.commit()
