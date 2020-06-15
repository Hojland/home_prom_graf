from dotenv import load_dotenv
load_dotenv()

# PROMETHEUS Module settings
PROMETHEUS_ENABLED = True
PROMETHEUS_PORT = [6080]
PROMETHEUS_HOST = "0.0.0.0"
PROMETHEUS_PATH = "metrics"
PROMETHEUS_UPDATE_INTERVAL = 20

CPH_ID = "2618425"

LOG_LEVEL = "INFO"
PULL_TIME = 60*2 # two minutes
PORT = 6080