from flask import Blueprint, jsonify, request, render_template
from backend.db import db
from models.states import State

states_bp = Blueprint('states', __name__, template_folder="templates")


@states_bp.route("/states")
def states():
    all_states = State.query.all()
    return render_template('states/state.html', states=all_states)


@states_bp.route("/states/<int:state_id>")
def read_state(state_id):
    state = State.query.get(state_id)
    if state is None:
        return jsonify({"message": "Статья не найдена"}), 404

    return render_template('states/state_detail.html', state=state)


@states_bp.route("/states", methods=['POST'])
def create_state():
    data = request.get_json()
    new_state = State(
        title=data['title'],
        content=data['content'],
        image_url=data['image_url']
    )
    db.session.add(new_state)
    db.session.commit()
    return jsonify({"message": "Статья успешно создан!"}), 201


@states_bp.route('/states/<int:state_id>', methods=['GET'])
def get_state(state_id):
    state = State.query.get(state_id)
    if state:
        return jsonify({
            "id": state.id,
            "title": state.title,
            "content": state.content,
            "image_url": state.image_url

        }), 200
    return jsonify({"message": "Статья не найден"}), 404


@states_bp.route("/states", methods=['GET'])
def delete_state(state_id):
    state = State.query.get(state_id)
    if state:
        db.session.delete(state)
        db.session.commit()
        return jsonify({"message": "Статья успешно удалена!"}), 200
    return jsonify({"message": "Статья не найдена"}), 404
