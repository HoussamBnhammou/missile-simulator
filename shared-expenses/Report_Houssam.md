what i did:
    since you mentioned the struggle of testing, i also think building more code without testing on this point will make it very chaotic, we need to test each service we add now and to do that we need an end to end implemntation, which include the db also.
    that's why i sacrificed this hour to add a local databasae that can easily be run  from each person's laptop. i dockerised and added it to a folder with the infromation needed for it, to start it up you just need to run the start script existing there.
    made sure to update the databse service so it can support this local postgres db, it reflect the same credential that we use to create it.
    i will leave the env files exposed in the repo, since the db is local now, nothing to worry about, and we will save oursevles from the hustle of sending these credentials on what's app.

strugles: 
    making things work locally can be a stubborn specially using work laptop hwere they restric using some images :/ but postgres worked eventually, and i def think it will work for you too.
    have no idea on how to visualide the db since i was only using sqldevlopper which is not natively compatible with postgres.

Next step: 

    i need to add in the app the feature of writing the whole schema and tables using sqlalchemy create option, and from there we are all set from the database side.
    aside from that i will see what you will do tmorrow on routes and pick up from there to help.