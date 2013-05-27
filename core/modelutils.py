import logging

logger = logging.getLogger(__name__)

def get_user(user_id, name):
    from default.models import User

    # if user already exists retrieve it, otherwise create a new one
    usr = None
    try:
        usr = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        logger.debug("A user with ID '%i' doesn't exist yet. Adding the user to the database."%user_id)
        usr = User(user_id=user_id, name=name)
        usr.save()
    return usr


def get_project(project_name):
    from default.models import Project

    # if project exists retrieve it, otherwise create a new one
    prj = None
    try:
        prj = Project.objects.get(name=project_name)
    except Project.DoesNotExist:
        logger.debug("A project with the name '%s' doesn't exist yet. Adding the project to the database."%project_name)
        prj = Project(name=project_name)
        prj.save()
    return prj