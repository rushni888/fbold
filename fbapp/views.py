from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.db.models import Q


def fn_index(request):
    if request.method == 'POST':
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        user = request.POST.get('username')
        psw = request.POST.get('password')
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')
        date = year+"-"+month+"-"+day
        gender = request.POST.get('gender')
        check_username_exist = LoginDetail.objects.filter(
            username=user).exists()
        if not check_username_exist:
            loguser_obj = LoginDetail(username=user, password=psw)
            loguser_obj.save()
            if loguser_obj.id > 0:
                user_obj = UserDetail(
                    firstname=firstname, lastname=lastname, birthdate=date, gender=gender, user=loguser_obj)
                    user_obj.save()
                if user_obj.id > 0:
                    # return HttpResponse("Registered sccessfully")
                    return render(request, 'fbapp/home.html')
        return render(request, "fbapp/index.html", {'msg': 'username already taken!', 'day': range(31), 'year': range(1905, 2020)})
    return render(request, "fbapp/index.html", {'day': range(31), 'year': range(1905, 2020)})


def fn_login(request):
    if request.method == 'POST':
        user = request.POST['loguser']
        psw = request.POST['logpass']
        user_exist = LoginDetail.objects.filter(username=user).exists()
        if not user_exist:
            return render(request, "fbapp/index.html", {'day': range(31), 'year': range(1905, 2020), 'incorrect_user': 'Incorrect username'})
        else:
            user_obj = LoginDetail.objects.get(username=user, password=psw)
            if user_obj:
                request.session['userid'] = user_obj.id
                return render(request, 'fbapp/home.html')
            else:
                return render(request, "fbapp/index.html", {'day': range(31), 'year': range(1905, 2020), 'incorrect_password': "Incorrect Password!!"})
    return render(request, "fbapp/index.html", {'day': range(31), 'year': range(1905, 2020)})


def fn_home(request):
    return render(request, 'fbapp/home.html')


def fn_changepassword(request):
    if request.method == "POST":
        current_pswd = request.POST['cur_psw']
        new_pswd = request.POST['new_psw']
        user_id = request.session['userid']
        user_obj = LoginDetail.objects.get(pk=user_id, password=current_pswd)
        if(user_obj):
            user_obj.password = new_pswd
            user_obj.save()
            return render(request, 'fbapp/changepassword.html', {"msg": "Password changed successfully.."})
        else:
            return render(request, 'fbapp/changepassword.html', {"msg": "Cannot reset Password"})

    return render(request, 'fbapp/changepassword.html')


def fn_viewprofile(request):

    if(request.method == "POST"):
        user_id = request.session['userid']
        try:
            firstname = request.POST['firstname']
            lastname = request.POST['surname']
            user_det = UserDetail.objects.get(user=user_id)
            user_det.firstname = firstname
            user_det.lastname = lastname
            user_det.save()
            if request.FILES:
                picture = request.FILES['picupload']
                try:
                    profile_pic_obj = ProfilePic.objects.get(fk_user=user_id)
                    profile_pic_obj.ProfilePic = picture
                    profile_pic_obj.save()
                    return render(request, 'fbapp/viewprofile.html', {"details": user_det, "pic": profile_pic_obj})
                except ProfilePic.DoesNotExist:
                    login_obj = LoginDetail.objects.get(pk=user_id)
                    profile_pic_obj = ProfilePic(ProfilePic=picture, fk_user=login_obj)
                    profile_pic_obj.save()
                    return render(request, 'fbapp/viewprofile.html', {"details": user_det, "pic": profile_pic_obj})
            else:
                profile_pic_obj = ProfilePic.objects.get(fk_user=user_id)
                return render(request, 'fbapp/viewprofile.html', {"details": user_det, "pic": profile_pic_obj})
        except UserDetail.DoesNotExist:
            return render(request, 'fbapp/viewprofile.html', {"error": "No user information table found!"})

    else:
        try:
            user_id = request.session['userid']
            user_det = UserDetail.objects.get(user=user_id)
            user_pic = ProfilePic.objects.get(fk_user=user_id)
            return render(request, 'fbapp/viewprofile.html', {"details": user_det, "pic": user_pic})
        except UserDetail.DoesNotExist:
            return render(request, 'fbapp/viewprofile.html')
        except ProfilePic.DoesNotExist:
            return render(request, 'fbapp/viewprofile.html', {"details": user_det})





def fn_addfriend(request):
    user_id = request.session['userid']   
    senderlist= Friends.objects.filter(reciever_id__id = user_id).values('sender_id') 
    recieverlist=Friends.objects.filter(sender_id__id = user_id).values('reciever_id')    
    # print(recieverlist[0]['reciever_id'])//result-17(reciever-id)
    # totalist=senderlist | recieverlist
    # print(totalist)
    pklist=[]
    for reciever in recieverlist:
        pklist.append(reciever['reciever_id'])
    for sender in senderlist:
        pklist.append(sender['sender_id'])
    print(pklist)
    user_details=UserDetail.objects.exclude(user__id=user_id)
     
    return render(request, "fbapp/add_friends.html",{"userdetails": user_details})

    
    # friendslist= Friends.objects.filter(Q(reciever_id__id = user_id) | Q(sender_id__id =user_id))   
    # user_det=[]
    # print("friends")
    # print(friendslist)   
    # for friends in friendslist:
    #     userNonfriends=UserDetail.objects.exclude(Q(user=friends.reciever_id) | Q(user=friends.sender_id))          
    #     user_det.append(userNonfriends)  

def fn_viewfriend(request):
    rec_id = request.session['userid']
    senderobjects = Friends.objects.filter(reciever_id__id=rec_id)
    request_friends = []
    for user in senderobjects:
        request_friend = UserDetail.objects.get(user=user.sender_id)
        request_friends.append(request_friend)
    return render(request, "fbapp/view_friends.html", {'req_frnds': request_friends})

def fn_cancelrequest(request):
    if request.method == 'POST':
        print("cancel working")
        reciever_obj = LoginDetail.objects.get(id=request.session['userid'])
        sender_obj = LoginDetail.objects.get(id=request.POST['sen_id'])
        requestexist = Friends.objects.filter(sender_id=sender_obj, reciever_id=reciever_obj, status=False)        
        if requestexist:
            requestexist.delete()
            return HttpResponse("Deleted Request")        



def fn_sendrequest(request):
    if request.method == 'POST':
        reci_id=request.POST['rec_id']
        print("send request working")        
        sender_obj = LoginDetail.objects.get(id=request.session['userid'])
        reciver_obj = LoginDetail.objects.get(id=reci_id) 
        print(sender_obj)
        print(reciver_obj)       
        requestexist = Friends.objects.filter(sender_id=sender_obj, reciever_id=reciver_obj, status=False)      
        if requestexist:
            requestexist.delete()
            print("deleted req")
            return HttpResponse("Add Friend",reci_id)
        else:
            friendobj = Friends(sender_id=sender_obj,reciever_id=reciver_obj, status=False)
            friendobj.save()
            print("requested")
            return HttpResponse("Requested",reci_id)
        

def fn_acceptrequest(request):
    if request.method == 'POST':        
        reciever_obj = LoginDetail.objects.get(id=request.session['userid'])
        sender_obj = LoginDetail.objects.get(id=request.POST['sen_id'])
        # print(request.POST['sen_id'])
        requestexist = Friends.objects.filter(sender_id=sender_obj, reciever_id=reciever_obj, status=False).exists()        
        if requestexist:           
            friendobj = Friends(sender_id=sender_obj,reciever_id=reciever_obj, status=True)
            friendobj.save()
            return HttpResponse("Friends",request.POST['sen_id'])

        #  requestexist = Friends.objects.filter(sender_id=sender_obj, reciever_id=reciever_obj, status=False).exists()        
        # if requestexist:           
        #     friendobj = Friends(sender_id=sender_obj,reciever_id=reciever_obj, status=True)
        #     friendobj.save()
        #     return HttpResponse("Friends",request.POST['sen_id'])
        


def fn_data(request):
    data = {
        "name": "rushni",
        "age": 29
    }
    return JsonResponse(data)


def post_data(req):
    print(req.POST['msg'])
    return JsonResponse({'status': True})


def fn_getdata(request):
    return render(request, "fbapp/getdata.html")
