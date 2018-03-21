import graphene

import app.teams.mutations
import app.teams.queries
import app.strands.mutations
import app.strands.queries
import app.users.mutations
import app.users.queries


class Query(app.strands.queries.Query, app.teams.queries.Query,
            app.users.queries.Query, graphene.ObjectType):
    pass


class Mutation(app.strands.mutations.Mutation, app.teams.mutations.Mutation,
               app.users.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
