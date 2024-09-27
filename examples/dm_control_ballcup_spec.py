"""Finds a heuristic policy for the ball in cup task.

On every iteration, improve policy_v1 over the policy_vX methods from previous iterations.
Make only small changes. Try to make the code short. 
"""

import numpy as np
import funsearch
from dm_control import suite


@funsearch.run
def solve(num_runs) -> float:
  """Returns the reward for a heuristic.
  """
  env = suite.load(domain_name="ball_in_cup", task_name="catch")
  obs_spec = env.observation_spec()
  action_spec = env.action_spec()
  avg_reward = 0.0
  for _ in range(num_runs):
    time_step = env.reset()
    initialize_to_zero(env)
    total_reward = 0.0
    obs = concatenate_obs(time_step, obs_spec)
    # sum_diff = 0.0
    for _ in range(1000):
      action = heuristic(obs)
      action = np.clip(action, -1, 1)
      time_step = env.step(action)
      obs = concatenate_obs(time_step, obs_spec)
      obs[3] -= 0.3
      total_reward += time_step.reward # +1 if ball in cup, 0 otherwise
      total_reward += custom_reward(obs)
    avg_reward += total_reward
  return avg_reward / num_runs

def concatenate_obs(time_step, obs_spec):
  return np.concatenate([time_step.observation[k].ravel() for k in obs_spec])

def initialize_to_zero(env):
  env.physics.named.data.qpos['ball_x'][0] = 0.0
  env.physics.named.data.qpos['ball_z'][0] = 0.0

def custom_reward(obs: np.ndarray) -> float:
  x_cup = obs[0]
  z_cup = obs[1]
  x_ball = obs[2]
  z_ball = obs[3]
  angle = np.arctan2(x_ball - x_cup, z_ball - z_cup)
  return 1 - np.abs(angle)/np.pi

@funsearch.evolve
def heuristic(obs: np.ndarray) -> np.ndarray:
  """Returns an action between -1 and 1.
  obs size is 8. return size is 2.
  """
  
  
  return np.zeros((2,))