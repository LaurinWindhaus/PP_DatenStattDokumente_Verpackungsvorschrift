from flask import Blueprint, request, jsonify, g
from core.database import Session
from schemas.image_schema import ImageReadResponseSchema, ImageCreateRequestSchema, ImageUpdateRequestSchema, ImageDeleteRequestSchema
from crud.image_crud import get_all_image_url, upload_image, update_image, delete_image
from core.image_errors import ImageNotFoundError, DatabaseOperationError
from core.document_errors import DocumentNotFoundError

app = Blueprint('images', __name__, static_url_path='/dsd/static')


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


@app.route('/dsd/images/read/<int:document_id>', methods=['GET'])
def get_all_images_route(document_id):
    try:
        # Attempt to retrieve all image URLs for the given document ID
        images = get_all_image_url(g.session, document_id)
        # If successful, return the list of images
        return jsonify([ImageReadResponseSchema(**img.to_dict()).model_dump() for img in images]), 200
    except ImageNotFoundError as e:
        # Handle case where no images are found for the document
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@app.route('/dsd/images/upload', methods=['POST'])
def upload_image_route():
    try:
        # Validate request data using your schema
        new_image_request = ImageCreateRequestSchema.model_validate(request.json)
        # Attempt to upload the new image
        new_image = upload_image(g.session, new_image_request.document_id, new_image_request.url, new_image_request.width, new_image_request.height)
        # If successful, return success response
        return jsonify({"status": "success", "image": {"image_id": new_image.image_id, "url": new_image.url, "width": new_image.width, "height": new_image.height, "created_at": new_image.created_at}}), 201
    except ValueError as e:
        # Handle schema validation errors
        return jsonify({"error": str(e)}), 400
    except DocumentNotFoundError as e:
        # Handle case where the specified document does not exist
        return jsonify({"error": str(e)}), 404
    except DatabaseOperationError as e:
        # Handle generic database operation errors
        return jsonify({"error": "Database operation failed", "details": str(e.original_exception)}), 500
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@app.route('/dsd/images/update/<int:document_id>', methods=['PUT'])
def update_image_route(document_id):
    try:
        # Validate request data using your schema
        updated_images_request = ImageUpdateRequestSchema.model_validate(request.json)
        # Attempt to update the images
        update_image(g.session, document_id, updated_images_request.images)
        # If successful, return success response
        return jsonify({"status": "success"}), 200
    except ValueError as e:
        # Handle schema validation errors
        return jsonify({"error": str(e)}), 400
    except ImageNotFoundError as e:
        # Handle case where an image to update is not found
        return jsonify({"error": str(e)}), 404
    except DatabaseOperationError as e:
        # Handle generic database operation errors
        return jsonify({"error": "Database operation failed", "details": str(e.original_exception)}), 500
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    

@app.route('/dsd/images/delete', methods=['DELETE'])
def delete_image_route():
    try:
        # Validate request data using your schema
        delete_image_request = ImageDeleteRequestSchema.model_validate(request.json)
        # Attempt to delete the image
        delete_image(g.session, delete_image_request.document_id, delete_image_request.url)
        # If successful, return success response
        return jsonify({"status": "success"}), 200
    except ValueError as e:
        # Handle schema validation errors
        return jsonify({"error": str(e)}), 400
    except ImageNotFoundError as e:
        # Handle case where the image to delete is not found
        return jsonify({"error": str(e)}), 404
    except DatabaseOperationError as e:
        # Handle generic database operation errors
        return jsonify({"error": "Database operation failed", "details": str(e.original_exception)}), 500
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500