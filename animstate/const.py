import os

# Project info
PROJECT_ROOT_DIR = os.path.dirname(__file__)

# Resources
REL_RESOURCES_DIR = 'resources'
FULL_RESOURCES_DIR = os.path.join(PROJECT_ROOT_DIR, REL_RESOURCES_DIR)

# UI
UI_KEY = 'ui'
FULL_UI_DIRECTORY = os.path.join(FULL_RESOURCES_DIR, UI_KEY)
