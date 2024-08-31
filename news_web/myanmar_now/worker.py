from config import setup_logger

class MyanmarNowWorker:
    def __init__(self):
        self.logger = setup_logger(__name__)

    def run(self):
        self.logger.info("Running Myanmar Now Worker")
