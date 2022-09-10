import graphene


from app.database import db
from app.models.user_models import User as UserModel
from app.types.user_types import User, CreateUserInput
from app.utils.input_to_dictionary import input_to_dictionary


class CreateUser(graphene.Mutation):
    user = graphene.Field(lambda: User)
    ok = graphene.Boolean()

    class Arguments:
        input = CreateUserInput(required=True)

    @staticmethod
    def mutate(self, info, input):
        data = input_to_dictionary(input)
        user = UserModel( **data )
        db.session.add(user)
        db.session.commit()
        ok = True
        return CreateUser(user=user, ok=ok)


class Mutation(graphene.ObjectType):
    createUser = CreateUser.Field()
