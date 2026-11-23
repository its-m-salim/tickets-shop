from django.shortcuts import render, get_object_or_404, redirect
from .views import*
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import*
from django.db.models import Q, Sum



def home_page(request):
    return render(request, 'home.html')



def registration(request):
    if request.method == "POST":
        data = request.POST
        if User.objects.filter(username = data['username']).exists():
            return redirect('registration')

        user = User.objects.create_user(
            username = data['username'],
            password=data['password']
        )
        login(request, user)
        return redirect('home')

    return render(request, 'registration.html')



def login_user(request):
    if request.method == 'POST':
        data = request.POST

        user = authenticate(username = data['username'], password = data['password'])

        if user is None:
            return redirect("login")
        
        login(request, user)

        return redirect('home')
    return render(request, 'login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


def home(request):
    games = Game.objects.all()

    upcoming_games = games.filter(status__in=['live', 'not_started']).order_by('date')[:3]

    stats = {
        'clubs': Team.objects.filter(is_active=True).count(),
        'sports': Category.objects.filter(is_active=True).count(),
        'games': games.count(),
        'tickets_left': games.aggregate(total=Sum('tickets'))['total'] or 0,
    }

    context = {
        'categories': Category.objects.filter(is_active=True),
        'upcoming_games': upcoming_games,
        'teams': Team.objects.filter(is_active=True)[:6],
        'stats': stats,
    }
    return render(request, 'home.html', context)


def show_teams(request):
    q = request.GET.get('q')

    teams = Team.objects.filter(is_active=True)
    if q:
        teams = teams.filter(name__icontains=q)

    return render(request, 'show_teams.html', {'teams': teams, 'q': q})



def show_games(request):

    games = Game.objects.all().order_by("date")
    
    if request.method == "GET":
        q = request.GET.get('q', '').strip()
        categories = request.GET.getlist("category")


        if q:
            games = games.filter(Q(team1__name__icontains=q) | Q(team2__name__icontains=q))
        
        if categories:
            games = games.filter(category__in=categories)
        
    context = {
        'games': games,
        'categories': Category.objects.filter(),
        'q': q,
        'selected_categories': categories,
        }
    return render(request, 'show_games.html', context)





def show_game(request, pk):
    game = get_object_or_404(Game, pk = pk)
    return render(request, "show_game.html", {'game': game})


@login_required
def create_order(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if request.method == 'POST':
        data = request.POST
        Order.objects.create(
            user = request.user,
            game = game,
            count = data['count']
        )

        game.tickets = game.tickets - int(data['count'])
        game.save()
        
        return redirect("show_orders")
    return render(request, 'create_order.html', {"game": game})




@login_required
def show_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'show_orders.html', {'orders': orders})





@login_required
def edit_order(request, pk):

    order = get_object_or_404(Order, pk =pk)

    if request.method == 'POST':
        data = request.POST
        game = order.game
        game.tickets = game.tickets + order.count - int(data['count'])
        game.save()

        order.count = data['count']
        order.save()

        return redirect("show_orders")

    return render(request, 'edit_order.html', {'order': order})




@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk =pk)

    if request.method == "POST":
        game = order.game
        game.tickets = game.tickets + order.count
        game.save()
        order.delete()

        return redirect("show_orders")

    return render(request, "delete_order.html", {"order": order})






@login_required
def show_team(request, pk):
    team = get_object_or_404(Team, pk =pk)
    return render(request, 'show_team.html', {"team": team})