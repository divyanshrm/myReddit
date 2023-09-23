from django import template
from groups.models import GroupMember

register = template.Library()

@register.simple_tag(takes_context=True)
def get_user_groups(context):
    user = context['request'].user
    if user.is_authenticated:
        return GroupMember.objects.filter(user=user)
    return GroupMember.objects.none()
