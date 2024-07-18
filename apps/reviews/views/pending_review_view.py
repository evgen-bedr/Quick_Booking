# apps/reviews/views/pending_review_view.py

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from rest_framework.pagination import PageNumberPagination
from apps.reviews.models.review_model import Review
from apps.reviews.serializers.review_serializer import ReviewSerializer
from apps.core.permissions.moderator_or_super import IsModeratorOrSuperUser

class PendingReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.filter(status=False).order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [IsModeratorOrSuperUser]
    pagination_class = PageNumberPagination

@api_view(['GET'])
@permission_classes([IsModeratorOrSuperUser])
def pending_reviews_view(request):
    reviews = Review.objects.filter(status=False).order_by('-created_at')
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(page, many=True)
    return render(request, 'pending_reviews.html', {'reviews': page, 'paginator': paginator})

@api_view(['GET'])
@permission_classes([IsModeratorOrSuperUser])
def pending_reviews_list(request):
    reviews = Review.objects.filter(status=False).order_by('-created_at')
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsModeratorOrSuperUser])
def approve_review(request, review_id):
    review = Review.objects.get(id=review_id)
    review.status = True
    review.save()
    return redirect('pending_reviews')

@api_view(['GET', 'POST'])
@permission_classes([IsModeratorOrSuperUser])
def reject_review(request, review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect('pending_reviews')
