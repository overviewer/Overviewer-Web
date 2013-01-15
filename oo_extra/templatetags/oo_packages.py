from django import template
from oo_extra.models import Package

DEFAULT_REPO = "git://github.com/overviewer/Minecraft-Overviewer.git"
DEFAULT_CHECKOUT = "master"

register = template.Library()

@register.assignment_tag
def get_latest_package(platform, repo=DEFAULT_REPO, checkout=DEFAULT_CHECKOUT):
    pkgs = Package.objects.filter(platform=platform, repo=repo, checkout=checkout)
    try:
        return pkgs.order_by('-date')[0]
    except IndexError:
        return None
