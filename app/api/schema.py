import graphene

import app.groups.mutations
import app.groups.queries
import app.users.mutations
import app.users.queries


class Query(app.groups.queries.Query, app.users.queries.Query, graphene.ObjectType):
    pass


class Mutation(app.groups.mutations.Mutation, app.users.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
