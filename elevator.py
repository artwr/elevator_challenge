import logging

UP = 1
DOWN = 2
FLOOR_COUNT = 6

def direction_sign(direction):
    return 1 - 2 * (direction - 1)

def other_direction(direction):
    return 3 - direction

class ElevatorLogic(object):
    """
    An incorrect implementation. Can you make it pass all the tests?

    Fix the methods below to implement the correct logic for elevators.
    The tests are integrated into `README.md`. To run the tests:
    $ python -m doctest -v README.md

    To learn when each method is called, read its docstring.
    To interact with the world, you can get the current floor from the
    `current_floor` property of the `callbacks` object, and you can move the
    elevator by setting the `motor_direction` property. See below for how this is done.
    """

    def __init__(self):
        # Feel free to add any instance variables you want.
        self.destination_floor = None
        self.last_destination_floor = None
        self.previous_direction = None
        self.destinations = dict()
        self.destinations[UP] = set()
        self.destinations[DOWN] = set()
        self.callbacks = None

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        self.destination_floor = floor
        self.destinations[direction].add(floor)
        if self.destination_floor == self.callbacks.current_floor:
            self.callbacks.motor_direction = None


    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        self.destination_floor = floor
        dest_diff = self.destination_floor - self.callbacks.current_floor
        if dest_diff < 0:
            self.destinations[DOWN].add(floor)
            # self.callbacks.motor_direction = DOWN if not self.callbacks.motor_direction
        elif dest_diff > 0:
            self.destinations[UP].add(floor)
            # self.callbacks.motor_direction = UP if not self.callbacks.motor_direction
        else:
            if self.callbacks.motor_direction:
                self.destinations[other_direction(self.callbacks.motor_direction)].add(floor)


            

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        logging.info("Curr dir = {}".format(self.callbacks.motor_direction))
        if ((self.callbacks.current_floor, self.callbacks.motor_direction)
                in [(FLOOR_COUNT, UP), (1, DOWN)]):
            self.previous_direction = self.callbacks.motor_direction
            self.callbacks.motor_direction = None
            return

        is_curr_floor_a_dest_in_curr_dir = self.callbacks.current_floor in self.destinations[self.callbacks.motor_direction]
        # is_up_dest = self.callbacks.current_floor in self.destinations[UP]
        # is_down_dest = self.callbacks.current_floor in self.destinations[DOWN]
        if is_curr_floor_a_dest_in_curr_dir:
            self.previous_direction = self.callbacks.motor_direction
            self.destinations[self.callbacks.motor_direction].remove(self.callbacks.current_floor)
            # if is_up_dest: self.destinations[UP].remove(self.callbacks.current_floor)
            # if is_down_dest: self.destinations[DOWN].remove(self.callbacks.current_floor)
            self.callbacks.motor_direction = None


    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        if self.previous_direction:
            logging.info("Has previous dir : {}".format(self.previous_direction))
            other_dir = other_direction(self.previous_direction)
            s = direction_sign(self.previous_direction)
            so = direction_sign(other_dir)
            if self.destinations[self.previous_direction]:
                if any([s*(f-self.callbacks.current_floor) > 0 for f in self.destinations[self.previous_direction]]):
                    self.callbacks.motor_direction = self.previous_direction
                else:
                    self.callbacks.motor_direction = other_dir
            elif self.destinations[other_dir]:
                if any([so*(f-self.callbacks.current_floor) > 0 for f in self.destinations[other_dir]]):
                    self.callbacks.motor_direction = other_dir
        else:
            if self.destinations[UP]:
                if any([f-self.callbacks.current_floor > 0 for f in self.destinations[UP]]):
                    self.callbacks.motor_direction = UP
                else:
                    self.callbacks.motor_direction = DOWN
            elif self.destinations[DOWN]:
                if any([f-self.callbacks.current_floor < 0 for f in self.destinations[DOWN]]):
                    self.callbacks.motor_direction = DOWN
                else:
                    self.callbacks.motor_direction = UP
            else:
                self.callbacks.motor_direction = None
