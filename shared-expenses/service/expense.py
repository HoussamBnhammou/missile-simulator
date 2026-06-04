def getExpense():
    return True


def createExpense():
    #input expense, user, group, participant, payer, distribution
    expense = 50
    userId = 'u1'
    groupId = 'g1'
    payer = 'u2'
    distribution = {'u1': 50, 'u2' : 50}

    for participant in distribution:
        percentage = distribution[participant]
        expensePerPerson = calculateexpense(percentage, expense)
        #addexpensetoJson()



    return True


def deleteExpense():
    return True


def updateExpense():
    return True