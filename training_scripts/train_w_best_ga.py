#!/usr/bin/env python3

# Simple self-play PPO trainer

import os
import gym
import slimevolleygym
from slimevolleygym.mlp import makeSlimePolicyLite
import numpy as np

from stable_baselines.ppo1 import PPO1
from stable_baselines.common.policies import MlpPolicy
from stable_baselines import logger
from stable_baselines.common.callbacks import EvalCallback

from shutil import copyfile # keep track of generations

# Settings
SEED = 17
NUM_TIMESTEPS = int(1e7)
EVAL_FREQ = int(1e5)
EVAL_EPISODES = int(1e2)
BEST_THRESHOLD = -0.5 # must achieve a mean score above this to replace prev best self

RENDER_MODE = False # set this to false if you plan on running for full 1000 trials.

EPSILON = 0

LOGDIR = "best_opponent_ga"

class SlimeVolleySelfPlayEnv(slimevolleygym.SlimeVolleyEnv):
  # wrapper over the normal single player env, but loads the best self play model
  def __init__(self):
    super(SlimeVolleySelfPlayEnv, self).__init__()
    self.policy = self
    self.best_model_filename = os.path.join(LOGDIR, "opponent.json")
    self.best_model = makeSlimePolicyLite(self.best_model_filename)
    self.baselinePolicy = slimevolleygym.BaselinePolicy()

    self.possible_policies = [self.best_model, self.baselinePolicy]
    self.policy_picked = 0

  def predict(self, obs): # the policy 
    action = None
    if self.policy_picked == 0: # best_model
      action = self.best_model.predict(obs)
    else: # baseline
      action = self.baselinePolicy.predict(obs)
    return action

  def reset(self):
    self.policy_picked = 0
    if EPSILON > 0:
      self.policy_picked = np.random.choice(len(self.possible_policies), p=[EPSILON, 1-EPSILON])

    return super(SlimeVolleySelfPlayEnv, self).reset()

class SelfPlayCallback(EvalCallback):
  # hacked it to only save new version of best model if beats prev self by BEST_THRESHOLD score
  # after saving model, resets the best score to be BEST_THRESHOLD
  def __init__(self, *args, **kwargs):
    super(SelfPlayCallback, self).__init__(*args, **kwargs)
    self.best_mean_reward = BEST_THRESHOLD
    self.generation = 0
  def _on_step(self) -> bool:
    result = super(SelfPlayCallback, self)._on_step()
    if result and self.best_mean_reward > BEST_THRESHOLD:
      self.generation += 1
      print("SELFPLAY: mean_reward achieved:", self.best_mean_reward)
      print("SELFPLAY: new best model, bumping up generation to", self.generation)
      source_file = os.path.join(LOGDIR, "best_model.zip")
      backup_file = os.path.join(LOGDIR, "history_"+str(self.generation).zfill(8)+".zip")
      copyfile(source_file, backup_file)
      self.best_mean_reward = BEST_THRESHOLD
    return result

def rollout(env, policy):
  """ play one agent vs the other in modified gym-style loop. """
  obs = env.reset()

  done = False
  total_reward = 0

  while not done:

    action, _states = policy.predict(obs)
    obs, reward, done, _ = env.step(action)

    total_reward += reward

    if RENDER_MODE:
      env.render()

  return total_reward

def train():
  # train selfplay agent
  logger.configure(folder=LOGDIR)

  env = SlimeVolleySelfPlayEnv()
  env.seed(SEED)

  # take mujoco hyperparams (but doubled timesteps_per_actorbatch to cover more steps.)
  model = PPO1(MlpPolicy, env, timesteps_per_actorbatch=4096, clip_param=0.2, entcoeff=0.0, optim_epochs=10,
                   optim_stepsize=3e-4, optim_batchsize=64, gamma=0.99, lam=0.95, schedule='linear', verbose=2)

  eval_callback = SelfPlayCallback(env,
    best_model_save_path=LOGDIR,
    log_path=LOGDIR,
    eval_freq=EVAL_FREQ,
    n_eval_episodes=EVAL_EPISODES,
    deterministic=False)

  model.learn(total_timesteps=NUM_TIMESTEPS, callback=eval_callback)

  model.save(os.path.join(LOGDIR, "final_model")) # probably never get to this point.

  env.close()

if __name__=="__main__":

  train()
