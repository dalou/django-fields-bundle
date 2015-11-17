try:
    default_app_config = 'fields_bundle.DefaultConfig'

    from django.apps import AppConfig

    class DefaultConfig(AppConfig):
        name = 'fields_bundle'
        verbose_name = u"Fields bundle"
except:
    # Prevent from package setup
    pass


