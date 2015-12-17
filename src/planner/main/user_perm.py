from django.contrib.auth.models import User, Permission


def batch():
    CALLCENTER_PERMISSION = Permission.objects.get(codename='callcenter')
    VIEWERS_PERMISSION = Permission.objects.get(codename='viewers')
    for user in User.objects.filter(is_active=True).all():
        user.user_permissions.add(VIEWERS_PERMISSION, CALLCENTER_PERMISSION)
        user.save()
