from collections import deque
from typing import Optional

import numpy as np
from gym.spaces import Box
from gym import ObservationWrapper


class LazyFrames:

    def __array__(self, dtype=None):
        arr = self[:]
        if dtype is not None:
            return arr.astype(dtype)
        return arr

    def __len__(self):
        return self.shape[0]

    def __eq__(self, other):
        return self.__array__() == other

    def _check_decompress(self, frame):
        if self.lz4_compress:
            from lz4.block import decompress

            return np.frombuffer(decompress(frame), dtype=self.dtype).reshape(
                self.frame_shape
            )
        return frame

    def tobytes(self):
        return np.array(self.__array__()).tobytes()

    def __str__(self):
        return str(self[:])
    

class LazyFrames3D(LazyFrames):
    r"""Ensures common frames are only stored once to optimize memory use.
    To further reduce the memory use, it is optionally to turn on lz4 to
    compress the observations.
    .. note::
        This object should only be converted to numpy array just before forward pass.
    Args:
        lz4_compress (bool): use lz4 to compress the frames internally
    """
    __slots__ = ("frame_shape", "dtype", "shape", "lz4_compress", "_frames")

    def __init__(self, frames, lz4_compress=False):
        self.frame_shape = tuple(frames[0].shape)
        self.shape = (len(frames),) + self.frame_shape
        self.dtype = frames[0].dtype
        if lz4_compress:
            from lz4.block import compress

            frames = [compress(frame) for frame in frames]
        self._frames = frames
        self.lz4_compress = lz4_compress

    def __getitem__(self, int_or_slice):
        if isinstance(int_or_slice, int):
            return self._check_decompress(self._frames[int_or_slice])  # single frame
        return np.stack([self._check_decompress(f) for f in self._frames[int_or_slice]], axis=0)
    
    

class LazyFrames2D(LazyFrames):
    r"""Ensures common frames are only stored once to optimize memory use.
    To further reduce the memory use, it is optionally to turn on lz4 to
    compress the observations.
    Also it stores the frames in a single image expanding the channel width
    .. note::
        This object should only be converted to numpy array just before forward pass.
    Args:
        lz4_compress (bool): use lz4 to compress the frames internally
    """
    __slots__ = ("frame_shape", "dtype", "shape", "lz4_compress", "_frames")

    def __init__(self, frames, lz4_compress=False):

        self.frame_shape = tuple(frames[0].shape)
        self._frames = np.empty((self.frame_shape[:-1] + (0,)))
        self.stacked_num = len(frames)
        self.shape = (self.frame_shape[:-1]) + (self.frame_shape[-1] * len(frames),)
        self.dtype = frames[0].dtype
        if lz4_compress:
            from lz4.block import compress
            frames = [compress(frame) for frame in frames]
            
        for frame in frames:
            self._frames  = np.append(self._frames,frame,2)

        self.lz4_compress = lz4_compress

    def __getitem__(self, int_or_slice):
        if isinstance(int_or_slice, int):
            return self._check_decompress(np.dsplit(self._frames,self.stacked_num)[int_or_slice])  # single frame

        return np.array(self._frames)





class FrameStack(ObservationWrapper):
    r"""Observation wrapper that stacks the observations in a rolling manner.
    .. note::
        To be memory efficient, the stacked observations are wrapped by :class:`LazyFrame`.
    .. note::
        The observation space must be `Box` type. If one uses `Dict`
        as observation space, it should apply `FlattenDictWrapper` at first.
    Example::
        >>> import gym
        >>> env = gym.make('PongNoFrameskip-v0')
        >>> env = FrameStack(env, 4,LazyFrames3D)
        >>> env.observation_space
        Box(4, 210, 160, 3)
    Example 2::
        >>> import gym
        >>> env = gym.make('PongNoFrameskip-v0')
        >>> env = FrameStack(env, 4,LazyFrames2D)
        >>> env.observation_space
        Box(210, 160, 12)
    Args:
        env (Env): environment object
        num_stack (int): number of stacks
        lz4_compress (bool): use lz4 to compress the frames internally
    """

    def __init__(self, env, num_stack,lazyFrame, lz4_compress=False):
        super().__init__(env)
        self.num_stack = num_stack
        self.lz4_compress = lz4_compress
        self.lazyFrame = lazyFrame
        self.frames = deque(maxlen=num_stack)

        low = np.repeat(self.observation_space.low[np.newaxis, ...], num_stack, axis=0)
        high = np.repeat(
            self.observation_space.high[np.newaxis, ...], num_stack, axis=0
        )
        self.observation_space = Box(
            low=low, high=high, dtype=self.observation_space.dtype
        )

    def observation(self):
        assert len(self.frames) == self.num_stack, (len(self.frames), self.num_stack)
        return self.lazyFrame(list(self.frames), self.lz4_compress)

    def step(self, action):
        observation, reward, done, info = self.env.step(action)
        self.frames.append(observation)
        return self.observation(), reward, done, info

    def just_step(self, action):
        self.env.just_step(action)

    def reset(self, **kwargs):
        obs = self.env.reset(**kwargs)
        [self.frames.append(obs) for _ in range(self.num_stack)]
        return self.observation()