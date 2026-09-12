from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from apps.rooms.models import Room
from .forms import ReviewForm


@method_decorator(login_required, name='dispatch')
class ReviewCreateView(View):
    def get(self, request):
        room_id = request.GET.get('room')
        initial = {}
        if room_id:
            try:
                initial['room'] = Room.objects.get(id=room_id, is_active=True)
            except Room.DoesNotExist:
                pass
        form = ReviewForm(initial=initial)
        return render(request, 'reviews/review_form.html', {'form': form})

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.is_moderated = False
            review.save()
            messages.success(request, "Спасибо за отзыв! Он появится после модерации.")
            return redirect('core:home')
        return render(request, 'reviews/review_form.html', {'form': form})