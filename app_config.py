
# Common config settings
class Config:
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False

# Settings for testing
class TestEnv(Config):
    DEBUG = True
    CSV_FILENAME = 'test_item_database.csv'
    TEMPLATES_AUTO_RELOAD = True

# Settings for live
class LiveEnv(Config):
    CSV_FILENAME = 'item_database.csv'
