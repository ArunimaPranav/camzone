from .models import Category, OrderItem

def menu_links(request) :
    categories = Category.objects.all()
    return dict(categories=categories)


def counter(request):
    if request.user.is_authenticated:
        cart_item = OrderItem.objects.filter(user=request.user)
        count=cart_item.count()
    else:
        count = 0
    return dict(count=count)