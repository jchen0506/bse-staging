from app import create_app
import os
from app import logger


# Determine config settings from environment variables
config_name = os.getenv('FLASK_CONFIG') or 'development'
print('Running Flask with config: ', config_name)

# Setup logging levels
logger.setup_logging(config_name=config_name)

app = create_app(config_name)

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = False
    app.run()
