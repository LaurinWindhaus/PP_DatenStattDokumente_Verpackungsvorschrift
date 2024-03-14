from flask import Flask, render_template, request, jsonify, g
from core.database import init_db, Session
from Models import Documents, Images
import requests

# Initialize the database
init_db()

# Create a Flask app
app = Flask(__name__, static_url_path='/dsd/static')

@app.before_request
def before_request():
    # Initialize a new session for each request
    g.session = Session()

@app.teardown_request
def teardown_request(exception=None):
    # Close the session at the end of each request
    session = g.get('session')
    if session is not None:
        session.close()


@app.route('/dsd/document/edit/<document_id>', methods=['GET'])
def view_document(document_id):
    document = g.session.query(Documents).filter(Documents.document_id == document_id).first()
    if not document:
        return jsonify({"error": "Document not found"}), 404
    images_data = get_all_image_url(document_id)
    if images_data is None:
        images_data = []
    return render_template('document.html', document=document, document_id=document_id, images_count=len(images_data), images_data=images_data)


@app.route('/dsd/document/create', methods=['POST'])
def create_item():
    data = request.json
    required_fields = ['artikelnummer', 'hauptpackvorschrift']
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({"error": "Missing fields", "missing_fields": missing_fields}), 400
    new_document = Documents(
        artikelnummer=data['artikelnummer'],
        hauptpackvorschrift=data['hauptpackvorschrift'],
        data={}
    )
    g.session.add(new_document)
    try:
        g.session.commit()
    except Exception as e:
        g.session.rollback()
        return jsonify({"error": "Database error: Kombination aus Artikelnummer und Hauptpackvorschrift bereits vorhanden"}), 500
    return jsonify({
        'id': new_document.document_id, 
        'artikelnummer': new_document.artikelnummer, 
        'hauptpackvorschrift': new_document.hauptpackvorschrift
    }), 201


@app.route('/dsd/document/read/', methods=['GET'])
def read_items():
    artikelnummer = request.args.get('artikelnummer')
    query = g.session.query(Documents)

    if artikelnummer:
        query = query.filter(Documents.artikelnummer.like(f"%{artikelnummer}%"))

    result = [
        {
            'document_id': item.document_id,
            'artikelnummer': item.artikelnummer,
            'hauptpackvorschrift': item.hauptpackvorschrift,
        }
        for item in query.all()
    ]
    return jsonify(result), 200


@app.route('/dsd/document/update/<item_id>', methods=['PUT'])
def update_item(item_id):
    item = g.session.query(Documents).filter(Documents.document_id == item_id).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.json
    item.data = data.get('data', item.data)
    try:
        g.session.commit()
        return jsonify({
            'id': item.document_id, 
            'artikelnummer': item.artikelnummer, 
            'hauptpackvorschrift': item.hauptpackvorschrift,
            'data': item.data
        }), 200
    except Exception as e:
        g.session.rollback()
        return jsonify({"error": "Database error: Kombination aus Artikelnummer und Hauptpackvorschrift bereits vorhanden"}), 500


@app.route('/dsd/document/delete/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = g.session.query(Documents).filter(Documents.document_id == item_id).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404
    try:
        g.session.delete(item)
        g.session.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        g.session.rollback()
        return jsonify({"error": "Database error"}), 500



# IMAGE ROUTES


def get_all_image_url(document_id):
    images = g.session.query(Images).filter(Images.document_id == document_id).order_by(Images.created_at.asc()).all()
    if not images:
        return []
    return images


@app.route('/dsd/image/read/<document_id>', methods=['GET'])
def get_all_images(document_id):
    image_urls = get_all_image_url(document_id)
    return jsonify(image_urls), 200


@app.route('/dsd/image/upload', methods=['POST'])
def upload_image():
    document_id = request.json.get('document_id')
    image_url  = request.json.get('url')
    width = request.json.get('width')
    height = request.json.get('height')

    validate_document_id = g.session.query(Documents).filter(Documents.document_id == document_id).first()
    if validate_document_id is None:
        return jsonify({"error": "Document not found"}), 404

    new_image = Images(
        document_id=document_id,
        url=image_url,
        width=width,
        height=height
    )
    g.session.add(new_image)
    g.session.commit()

    return jsonify({"status": "success", "message": "Image uploaded successfully"}), 201


@app.route('/dsd/image/update/<document_id>', methods=['PUT'])
def update_image(document_id):
    images = request.json.get('images')
    for image in images:
        image_url = image.get('image_url')
        width = int(float(image.get('width').replace("px", "")))
        height = int(float(image.get('height').replace("px", "")))
        print(width, height, image_url)

        update_image = g.session.query(Images).filter(Images.url == image_url, Images.document_id == document_id).first()
        if not update_image:
            print("Error")
            return jsonify({"error": "Image not found"}), 404
        update_image.width = width
        update_image.height = height

    try:
        g.session.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        g.session.rollback()
        return jsonify({"error": "Database error: "}), 500


@app.route('/dsd/image/delete', methods=['DELETE'])
def delete_image():
    image_url = request.json.get('image_url')
    document_id = request.json.get('document_id')

    image = g.session.query(Images).filter(Images.url == image_url, Images.document_id == document_id).first()
    if not image:
        return jsonify({"error": "Image not found"}), 404
    try:
        g.session.delete(image)
        g.session.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        g.session.rollback()
        return jsonify({"error": "Database error"}), 500



if __name__ == '__main__':
    app.run(debug=True)