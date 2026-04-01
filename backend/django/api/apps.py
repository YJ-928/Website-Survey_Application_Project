from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        # Import here to avoid circular import issues
        from api.utils.default_admin import create_default_super_admin
        from api.utils.seed_locations import seed_nalgonda_locations
        from api.utils.seed_survey_schema import seed_survey_schema_data
        from api.utils.seed_survey_responses import seed_balanced_survey_responses
        
        # Always ensure default super admin exists
        post_migrate.connect(
            create_default_super_admin,
            sender=self,
        )

        # Seed master data only if explicitly enabled
        if getattr(settings, "SEED_DATA", False):
            post_migrate.connect(
                seed_nalgonda_locations,
                sender=self,
            )
            post_migrate.connect(
                seed_survey_schema_data,
                sender=self
            )
            post_migrate.connect(
                seed_balanced_survey_responses,
                sender=self
            )
