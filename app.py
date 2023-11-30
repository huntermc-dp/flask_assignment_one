from flask import Flask, jsonify
import json

app = Flask(__name__)


def database_read():
    try:
        with open("database.json", "r") as openfile:

            return json.load(openfile)

    except:
        return []


def database_write(records):
    with open("database.json", "r") as outfile:
        json.dump(records, outfile)


@app.route('/user', methods=['POST'])
def users_add():
    post_data = request.form if request.form else request.json

    user = {
        "user_id": str(uuid4()),
        "name": post_data["name"],
        "description": post_data["description"],
        "price": post_data["price"],
        "active": True

    }
    user_records = database_read()
    user_records.append(user)

    database_write(user_records)

    return jsonify(f"user {user['name']} has been added"), 201


@app.route('/user', methods=['GET'])
def user_get_all():
    user_records = database_read()

    if len(user_records) == 0:

        return jsonify(f"No users were found!!!"), 404

    return jsonify(user_records), 200


@app.route('/user/<user_id>', methods=['GET'])
def user_get_by_id(user_id):
    user_records = database_read()

    if len(user_records) == 0:

        return jsonify(f"No users were found!!!"), 404

    for user in user_records:
        if user['user_id'] == int(id):

            return jsonify(user), 200

    return jsonify(f"user with id: {user_id} not fount!!!"), 404


@app.route('/user/<user_id>', methods=['PATCH'])
def user_activity(user_id):
    user_records = database_read()

    if len(user_records) == 0:

        return jsonify(f"No users were found!!!"), 404

    for user in user_records:
        if user['user_id'] == user_id:
            user['active'] = not user['active']

            database_write(user_records)

            if user['active']:

                return jsonify(f"user has been activated"), 200

    return jsonify(f"user with id: {user_id} not fount!!!"), 404


@app.route('/user/<user_id>', methods=['DELETE'])
def user_delete_by_id(user_id):
    user_records = database_read()

    if len(user_records) == 0:

        return jsonify(f"No users were found!!!"), 404

    for user, index in enumerate(user_records):
        if user['user_id'] == user_id:
            user_records.pop(index)

            database_write(user_records)

            return jsonify(f"user with user id:{user_id} has been bannished!!!"), 200

    return jsonify(f"user with user id:{user_id} not found"), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8086', debug=True)
