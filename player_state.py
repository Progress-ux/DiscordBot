# player_state.py
from collections import deque

class PlayerState:
    def __init__(self):
        self.track_queue = deque()
        self.track_history = deque()
        self.current_track = None
        self.should_play_next = True
        self.isRepeat = False
    
    def addTrack(self, title, url):
        self.track_queue.append((title, url))
    
    def popNextTrack(self):
        if self.isRepeat and self.current_track:
            return self.current_track
        elif self.track_queue:
            self.current_track = self.track_queue.popleft()
            self.track_history.append(self.current_track)
            return self.current_track
        return (None, None)
    

    def getQueueList(self):
        return list(self.track_queue)

    def getHistoryList(self):
        return list(self.track_history)
    
    def backTrack(self):
        if len(self.track_history) > 1:
            self.track_queue.appendleft(self.current_track)
            self.track_history.pop()
            self.current_track = self.track_history[-1]
            return self.current_track
        return (None, None)
    
    def clearAll(self):
        self.track_queue.clear()
        self.track_history.clear()
        self.current_track = None
        self.should_play_next = True
        self.isRepeat = False