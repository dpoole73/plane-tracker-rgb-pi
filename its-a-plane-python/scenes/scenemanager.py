# deals with rotaing the non-plane views

from utilities.animator import Animator
from setup import frames

class SceneManager(object):
    def __init__(self):
        super().__init__()
        self._scene_index = 0
        self._scene_timer = 0
        self._scenes = ['stock', 'weather', 'solar']  # Rotation order
        
    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def scene_rotator(self, count):
        if len(self._data):
            return  # Planes overhead, skip rotation
            
        # Switch scenes every 10 seconds
        if count % 10 == 0:
            self._scene_index = (self._scene_index + 1) % len(self._scenes)
            
        # Set flags for which scene should display
        self._show_stock = (self._scenes[self._scene_index] == 'stock')
        self._show_weather = (self._scenes[self._scene_index] == 'weather')
        self._show_solar = (self._scenes[self._scene_index] == 'solar')