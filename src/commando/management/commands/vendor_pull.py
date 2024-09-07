from django.conf import settings
from django.core.management.base import BaseCommand

import helpers

VENDORSTATIC_FILE = getattr(settings, "STATICFILES_VENDOR_DIR")

VENDOR_STATIC_FILES = {
    "flowbite.min.js": "https://cdn.jsdelivr.net/npm/flowbite@2.5.1/dist/flowbite.min.js",
    "flowbite.min.css": "https://cdn.jsdelivr.net/npm/flowbite@2.5.1/dist/flowbite.min.css",
}


class Command(BaseCommand):
    def handle(self, *args: any, **options: any):
        self.stdout.write("Downloading vendor files")

        completed_url = []
        for name, url in VENDOR_STATIC_FILES.items():
            out_path = VENDORSTATIC_FILE / name
            dl_sucess = helpers.download_to_local(url, out_path)
            if dl_sucess:
                completed_url.append(url)
            else:
                self.stdout.write(self.style.ERROR(f"failled to download {url}"))
        if set(completed_url) == set(VENDOR_STATIC_FILES.values()):
            self.stdout.write(
                self.style.SUCCESS("Sucessfully updated vendor static files")
            )
        else:
            self.stdout.write(self.style.WARNING("Some files are not updated"))
