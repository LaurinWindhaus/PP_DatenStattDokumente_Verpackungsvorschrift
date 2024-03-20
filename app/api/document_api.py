from flask import Blueprint, request, jsonify, g, render_template
from core.database import Session
from schemas.document_schema import DocumentCreateRequestSchema, DocumentCreateResponseSchema, DocumentUpdateRequestSchema, DocumentUpdateResponseSchemaWithData
from crud.document_crud import get_documents, create_document, get_document, update_document, delete_document
from crud.image_crud import get_all_image_url
from core.document_errors import DocumentNotFoundError, DatabaseOperationError


app = Blueprint('documents', __name__, static_url_path='/dsd/static')


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


@app.route('/dsd/documents/edit/<int:document_id>', methods=['GET'])
def view_document_route(document_id):
    try:
        document = get_document(g.session, document_id)
        images_data = get_all_image_url(g.session, document_id)
        return render_template('document.html', document=document, document_id=document_id, images_count=len(images_data), images_data=images_data)
    except DocumentNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@app.route('/dsd/documents/create', methods=['POST'])
def create_document_route():
    try:
        new_document_request = DocumentCreateRequestSchema.model_validate(request.json)
        new_document = create_document(g.session, new_document_request.artikelnummer, new_document_request.hauptpackvorschrift)
        return jsonify(DocumentCreateResponseSchema(**new_document.to_dict()).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except DatabaseOperationError as e:
        return jsonify({"error": "Database operation failed", "details": str(e.original_exception)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@app.route('/dsd/documents/read/', methods=['GET'])
def get_documents_route():
    artikelnummer = request.args.get('artikelnummer')
    documents = get_documents(g.session, artikelnummer)
    return jsonify([DocumentCreateResponseSchema(**doc.to_dict()).model_dump() for doc in documents]), 20


@app.route('/dsd/documents/update/<int:document_id>', methods=['PUT'])
def update_document_route(document_id):
    try:
        document_data = DocumentUpdateRequestSchema.model_validate(request.json)
        updated_document = update_document(g.session, document_id, document_data.data)
        return jsonify(DocumentUpdateResponseSchemaWithData(**updated_document.to_dict()).model_dump()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except DocumentNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except DatabaseOperationError as e:
        return jsonify({"error": "Database operation failed", "details": str(e.original_exception)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@app.route('/dsd/documents/delete/<int:document_id>', methods=['DELETE'])
def delete_document_route(document_id):
    try:
        delete_document(g.session, document_id)
        return jsonify({"status": "Document deleted successfully"}), 200
    except DocumentNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except DatabaseOperationError as e:
        return jsonify({"error": "Database operation failed", "details": str(e.original_exception)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
