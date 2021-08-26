#!/usr/bin/env python3

from flask import Flask, abort, jsonify, send_file
import os

from utils.objects.FileObject import FileObj

app = Flask(__name__)

def can_access() -> bool:
    return True


@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def query(req_path):
    BASE_DIR = '/home/'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    if can_access():
        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            return abort(404)

        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            return send_file(abs_path, as_attachment=True)
        # If dir build
        elif os.path.isdir(abs_path):
            # Show directory contents
            files = os.listdir(abs_path)
            files_obj = list()
            for filename in files:
                file_obj = FileObj(abs_path, filename).to_JSON_dict()
                if not file_obj == None:
                    files_obj.append(file_obj)
            return jsonify(files_obj)
        else:
            return abort(418)
    else:
        return abort(401)

def register_blueprints(path:str):
    try:
        from flask_server.responses import responses_blueprint
        app.register_blueprint(responses_blueprint)
    except Exception as error:
        print(f"Unable to load blueprint: {error}")


if __name__ == "__main__":
    register_blueprints("somewhere")
    app.run()
