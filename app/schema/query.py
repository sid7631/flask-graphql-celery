import graphene
from graphene import relay

from app.models.user_models import User as UserModel, Role as RoleModel
from app.types.user_types import User


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    users_by_username = graphene.List(User, name=graphene.String())
    users_by_role = graphene.List(User, name=graphene.String())

    @staticmethod
    def resolve_users_by_username(parent, info, **args):
        q = args.get('name')

        users_query = User.get_query(info)

        return users_query.filter(UserModel.username.contains(q)).all()

    @staticmethod
    def resolve_users_by_role(parent, info, **args):
        q = args.get('name').lower()

        users_query = User.get_query(info)

        return users_query.filter(UserModel.roles.any(RoleModel.name == q)).all()