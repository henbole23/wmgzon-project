from flask import redirect, url_for, jsonify
from flask_restful import Resource, reqparse

from app.models import Products
from app.extensions import db


class ProductsResource(Resource):
    """API class for retriveing all products"""

    def get(self):
        products = db.session.query(Products).all()
        if products:
            products_list = []
            for product in products:
                product_dict = {
                    "product_id": int(product.product_id),
                    "name": product.name,
                    "image": product.image,
                    "price": product.price,
                    "type": product.type,
                    "stock":  product.stock,
                    "date_added": product.date_added.isoformat(),
                    "music_info": {} if product.music_info is None else {
                        "album_id": product.music_info.album_id,
                        "name": product.music_info.name,
                        "year": product.music_info.year,
                        "artist": {} if product.music_info.artists is None else {
                            "artist_id": product.music_info.artists.artist_id,
                            "name": product.music_info.artists.name,
                            "bio": product.music_info.artists.bio
                        }
                    }
                }
                products_list.append(product_dict)
            return products_list, 200
        else:
            return {"message": "No Products Found"}, 404


class ProductResource(Resource):
    """API class for CRUD methods involving products"""
    parser = reqparse.RequestParser()
    arguments = ['name', 'image', 'price', 'type', 'stock']
    for argument in arguments:
        parser.add_argument(argument, type=str, required=True,
                            help='Name cannot be blank')

    def get(self, id):
        product = db.session.query(Products).get(id)
        if product:
            product_dict = {
                "product_id": int(product.product_id),
                "name": product.name,
                "image": product.image,
                "price": product.price,
                "type": product.type,
                "stock":  product.stock,
                "date_added": product.date_added.isoformat(),
                "music_info": {} if product.music_info is None else {
                    "album_id": product.music_info.album_id,
                    "name": product.music_info.name,
                    "year": product.music_info.year,
                    "artist": {} if product.music_info.artists is None else {
                        "artist_id": product.music_info.artists.artist_id,
                        "name": product.music_info.artists.name,
                        "bio": product.music_info.artists.bio
                    }
                }
            }
            return product_dict, 200
        else:
            return {"message": "Product Not Found"}, 404

    def post(self):
        args = self.parser.parse_args()
        product_exists = db.session.query(
            Products).filter_by(name=args['name']).first()
        print(product_exists)
        if not product_exists:
            new_product = Products(name=args['name'], image=args['image'],
                                   price=args['price'], type=args['type'], stock=args['stock'])
            db.session.add(new_product)
            db.session.commit()
            return {'product_id': new_product.product_id, 'name': new_product.name, 'image': new_product.image, 'price': new_product.price, 'type': new_product.type, 'stock': new_product.stock}, 201
        else:
            return {"message": "Product Name Already Taken"}, 409

    def put(self, id):
        args = self.parser.parse_args()
        product_exists = db.session.query(
            Products).filter_by(name=args['name']).first()
        print(product_exists)
        if product_exists:
            product_exists.name = args['name']
            product_exists.image = args['image']
            product_exists.price = args['price']
            product_exists.type = args['type']
            product_exists.stock = args['stock']
            db.session.commit()
            return {"product_id": product_exists.product_id, "name": product_exists.name, "image": product_exists.image, "price": product_exists.price, "type": product_exists.type, "stock": product_exists.stock}, 201
        else:
            return {"message": "Product Doesn't Exist"}, 404

    def delete(self, id):
        args = self.parser.parse_args()
        product_exists = db.session.query(
            Products).filter_by(name=args['name']).first()
        if product_exists:
            db.session.delete(product_exists)
            db.session.commit()
            return '', 204
        else:
            return {"message": "Product Doesn't Exist"}, 404
