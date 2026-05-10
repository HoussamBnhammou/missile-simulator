Rocket simulator

the point of this simulator is to shapre the rocket you want to make, and you can simulate on how that rocket will behave on real life scenarios.


## First step:

Modelize with strpping physical complexity - making the rocket just a point - and calculate the path of the rocket depending on thrust, intial coordination, initial speed, initial angles.

at first we assume the thrus vector is fixed, but we should build the code assuming it will become variable in the future.

implement the variance of the thrus vector by only injecting raw inputs of vector getting changed through time.
    the variance of thrust vector should also be changed through dt, but in our case since it's an input we can't determing how many dt's will be in the missle flight.
    so we will input it's variance through chuncks, just to see the behaviour of the missle.


## Second step

The only way to make simulation more real from here, is to model the rocket physical caracteristics, modeling the rocket includes as a first step

shape
mass distrubtion
    fuel placement
suface material
thrust output behaviour
    thrust output regions.
    number of thrust outputs
    fuel type



translate the rocket model to infromation that can be used upon our calculation of missle path - dierection - drag - heat behavior


## Third step

Re-model the missle path while adding these attributes in consideration.

    Add the vector of the rocket as a varible that is affectet by the 6 mouvements of the rocket that can be affected by thrust direction - gravity and drag etc ...


there is a lot to remodel but i want to make steps with one objective to be tackleabl
Plus i will leave attributes that are not affecting path simulation a lot as the last ones, like rocket skeleton heat and resistance.

## forth step

Re-model the dynamic mouvment of the missle to include drag and thrust behaviour (assuming until now the thrust vector is fixed)

## fifth step

add contol to the missle by controlling thrust vectors in each output, the control will behave through time taking in consideration the missle vector, thrust vector, speed(if necessare), and target.


