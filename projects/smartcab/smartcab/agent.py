import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.qTable = {}
        self.learningRate = .7
        self.discountFactor = .4
        self.epsilon = .25

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = tuple(inputs.items()) + tuple({'waypoint': self.next_waypoint}.items())
        # print "HI THERE BABABAAAAAA", self.next_waypoint

        # TODO: Select action according to your policy
        actions = ["forward", 'right', 'left', None]

        # find the state in the table, if not initialize
        # if state found in table, select an action
        # print "HI", type(self.state), type(self.qTable)
        # print self.state, self.qTable
        if self.state in self.qTable:
            # print "hi"
            # decide to explore or to exploit
            if random.random() < self.epsilon:
                # take a random move
                action = random.choice(actions)
            else:
                # take action from policy
                action = random.choice(self.defaultQuery(self.qTable[self.state]))

        # if state not found in table, then initialize and choose a random action
        else:
            self.qTable[self.state] = {'left': 0.0, 'right': 0.0, 'forward': 0.0, None: 0.0}
            action = random.choice(actions)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        self.qTable[self.state][action] += self.learningRate * (reward - self.qTable[self.state][action])

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

    def defaultQuery(self, mapping):
        highest = max(mapping.values())
        actions = [k for k, v in mapping.items() if v == highest]
        return actions


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
