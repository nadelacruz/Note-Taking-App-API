import os
import flask_cors as cors
from flask import Flask, request, jsonify
from database import Database
from note import Note
from llm import LangModel

API_KEY = os.environ.get('API_KEY')
MODEL_PATH = os.environ.get('MODEL_PATH')
MODEL_TYPE = os.environ.get('MODEL_TYPE')
os.environ["OPENAI_API_KEY"] = API_KEY

llm = LangModel(API_KEY, MODEL_PATH, MODEL_TYPE)

app = Flask(__name__)
cors.CORS(app)

db = Database("database.db")


def generate_summary(content):
    summary = llm.generate_summary(content)
    print(str(summary))
    return str(summary)


@app.route('/')
def home():
    return 'Welcome to the Note Taking App API!'


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'GET':
        total_notes = db.read_all_notes()
        notes_dict = [note.to_dict() for note in total_notes]
        return jsonify(notes_dict)
    elif request.method == 'POST':
        data = request.json
        content = data['content']
        note = Note(None, data['title'], content, generate_summary(content))
        db.add_note(note)
        return jsonify(note.to_dict())


@app.route('/notes/<int:note_id>', methods=['GET', 'PUT', 'DELETE'])
def note_details(note_id):
    note_data = db.read_note_by_id(note_id)
    if note_data is None:
        return jsonify({'error': f'Note with id {note_id} not found'}), 404
    note = Note(*note_data[0:])
    if request.method == 'GET':
        return jsonify(note.to_dict())
    elif request.method == 'PUT':
        data = request.json
        title = data.get('title', note.title)
        content = data.get('content', note.content)
        note.update(title=title, content=content, summary=None)
        note.summary = generate_summary(content)
        db.update_note_by_id(note_id, note.title, note.content, note.summary)
        return jsonify(note.to_dict())
    elif request.method == 'DELETE':
        db.delete_note_by_id(note_id)
        return '', 204


@app.route('/notes/<string:note_content>', methods=['GET'])
def search_notes(note_content):
    found_note = db.search_notes(note_content)
    if found_note is None:
        return jsonify({'error': f'Note with content {note_content} not found'}), 404
    notes_dict = [note.to_dict() for note in found_note]
    return jsonify(notes_dict)


@app.route('/keep-alive')
def keep_alive():
    return 'Server is running!'
