# src/envs/multi_carrier_env.py
import gym
from gym import spaces
import numpy as np
from ..fragmenter import fragment_bytes

class MultiCarrierEnv(gym.Env):
    """
    Action: integer: choose carrier index for next fragment.
    Observation: vector of carrier states + fragments remaining info.
    Simplified for initial testing.
    """
    def __init__(self, carriers, fragments, max_steps=100):
        super().__init__()
        self.carriers = carriers  # list of carrier metadata dicts
        self.fragments = fragments  # list of fragment dicts
        self.max_steps = max_steps
        # Example obs: for each carrier capacity_norm, distortion_norm; plus fragments_remaining
        obs_len = len(carriers)*2 + 1
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(obs_len,), dtype=np.float32)
        self.action_space = spaces.Discrete(len(carriers))  # choose which carrier for next frag
        self.reset()

    def reset(self):
        self.step_idx = 0
        self.assigned = []  # list of (frag_id, carrier_id)
        return self._get_obs()

    def _get_obs(self):
        vals = []
        for c in self.carriers:
            vals.append(c.get("capacity_norm", 1.0))
            vals.append(c.get("distortion_norm", 0.0))
        vals.append(len(self.fragments) - len(self.assigned))  # remaining
        return np.array(vals, dtype=np.float32)

    def step(self, action):
        # assign next fragment to carrier action
        fr = self.fragments[len(self.assigned)]
        carrier = self.carriers[action]
        self.assigned.append((fr["id"], action))
        self.step_idx += 1

        done = (len(self.assigned) >= len(self.fragments)) or (self.step_idx >= self.max_steps)

        # Simulate immediate small distortion and compute partial reward (placeholder)
        reward = -carrier.get("distortion_norm", 0.0) * 0.1
        info = {}
        return self._get_obs(), reward, done, info
