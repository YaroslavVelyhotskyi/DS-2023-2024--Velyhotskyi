import threading

class ThreadManager:
    def __init__(self):
        self.threads = []
        self.stop_event = threading.Event()

    def addThread(self, beast):
        thread = threading.Thread(target=beast.start,args=(self.stop_event,))
        self.threads.append(thread)
        
    def addThreadPerson(self, person):
        thread = threading.Thread(target=person.start,args=(self.stop_event,))
        self.threads.append(thread)

    def start(self):
        for thread in self.threads:
            print("Starting thread:", thread)
            thread.start()

    def join(self):
        for thread in self.threads:
            thread.join()

    def stop(self):
        self.stop_event.set()
        current_thread = threading.current_thread()
        for thread in self.threads:
            if thread is not current_thread:
                thread.join()
        self.threads.clear()
