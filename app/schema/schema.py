import graphene

from app.schema.query import Query
from app.schema.mutation import Mutation

from app.types.user_types import User, Role, UsersRoles

schema = graphene.Schema(query=Query, mutation=Mutation, types=[User, Role, UsersRoles ])