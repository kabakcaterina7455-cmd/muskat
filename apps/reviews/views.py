from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from apps.rooms.models import Room
from .forms import ReviewForm


@method_decorator(login_required, name='dispatch')
class ReviewCreateView(View):
    """Форма добавления отзыва. Только для авторизованных."""

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id, is_active=True)
        form = ReviewForm()
        return render(request, 'reviews/review_form.html', {
            'room': room,
            'form': form,
        })

    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id, is_active=True)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.room = room
            review.user = request.user
            review.is_moderated = False
            review.save()
            messages.success(request, "Спасибо за отзыв! Он появится после модерации.")
            return redirect('rooms:detail', slug=room.slug)
        return render(request, 'reviews/review_form.html', {
            'room': room,
            'form': form,
        })