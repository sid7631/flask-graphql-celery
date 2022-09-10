import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType


from app.models.user_models import User as UserModel, Role as RoleModel, UsersRoles as UsersRolesModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node,)


class UserAttribute:
    email = graphene.String()
    username = graphene.String()
    email_confirmed_at = graphene.DateTime()
    password = graphene.String()
    active = graphene.Boolean()
    first_name = graphene.String()
    last_name = graphene.String()


class CreateUserInput(graphene.InputObjectType, UserAttribute):
    pass


class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel
        interfaces = (graphene.relay.Node,)


class UsersRoles(SQLAlchemyObjectType):
    class Meta:
        model = UsersRolesModel
        interfaces = (graphene.relay.Node,)