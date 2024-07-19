from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from rest_framework.pagination import PageNumberPagination
from apps.reviews.models.review_model import Review
from apps.reviews.serializers.review_serializer import ReviewSerializer
from apps.core.permissions.moderator_or_super import IsModeratorOrSuperUser


class PendingReviewViewSet(viewsets.ModelViewSet):
    """
   Handles operations for listing pending reviews.

   @queryset: Review.objects.filter(status=False).order_by('-created_at') : QuerySet : Pending reviews ordered by creation date
   @serializer_class: ReviewSerializer : Serializer : Review serializer
   @permission_classes: [IsModeratorOrSuperUser] : List : Permissions required to access the view
   @pagination_class: PageNumberPagination : Pagination : Pagination class used by the viewset
   """
    queryset = Review.objects.filter(status=False).order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [IsModeratorOrSuperUser]
    pagination_class = PageNumberPagination


@api_view(['GET'])
@permission_classes([IsModeratorOrSuperUser])
def pending_reviews_view(request):
    """
    Render a template with the list of pending reviews.

    @param request: Request : Request object containing the request data

    @return: Response : Rendered HTML template with pending reviews and pagination
    """
    reviews = Review.objects.filter(status=False).order_by('-created_at')
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(page, many=True)
    return render(request, 'pending_reviews.html', {'reviews': page, 'paginator': paginator})


@api_view(['GET'])
@permission_classes([IsModeratorOrSuperUser])
def pending_reviews_list(request):
    """
    Retrieve a paginated list of pending reviews in JSON format.

    @param request: Request : Request object containing the request data

    @return: Response : JSON response with paginated list of pending reviews
    """
    reviews = Review.objects.filter(status=False).order_by('-created_at')
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsModeratorOrSuperUser])
def approve_review(request, review_id):
    """
    Approve a pending review by setting its status to True.

    @param request: Request : Request object containing the request data
    @param review_id: int : ID of the review to be approved

    @return: Response : Redirect to the pending reviews page
    """
    review = Review.objects.get(id=review_id)
    review.status = True
    review.save()
    return redirect('pending_reviews')


@api_view(['GET', 'POST'])
@permission_classes([IsModeratorOrSuperUser])
def reject_review(request, review_id):
    """
    Reject a pending review by deleting it.

    @param request: Request : Request object containing the request data
    @param review_id: int : ID of the review to be rejected

    @return: Response : Redirect to the pending reviews page
    """
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect('pending_reviews')
