- what i did :
    - programmed the participants_split_helper (psuedocode) 
    - a few design issues appeared and i taught more about them, they are presented below 


- struggles :
    - naming convention is inconsistent, mainly the schema and the models 
    - the codebase is still not in my mind, i have to read all of it everytime i sit down to work on it 


- next step : 
    - YOOOOOO !!!!!! : need to fix naming convention for models and schema, it's DISORIENTING
    - important design stuff we must fix first :
        - leaving and rejoignin in membership (already flagged)
        - soft delete for groups (this is very dangerous, already flagged)
        - some for admin rights in the groups (perhaps created_by)
        - time stamp for the log (perhaps a created_at)
        - maybe a history log ? (if value is 100 and they change we should keep old value somewhere)