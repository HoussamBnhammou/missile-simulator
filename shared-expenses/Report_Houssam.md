What i did:
Red your design concerns and applied changes accordingly to what i agreed on to be logical.
which includes
    removing expense_split table.
    adding created_at timestamp for activity log
    adding old_value for activity log to have some history.
    adding deleted_at to expense_group to enable soft delete
    changed the files of models  that doesn't reflect the same name of the objects.
    the membership flag already resolved in the last work.
    i don't think adding governance to expense group is good idea. but if we need it, we can add it in the future it won't be a problem.

Finished the membership helper.
added a comment regarding the settling up function in expense participant

Strugles:

Not revising enough the finished work made the lefout mistakes get back to us, have to be more vigilant from this part.

Next step: 

start to think about the calculations that should be done to know what each person owes to the other. (maybe think about it lightly)

participant_split_helper if you didn't do it by the time i start working.