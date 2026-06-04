Rocket simulator

the point of this simulator is to shapre the rocket you want to make, and you can simulate on how that rocket will behave on real life scenarios.


## First step:

Modelize with strpping physical complexity - making the rocket just a point - and calculate the path of the rocket depending on thrust, intial coordination, initial speed, initial angles.

at first we assume the rocket body orientation vector is fixed, but we should build the code assuming it will become variable in the future.

implement the variance of body orientation by only injecting raw inputs of vector getting changed through time.
    the orientation vector should also be changed through dt, but in our case since it's an input we can't determing how many dt's will be in the missle flight.
    so we will input it's variance through chuncks, just to see the behaviour of the missle.

Important design rule:
    orientation_vec = where the rocket nose/body points.
    path_vec        = where the rocket is actually moving, from velocity.
    These two vectors must stay separate. The body vector is used for thrust and aerodynamic angle-of-attack calculations. The path vector is used for drag and trajectory.

Rigid-body design rule:
    The rocket is no longer only a point.
    position and velocity describe the center of mass.
    orientation is stored as a quaternion [q0, q1, q2, q3].
    angular velocity [wx, wy, wz] describes how fast the body rotates.
    Force torque is calculated with torque = r x F around the center of mass.


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



translate the rocket model to infromation that can be used upon our calculation of missle path - orientation - drag - lift - heat behavior

Current simple shape model:
    cylinder length
    cylinder radius
    center of mass in the middle
    gravity, drag, and lift apply at center of mass
    thrust applies at the center of the rear circular face
    inertia is calculated from mass, length, and radius


## Third step

Re-model the missle path while adding these attributes in consideration.

    Add the orientation quaternion of the rocket as a varible that is affectet by the 6 mouvements of the rocket that can be affected by torque from thrust direction - gravity and drag etc ...


there is a lot to remodel but i want to make steps with one objective to be tackleabl
Plus i will leave attributes that are not affecting path simulation a lot as the last ones, like rocket skeleton heat and resistance.

## forth step

Re-model the dynamic mouvment of the missle to include drag and thrust behaviour (assuming until now the body orientation vector is fixed)

## fifth step

add contol to the missle by controlling thrust vectors in each output, the control will behave through time taking in consideration the orientation vector, path vector, speed(if necessare), and target.
