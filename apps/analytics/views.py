from datetime import date, timedelta
from decimal import Decimal
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth

from apps.bookings.models import Booking
from apps.rooms.models import Room


@staff_member_required
def dashboard_view(request):
    """Дашборд со статистикой для владельца."""

    # ========================================
    # Общие показатели
    # ========================================
    all_bookings = Booking.objects.all()
    confirmed_bookings = all_bookings.filter(status__in=['confirmed', 'completed'])

    total_bookings = all_bookings.count()
    total_confirmed = confirmed_bookings.count()
    total_revenue = confirmed_bookings.aggregate(
        s=Sum('total_price')
    )['s'] or Decimal('0')

    avg_check = total_revenue / total_confirmed if total_confirmed else 0

    # ========================================
    # Данные по месяцам (последние 12 месяцев)
    # ========================================
    today = date.today()
    start_date = today - timedelta(days=365)

    monthly_data = (
        Booking.objects
        .filter(created_at__gte=start_date)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            count=Count('id'),
            revenue=Sum('total_price', filter=Q(status__in=['confirmed', 'completed'])),
        )
        .order_by('month')
    )

    months_labels = []
    months_count = []
    months_revenue = []

    month_names = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
                   'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

    for row in monthly_data:
        month = row['month']
        months_labels.append(f"{month_names[month.month - 1]} {month.year}")
        months_count.append(row['count'])
        months_revenue.append(float(row['revenue'] or 0))

    # ========================================
    # Топ-5 популярных номеров
    # ========================================
    popular_rooms = (
        Booking.objects
        .values('room__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    rooms_labels = [r['room__name'] for r in popular_rooms]
    rooms_count = [r['count'] for r in popular_rooms]

    # ========================================
    # Статусы броней
    # ========================================
    status_data = (
        all_bookings
        .values('status')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    status_map = dict(Booking.STATUS_CHOICES)
    status_labels = [status_map.get(s['status'], s['status']) for s in status_data]
    status_counts = [s['count'] for s in status_data]

    # ========================================
    # Загрузка на сегодня
    # ========================================
    today_bookings = Booking.objects.filter(
        check_in__lte=today,
        check_out__gt=today,
        status__in=['confirmed', 'pending'],
    ).count()

    total_rooms = sum(r.quantity for r in Room.objects.filter(is_active=True))
    occupancy = round((today_bookings / total_rooms * 100) if total_rooms else 0, 1)

    # ========================================
    # Контекст для шаблона
    # ========================================
    context = {
        # KPI-карточки
        'total_bookings': total_bookings,
        'total_confirmed': total_confirmed,
        'total_revenue': total_revenue,
        'avg_check': round(avg_check, 0),
        'occupancy': occupancy,

        # Графики (передаём как JSON-строки)
        'months_labels': json.dumps(months_labels),
        'months_count': json.dumps(months_count),
        'months_revenue': json.dumps(months_revenue),

        'rooms_labels': json.dumps(rooms_labels),
        'rooms_count': json.dumps(rooms_count),

        'status_labels': json.dumps(status_labels),
        'status_counts': json.dumps(status_counts),
    }

    return render(request, 'analytics/dashboard.html', context)