# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ga0c$9bzy#+nhy-f$3r@r=j8b0yexhxd)m_^rpoa#8o+hjzy#m'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'movies',
        'USER': 'nrogers',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
