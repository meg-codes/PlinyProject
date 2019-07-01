DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # Django needs to make databases in the test mysql server
        'NAME': 'pliny',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'OPTIONS': {
            # In each case, we want strict mode on to catch truncation issues
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            # Load the socket info from .my.cnf in the travis user
            'read_default_file': '~travis/.my.cnf'
        },
        'PORT': '',
        'TEST': {
                # We also want the test databse to for utf8 and the general
                # collation to keep case sensitive unicode searches working
                # as we would expect on production
                'CHARSET': 'utf8',
                'COLLATION': 'utf8_general_ci',
                'OPTIONS': {
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                },
            },
    },
}
