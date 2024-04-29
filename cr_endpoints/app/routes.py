import time, uuid
from flask import Blueprint, request, jsonify, Response
from app.controllers.search_controller import search
from app.controllers.generation_controller import generate_response
from app.models import Conversation
from datetime import datetime
from .models import db

milvus_bp = Blueprint("milvus", __name__)


@milvus_bp.route("/uid", methods=["GET"])
def generate_uid():
    uid = str(uuid.uuid4())
    return jsonify({"uid": uid})


@milvus_bp.route("/search", methods=["POST"])
def milvus_search():
    data = request.get_json()
    query = data["query"]

    if not query:
        return jsonify({"error": "Query parameter not provided"}), 400

    
    ret_list = search(query, filters=None)

    augmented_response = generate_response(query, ret_list)
    if "I could not find an answer." in augmented_response:
        return jsonify({"augmented_response": augmented_response})
    
    if ret_list:
        retrivals_list = []

        for ret in ret_list:
            ret_score, ret_id, ret_spec, ret_cr_number, ret_impacted_version, ret_status, ret_title, ret_source, ret_summary = ret
            retrival = {
                "id" : ret_id,
                "score": ret_score,
                "spec": ret_spec,
                "cr_number": ret_cr_number,
                "impacted_version": ret_impacted_version,
                "retstatus": ret_status,
                "title" : ret_title,
                "Source" : ret_source,
                "summary"  : ret_summary
            }
            retrivals_list.append(retrival)

    response = {
        "retrivals": retrivals_list,
        "augmented_response": augmented_response
    }

    return jsonify(response)


@milvus_bp.route("/logs", methods=["POST"])
def chat_logs():
    try:
        uid = request.form['uid']
        logs = request.form['logs']

        conversation = Conversation(
            conversation_id=uid,
            messages=logs,
            created_at=datetime.utcnow(),
        )

        db.session.add(conversation)

        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                }
            ),
            200,
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500