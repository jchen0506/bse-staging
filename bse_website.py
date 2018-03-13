from app import create_app
import os
from app import logger


# Determine config settings from environment variables
config_name = os.getenv('FLASK_CONFIG') or 'development'

# Setup logging levels
logger.setup_logging(config_name=config_name)

app = create_app(config_name)


if __name__ == "__main__":
    app.run(debug=True)
