DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'b2tech',
        'USER': 'admin',
        'PASSWORD': 'wecode!!',
        'HOST': 'database-1.cx1nsexwbsnv.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}

SECRET_KEY = 'django-insecure-1=65-oer&n20@y!hi#m@m_pnv2nwkgdy8^f@g19dhfycs7g$p8'
