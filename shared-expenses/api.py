from flask import FLASK
from flask import request
from service.expense import getExpense, createExpense, updateExpense, deleteExpense
from service.group import deleteGroup, getGroup, updateGroup, CreateGroup
from service.user import getUser, deleteUser, updateUser, createUser

app = FLASK(__name__)




@app.route("/Group", methods=['GET', 'POST', 'DELETE', 'PATCH'])
def Group():
    if request.method == 'GET':
        return getGroup()
    
    if request.method == 'POST':
        return CreateGroup()
    
    if request.method == 'DELETE':
        return deleteGroup()
    
    if request.method == 'PATCH':
        return updateGroup()
    


@app.route("/Expense", methods=['GET', 'POST', 'DELETE', 'Patch'])
def Expense():
    if request.method == 'GET':
        return getExpense()
    
    if request.method == 'POST':
        return createExpense()
    
    if request.method == 'DELETE':
        return deleteExpense()
    
    if request.method == 'PATCH':
        return updateExpense()
    

@app.route("/User", methods=['GET', 'POST', 'DELETE', 'Patch'])
def User():
    if request.method == 'GET':
        return getUser()

    
    if request.method == 'POST':
        return createUser()

    if request.method == 'DELETE':
        return deleteUser()

    if request.method == 'PATCH':
        return updateUser()

