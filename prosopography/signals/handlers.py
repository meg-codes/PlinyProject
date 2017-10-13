from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from prosopography.models import Relationship

RECIPROCAL_RELATIONSHIP_MAP = {
        Relationship.ANCESTOR: Relationship.DESCENDANT,
        Relationship.DESCENDANT: Relationship.ANCESTOR,
        Relationship.SIBLING: Relationship.SIBLING,
        Relationship.PARENT: Relationship.CHILD,
        Relationship.CHILD: Relationship.PARENT,
        Relationship.AMICUS: Relationship.AMICUS,
        Relationship.CONCIVIS: Relationship.CONCIVIS,
        Relationship.FAMILIA: Relationship.FAMILIA
        }


@receiver(post_save, sender=Relationship)
def make_reciprocal(sender, **kwargs):
    # Get the old instance and its attributes
    instance = kwargs['instance']
    if instance.relationship_type == 'oth':
        return 0
    old_from = instance.from_person
    old_to = instance.to_person
    old_relationship = instance.relationship_type
    # prep a new one
    new_instance = Relationship(
            from_person=old_to,
            to_person=old_from,
            relationship_type=RECIPROCAL_RELATIONSHIP_MAP[old_relationship]
            )
    post_save.disconnect(make_reciprocal, sender=sender)
    new_instance.save()
    post_save.connect(make_reciprocal, sender=sender)


@receiver(post_delete, sender=Relationship)
def delete_reciprocal(sender, **kwargs):
    instance = kwargs['instance']
    old_from = instance.from_person
    old_to = instance.to_person
    relationship_type = instance.relationship_type

    try:
        recip_instance = Relationship.objects.get(
                    from_person=old_to,
                    to_person=old_from,
                    relationship_type=
                    RECIPROCAL_RELATIONSHIP_MAP[relationship_type]
                )
        recip_instance.delete()
    except ObjectDoesNotExist:
        pass





