import string
import random
from django.contrib.auth.decorators import login_required  
from sslcommerz_lib import SSLCOMMERZ
from .models import PaymentGateWaySettings

def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
# amra amader j ascii character gulo ache uppercase and digit gulo ache segulo combination
# kore ekta transaction id(string--> 10 size er) create kortechi 

@login_required 
def sslcommerz_payment_gateway(request, id, user_id, grand_total):
    gateway_auth_details = PaymentGateWaySettings.objects.all().first()
    # onek gulo store id theke first id ta nilam ami 
    settings = {'store_id': gateway_auth_details.store_id,
                'store_pass': gateway_auth_details.store_pass, 'issandbox': True}
    # amra store id and pass ta nilam ...interface ta thakbe ki na oi jonno True 
    # payment er j box ta thakbe seta hocche sandbox  
    print("heyyyyyyyy ", settings)
    sslcommez = SSLCOMMERZ(settings) #sslcommerz er moddhe store id and password pass kre dilam
    post_body = {}
    post_body['total_amount'] = grand_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = unique_transaction_id_generator()
    post_body['success_url'] = 'http://127.0.0.1:8000/order/success/'
    post_body['fail_url'] = 'http://127.0.0.1:8000/orders/payment/faild/'
    post_body['cancel_url'] = 'http://127.0.0.1:8000/'
    # jodi tran id er kaj ta complete hoi taile success url e pathay dibo tar jonno url
    # link create korchi or fail/cancel er jonno url boshay dibo 
    post_body['emi_option'] = 0
    post_body['cus_email'] = 'request.user.email'  # Retrieve email from the current user session
    post_body['cus_phone'] = 'request.user.phone'  # Retrieve phone from the current user session
    post_body['cus_add1'] = 'request.user.address'  # Retrieve address from the current user session
    post_body['cus_city'] = 'request.user.city'  # Retrieve city from the current user session
    post_body['cus_country'] = 'Bangladesh'
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"

    # OPTIONAL PARAMETERS
    post_body['value_a'] = id
    post_body['value_b'] = user_id
    post_body['value_c'] = 'email'

    response = sslcommez.createSession(post_body)
    print(response)
    # return JsonResponse(response)
    return 'https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"]