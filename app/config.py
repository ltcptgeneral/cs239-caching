import os
import yaml

CONFIG_FILE = "config.yaml"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

config = load_config()

# Read from environment variable or fallback to YAML value
CACHE_STRATEGY = os.getenv("CACHE_STRATEGY", config.get("cache_strategy", "Baseline"))
CACHE_LIMIT = config.get("cache_limit", 10)
L2_CACHE_LIMIT = config.get("l2_cache_limit", 100)
DB_FILE = config.get("db_file", "llmData_sns.json")
