import os

DATA_PROCESSING_ACTUATOR_TIMER = 10 if os.environ.get('MODE', 'dev') != "test" else 1  # 30
