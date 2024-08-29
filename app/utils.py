from flask import request, session


def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')


def cart_stats(cart):
    total_amount, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity']*c['price']

    return {
        "total_amount": total_amount,
        "total_quantity": total_quantity
    }

# def cashier_stats(cartCashier):
#     total_amount, total_quantity = 0, 0
#
#     if cartCashier:
#         for c in cartCashier.values():
#             total_quantity += c['quantity']
#             total_amount += c['quantity']*c['price']
#
#     return {
#         "total_amount": total_amount,
#         "total_quantity": total_quantity
#     }
