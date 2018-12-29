from flask import Flask, request
from flask_login import login_required, current_user
app = Flask(__name__)

members = []

day_of_week = 'TUE'
rollbook_db = {}
today = ''

def update_rollbook():
    for member in members:
        if member.day == day_of_week:
            rollbook_db[today][member.id].name = member.name
            rollbook_db[today][member.id].check = False

# it will be scheduled
update_rollbook()


@app.route('/rollbook/<date>', methods=['POST', 'GET', 'PUT', 'FETCH'])
@login_required
def route_rollbook(date):
    if request.method == 'POST':
        member = request.json
        rollbook = rollbook_db[date]
        if member.name in rollbook:
            if rollbook[member.name].check:
                return 'already checked'
            else:
                rollbook[today][member.name] = True
                members[member.id].count -= 1
                return rollbook
        else:
            return 'unbooked'
    elif request.method == 'GET':
        return rollbook_db[date]
    elif request.method == 'PUT':
        rollbook = request.json
        rollbook_db[date] = rollbook
        return 'rollbook updated'
    elif request.method == 'FETCH':
        changes = request.json

        # for key, value in data.items():
        #     rollbook_db[date][key] = value
        return rollbook_db[date]

@app.route('/member/<id>', methods=['POST', 'GET', 'PUT'])
@login_required
def route_member(id):
    if request.method == 'POST':
        member = request.json
        members[id] = member
        return 'updated'
    elif request.method == 'GET':
        return members
    elif request.method == 'PUT':
        member = request.json
        members[member.id] = member
        return 'added'