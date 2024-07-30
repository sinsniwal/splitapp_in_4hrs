from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .models import CustomUser, User, Expense
from django.shortcuts import render


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from django.http import HttpResponse
from rest_framework.views import APIView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Create your views here.
@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello, world!", "status": 200})


@api_view(["GET"])
def isLoggedin(request):
    a = JWTAuthentication().authenticate(request)
    if a:
        return Response({"message": "User is logged in."})
    else:
        return Response({"message": "User is not logged in."})


class LoginAPI(APIView):
    def post(self, request):
        if request.method == "POST":
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response(
                    {
                        "message": "Username and password are required.",
                        "status": status.HTTP_400_BAD_REQUEST,
                    }
                )

            user = CustomUser.objects.filter(username=username).first()
            print(user)
            if user:
                authenticated_user = authenticate(username=username, password=password)
                if authenticated_user:
                    refresh = RefreshToken.for_user(user)
                    print("Validated")
                    return Response(
                        {
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                            "status": 200,
                            "usertype": user.user_type,
                        }
                    )
                    return render(request, "blog.html")
                else:
                    return Response({"message": "Invalid Credentials", "status": 400})
            else:
                return Response({"message": "User does not exist", "status": 400})



#create user
class RegisterAPI(APIView):
    def post(self, request):
        try:
            if CustomUser.objects.filter(
                username=request.data.get("username")
            ).exists():
                return Response({"message": "Username already exists", "status": 400})
            if request.data.get("user_type") == "user":
                try:
                    # first create customUser
                    # create normal user
                    user = CustomUser()
                    user.username = request.data.get("username")
                    user.first_name = request.data.get("first_name")
                    user.last_name = request.data.get("last_name")
                    user.set_password(request.data.get("password"))
                    user.user_type = request.data.get("user_type")
                    user.email=request.data.get("email")
                    user.save()
                    newuser = User()
                    newuser.user = user
                    newuser.email = request.data.get("email")
                    newuser.save()
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                            "status": 200,
                            "usertype": user.user_type,
                        }
                    )
                except Exception as e:
                    print(e)
                    return Response({"message": "Invalid Data", "status": 400})
            
            else:
                print(request.data.get("user_type"))
                print("else")
                return Response({"message": "Invalid Data", "status": 400})
        except Exception as e:
            print(e)
            return Response({"message": "Invalid Data", "status": 400})


@api_view(["GET"])
def getUser(request,id):
    user=User.objects.filter(id=id).first()
    print(user)
    return Response({"message": "Invalid Data", "status": 400})


class AddExpense(APIView):
    def post(self, request):
        try:
            if request.data.get("type") == "new":
                try:
                    newexpense = Expense()
                    total_amount=int(request.data.get("total_amount"))

                    if request.data.get("split_method")=="equal":
                        usernames=request.data.get("users")# eval as list of usernames 
                        usernames=eval(usernames)
                        amount_per_user=int(total_amount/len(usernames))
                        users=[]
                        details={
                            "total_amount":total_amount
                        }
                        extra={}
                        for username in usernames:
                            extra[username]=amount_per_user
                        details.update(extra)
                        details=str(details)
                        newexpense.split_method="equal"
                        newexpense.details=details
                        newexpense.save()

                        for username in usernames:
                            user=User.objects.get(user__username=username)
                            users.append(user)
                        try:
                           newexpense.user.add(*users)
                        except Exception as e:
                            return Response({"message": "Invalid Data", "status": 400})

                    elif request.data.get("split_method")=="exact":
                        userdata=request.data.get("users")# eval as list of usernames 
                        userdata=eval(userdata)
                        testamount=0
                        for amount in userdata.values():
                            amount=int(amount)
                            testamount+=amount
                        if total_amount!=testamount:
                            return Response({"message": "Total Amount does not add up, please fix it.", "status": 400})



                        details={
                            "total_amount":total_amount,
                        }
                        details.update(userdata)
                        details=str(details)
                        newexpense.split_method="exact"
                        newexpense.details=details
                        newexpense.save()
                        users=[]
                        for username,amount in userdata.items():
                            user=User.objects.get(user__username=username)
                            users.append(user)
                        try:
                           newexpense.user.add(*users)
                        except Exception as e:
                            return Response({"message": "Invalid Data", "status": 400})


                    elif request.data.get("split_method")=="percentage":
                        userdata=request.data.get("users")# eval as list of usernames 
                        userdata=eval(userdata)

                        testpercentage=0
                        for percentage in userdata.values():
                            percentage=int(percentage)
                            testpercentage+=percentage
                        if testpercentage!=100:
                            return Response({"message": "Percentage does not add up to 100%, please fix it.", "status": 400})

                        details={
                        }
                        details.update(userdata)
                        details=str(details)
                        newexpense.split_method="percentage"
                        newexpense.details=details

                        newexpense.save()
                        users=[]
                        for username,amount in userdata.items():
                            user=User.objects.get(user__username=username)
                            users.append(user)
                        try:
                           newexpense.user.add(*users)
                        except Exception as e:
                            return Response({"message": "Invalid Data", "status": 400})

                    else:
                        return Response({"message": "Invalid Data", "status": 400})
                    
                    return Response(
                        {
                            "message": "Expense Added",
                            "status": 200,
                        }
                    )
                except:
                    return Response({"message": "Invalid Data", "status": 400})
            
            else:
                return Response({"message": "Invalid Data", "status": 400})
        except:
            return Response({"message": "Invalid Data", "status": 400})


@api_view(["GET"])
def getExpense(request, id):
    expense=Expense.objects.filter(id=id).first()
    if expense:
        return Response(
            {
                "id":expense.id,
                "details":expense.details,
                "split_method":expense.split_method,
                "datetime":expense.datetime,
            }
        )
    else:

        return Response({"message": "Invalid Id", "status": 400})



@api_view(["GET"])
def getUserExpenses(request, username):
    try:
        #get the expenses of the user
        user=User.objects.get(user__username=username)
        expenses=Expense.objects.filter(user=user)
        serialized_expenses=[]
        for expense in expenses:
            serialized_expenses.append({
                "id":expense.id,
                "details":expense.details,
                "split_method":expense.split_method,
                "datetime":expense.datetime,
            })
        return Response({'expenses':serialized_expenses})
    except:
        return Response({"message": "Username does not exist", "status": 400})
@api_view(["GET"])
def getOverallExpenses(request):
    try:
        expenses=Expense.objects.all()
        serialized_expenses=[]
        for expense in expenses:
            serialized_expenses.append({
                "id":expense.id,
                "details":expense.details,
                "split_method":expense.split_method,
                "datetime":expense.datetime,
            })
        return Response({'expenses':serialized_expenses})
    except:
        return Response({"message": "Invalid Data",'status':400})
    pass

@api_view(["GET"])
def getBalanceSheet(request,username):
    #calculate the balance sheet for a user
    user=User.objects.get(user__username=username)
    expenses=Expense.objects.filter(user=user)
    your_expenses={}
    count=0
    for expense in expenses:
        mydict=eval(expense.details)
        print(mydict)
        value=mydict[username]
        your_expenses[expense.id]=value
        count+=value
    your_expenses['total-expense']=count

    return Response(your_expenses)


def _getBalanceSheet(username):
    #calculate the balance sheet for a user
    user=User.objects.get(user__username=username)
    expenses=Expense.objects.filter(user=user)
    your_expenses={}
    count=0
    for expense in expenses:
        mydict=eval(expense.details)
        value=mydict[username]
        your_expenses[expense.id]=value
        count+=value
    your_expenses['total-expense']=count

    return your_expenses









@api_view(['GET'])
def downloadBalanceSheet(request, username):
    """
    chat gpt pasted: prompt was, convert dict to pdf and give response of django rest framework"""
    balancesheet=_getBalanceSheet(username)
    print("this is sheet",balancesheet)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    y = height - 40  # Starting Y position
    x = 40  # Starting X position

    # Drawing the content on the PDF
    def draw_dict(p, data, x, y, indent=0):
        for key, value in data.items():
            if isinstance(value, dict):
                p.drawString(x + indent, y, f"{key}:")
                y -= 20
                y = draw_dict(p, value, x, y, indent + 20)
            elif isinstance(value, list):
                p.drawString(x + indent, y, f"{key}:")
                y -= 20
                for item in value:
                    p.drawString(x + indent + 20, y, f"- {item}")
                    y -= 20
            else:
                p.drawString(x + indent, y, f"{key}: {value}")
                y -= 20
        return y

    y = draw_dict(p, balancesheet, x, y)

    # Finalize the PDF page
    p.showPage()
    p.save()

    return response