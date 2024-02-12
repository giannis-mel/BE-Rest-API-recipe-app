"""
Views for the recipe APIs
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """
        Retrieve recipes for the authenticated user, with optional filtering
        by tags and ingredients.
        """

        # Retrieve query parameters for 'tags' and 'ingredients' from the request
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')

        # Start with the default queryset (all recipes)
        queryset = self.queryset

        # If 'tags' parameter is provided, filter the queryset by those tags
        if tags:
            tag_ids = self._params_to_ints(tags)  # Convert 'tags' to a list of integers
            queryset = queryset.filter(tags__id__in=tag_ids)  # Filter by tag IDs

        # If 'ingredients' parameter is provided, do the same for ingredients
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)  # Convert 'ingredients' to a list of integers
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)  # Filter by ingredient IDs

        # Finally, filter the queryset to only include recipes of the authenticated user
        # Order by descending ID and remove duplicates
        return queryset.filter(user=self.request.user).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.',
            ),
        ]
    )
)
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    # Authentication and permission classes for the ViewSet
    # TokenAuthentication: Uses token-based authentication
    # IsAuthenticated: Ensures only authenticated users access the API
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset to authenticated user.
        This method overrides the default queryset to return only the tags
        that belong to the currently authenticated user, ordered by name.
        """

        # Retrieve the 'assigned_only' parameter from the request's query parameters.
        # If 'assigned_only' is not provided, it defaults to 0 (False).
        # Convert the parameter to an integer, and then to a boolean.
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )

        # Start with the default queryset as defined in the viewset.
        queryset = self.queryset

        # If 'assigned_only' is True, modify the queryset to include only those
        # tags that are assigned to a recipe (i.e., filter out tags not assigned to any recipe).
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        # Further filter the queryset to include only tags that belong to the
        # currently authenticated user. Then order the results by the tag name
        # in descending order and remove any duplicates.
        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    """
    Manage tags in the database.
    This class handles the creation, update, and listing of tags.
    It uses mixins to add specific functionalities.
    """
    # Serializer class for converting Tag instances to and from JSON
    serializer_class = serializers.TagSerializer
    # The default set of records the ViewSet will operate on
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
