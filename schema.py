from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from .models import EmailActivation
from django.contrib.auth import password_validation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_tools.filter import lookups
from graphene_tools import types as graphene_types

# TODO: clean this massy imports
User = get_user_model()


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ('password',)
        filter_fields = {
            'full_name': lookups.TEXT_LOOKUPS,
            'username': lookups.TEXT_LOOKUPS,
            'is_admin': ['exact'],
            'is_active': ['exact'],
        }
        interfaces = (graphene.relay.Node, )


class CreateUser(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserNode)

    class Input:
        password = graphene.String(required=True)
        email = graphene_types.Email(required=True)
        full_name = graphene.String(required=True)
        username = graphene.String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        password_validation.validate_password(input.get('password'))
        user = User.objects.create_user(
            email=input.get('email'),
            full_name=input.get('full_name'),
            username=input.get('username'),
            password=input.get('password'),
        )
        # TODO: raise password and full_clean errors together
        return CreateUser(user=user)


class VerifyKey(graphene.relay.ClientIDMutation):
    email = graphene.String()

    class Input:
        key = graphene.String(required=True)
        email = graphene_types.Email(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        email = EmailActivation.objects.verify_key(key=input.get('key'), email=input.get('email'))
        return VerifyKey(email=email)


class Query(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    verify_key = VerifyKey.Field()
