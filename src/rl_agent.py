import random

class SimpleRLAgent:
    """
    Dummy RL agent that randomly assigns chunks to image or audio.
    Replace with TensorFlow/PyTorch RL model later.
    """
    def __init__(self):
        pass

    def assign(self, chunks, cover_files):
        """
        Assign chunks to cover files randomly.
        cover_files = list of ("image", "path") or ("audio", "path")
        returns: list of (chunk, cover_file_path)
        """
        assignments = []
        for chunk in chunks:
            cover_type, path = random.choice(cover_files)
            assignments.append((chunk, path))
        return assignments
