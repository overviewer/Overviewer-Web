from django import template
from oo_extra.models import Package, Build

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

@register.assignment_tag
def get_latest_build(builder, repo=DEFAULT_REPO, branch=DEFAULT_CHECKOUT):
    pkgs = Build.objects.filter(builder=builder, branch=branch)
    try:
        return pkgs.order_by('-date')[0]
    except IndexError:
        return None
