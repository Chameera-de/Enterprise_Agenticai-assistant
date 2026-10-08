from collections import defaultdict, deque
class SessionMemory:
    def __init__(self,max_turns=12): self.data=defaultdict(lambda:deque(maxlen=max_turns))
    def add(self,user_id,role,content): self.data[user_id].append({'role':role,'content':content})
    def get(self,user_id): return list(self.data[user_id])
memory=SessionMemory()
