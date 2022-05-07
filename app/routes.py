from sqlalchemy import asc, desc
from app import db
from app.models.task import Task 
from flask import Blueprint, abort, jsonify, make_response, request
import datetime
from sqlalchemy.sql.functions import now 


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {
        "details": "Invalid data"
    }, 400
        #return make_response("Invalid Request", 400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"]
                    )

    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]
    #new_task.completed_at == None
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
            }
            }), 201


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    task_query = request.args
    if "sort" in task_query:
        if task_query["sort"] == "desc":
            tasks = Task.query.order_by(desc(Task.title)).all()
        else: 
            tasks = Task.query.order_by(asc(Task.title)).all()
    
    else:
        tasks = Task.query.all()
    

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
    return jsonify(tasks_response)



##### helper function #####
def validate_task(id_of_task):
    try:
        id_of_task = int(id_of_task)
    except:
        abort(make_response({"message":f"task {id_of_task} invalid"}, 400))

    task = Task.query.get(id_of_task)

    if not task:
        abort(make_response({"message":f"task {id_of_task} not found"}, 404))

    return task
##### helper function #####


@tasks_bp.route("/<id_of_task>", methods=["GET"])
def read_one_task(id_of_task):
    task = validate_task(id_of_task)
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
            }
            })


@tasks_bp.route("/<id_of_task>", methods=["PUT"])
def replace_task(id_of_task):
    task = validate_task(id_of_task)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }
            })

@tasks_bp.route("/<id_of_task>/mark_complete", methods=["PATCH"])
def update_task_complete(id_of_task):
    task = validate_task(id_of_task)
    #request_body = request.get_json()

    # try:
    #     task.title = request_body["title"]
    #     task.description = request_body["description"]
    
    # except KeyError:
    #     return {"details": "mark task is required"}, 400

    task.completed_at = datetime.datetime.now()
    db.session.commit()

    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }
            }), 200

@tasks_bp.route("/<id_of_task>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(id_of_task):
    task = validate_task(id_of_task)
    #request_body = request.get_json()

    # try:
    #     task.title = request_body["title"]
    #     task.description = request_body["description"]
    
    # except KeyError:
    #     return {"details": "mark task is required"}, 400

    task.completed_at = None 
    db.session.add(task)
    db.session.commit()

    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }
            }), 200




@tasks_bp.route("/<id_of_task>", methods=["DELETE"])
def delete_task(id_of_task):
    task = validate_task(id_of_task)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task 1 "{task.title}" successfully deleted'
    }
    #"details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"