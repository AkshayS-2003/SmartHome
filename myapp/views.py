from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

# Create your views here.
from myapp.models import architect, mobile_user, complai, work_design, work_req, chatss


def login_view(request):
    return render(request, 'login.html')

# @login_required(login_url='/myapp/login_view/')
def home(request):
    return render(request,'index.html')

def logout_view(request):
    request.session.flush()
    return redirect('/myapp/login_view/')

# @login_required(login_url='/myapp/login_view/')
def architect_home(request):
    return render(request,'Architect/Architect_index.html')

# @login_required(login_url='/myapp/login_view/')
def login_post(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # Admin Login
            if user.groups.filter(name='Admin').exists():
                login(request, user)
                messages.success(request, 'Login Successful!')
                return redirect('/myapp/home/')


            elif user.groups.filter(name='Architect').exists():
                ce = architect.objects.get(LOGIN_id=user.id)

                if ce.stat == 'Approved':
                    login(request, user)
                    messages.success(request, 'Login Successful!')
                    return redirect('/myapp/architect_home/')
                else:
                    messages.error(request, 'No architect with this username is approved')
                    return redirect('/myapp/login_view/')

            else:
                messages.error(request, 'You are not authorized')
                return redirect('/myapp/login_view/')

        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('/myapp/login_view/')

    return render(request, 'login.html')

@login_required(login_url='/myapp/login_view/')
def change_pass(request):
    return render(request,'Admin/change_pass.html')

@login_required(login_url='/myapp/login_view/')
def change_post(request):
    current_password=request.POST['current_password']
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']
    if new_password==confirm_password:
        pas=check_password(current_password,request.user.password)
        if pas:
            user=request.user
            user.set_password(new_password)
            user.save()

            messages.success(request,'password_changed')
            return redirect('/myapp/login_view/')
        else:
            messages.success(request, 'please try again')
            return redirect('/myapp/change_pass')
    else:
        messages.success(request, 'Mismatch is confirm paddword and new password')
        return redirect('/myapp/change_pass')

@login_required(login_url='/myapp/login_view/')
def register(request):
    return render(request,'Architect/register.html')

@login_required(login_url='/myapp/login_view/')
def register_post(request):
    username=request.POST['username']
    password=request.POST['password']
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    post_office=request.POST['post_office']
    pin_no=request.POST['pin_no']
    dist=request.POST['dist']
    certificate = request.FILES.get('certificate')
    image = request.FILES.get('image')


    fs=FileSystemStorage()
    path=fs.save(image.name,image)
    path1 = fs.save(certificate.name,certificate)

    user =User.objects.create(username=username,password=make_password(password),first_name=name,email=email)
    center_group, created = Group.objects.get_or_create(name='Architect')
    user.groups.add(center_group)
    user.save()


    re=architect()
    re.name=name
    re.email=email
    re.phone=phone
    re.place=place
    re.post_office=post_office
    re.pin_no=pin_no
    re.dist=dist
    re.stat="Pending"
    re.LOGIN=user
    re.certificate = path1
    re.image=path
    re.save()
    return redirect('/myapp/login_view/')


@login_required(login_url='/myapp/login_view/')
def view_architect(request):
    b=architect.objects.filter(stat='Pending')
    return render(request,'Admin/admin_view_architect.html',{'data':b})

@login_required(login_url='/myapp/login_view/')
def view_mobile_users(request):
    c=mobile_user.objects.all()
    return render(request,'Admin/admin_view_users.html',{'data':c})

@login_required(login_url='/myapp/login_view/')
def approve_architect(request,id):
    ag=architect.objects.filter(id=id).update(stat="Approved")
    return redirect('/myapp/view_architect')

@login_required(login_url='/myapp/login_view/')
def reject_architect(request,id):
    ad=architect.objects.filter(id=id).update(stat="Rejected")
    return redirect('myapp/view_architect')

@login_required(login_url='/myapp/login_view/')
def ad_approved(request):
    vi=architect.objects.filter(stat="Approved")
    return render(request,'Admin/approved_architects.html',{'data':vi})

@login_required(login_url='/myapp/login_view/')
def ad_rejected(request):
    vi=architect.objects.filter(stat="Rejected")
    return render(request,'Admin/rejected_architects.html',{'data':vi})

@login_required(login_url='/myapp/login_view/')
def view_complaints(request):
    a=complai.objects.all()
    return render(request,'Admin/admin_view_complaints.html',{'data':a})

@login_required(login_url='/myapp/login_view/')
def admin_reply(request,id):
    re=complai.objects.get(id=id)
    return render(request,'Admin/admin_reply.html',{'data':re})

@login_required(login_url='/myapp/login_view/')
def admin_reply_post(request):
    reply=request.POST['reply']
    id=request.POST['id']
    re=complai.objects.filter(id=id).update(reply=reply)
    return redirect('/myapp/view_complaints')




@login_required(login_url='/myapp/login_view/')
def view_arch_prof(request):
    d=architect.objects.get(LOGIN = request.user)
    return render(request,'Architect/view_profile.html',{'data':d})

@login_required(login_url='/myapp/login_view/')
def edit_architect(request,id):
    ee = architect.objects.get(id=id)
    return render(request, 'Architect/ed_profile.html', {'data': ee})

@login_required(login_url='/myapp/login_view/')
def ed_architect_post(request,id):
    ee=architect.objects.get(id=id)
    ee.name = request.POST['name']
    ee.email=request.POST['email']
    ee.phone=request.POST['phone']
    ee.place=request.POST['place']
    ee.dist=request.POST['dist']
    if request.FILES.get('image'):
        ee.image = request.FILES['image']
    ee.save()
    return redirect('/myapp/view_arch_prof/')

@login_required(login_url='/myapp/login_view/')
def add_work(request):
    return render(request,'Architect/add_works.html')

@login_required(login_url='/myapp/login_view/')
def add_work_post(request):
    a=architect.objects.get(LOGIN_id = request.user.id)
    details = request.POST['details']
    image = request.FILES.get('image')
    title = request.POST['title']

    fs = FileSystemStorage()
    path = fs.save(image.name, image)

    ad = work_design()
    ad.details = details
    ad.title = title
    ad.image = path
    ad.date = datetime.now()
    ad.ARCHITECT_id = a.id
    ad.save()
    return redirect('/myapp/add_work')

@login_required(login_url='/myapp/login_view/')
def view_add_work(request):
    a=architect.objects.get(LOGIN_id = request.user.id)
    b=work_design.objects.filter(ARCHITECT_id = a)
    return render(request,'Architect/architect_view_work.html',{'data':b})

@login_required(login_url='/myapp/login_view/')
def delete_work(request,id):
    a=work_design.objects.filter(id = id)
    a.delete()
    return redirect('/myapp/view_add_work')

@login_required(login_url='/myapp/login_view/')
def edit_works(request,id):
    ee = work_design.objects.get(id=id)
    return render(request, 'Architect/ed_work.html', {'data': ee})

@login_required(login_url='/myapp/login_view/')
def ed_works_post(request,id):
    ee=work_design.objects.get(id=id)
    ee.title = request.POST['title']
    ee.details=request.POST['details']
    ee.date = datetime.now()
    if request.FILES.get('image'):
        ee.photo = request.FILES['image']
    ee.save()
    return redirect('/myapp/view_add_work/')


@login_required(login_url='/myapp/login_view/')
def view_request(request):
    a=work_req.objects.filter(
        WORK_DESIGN__ARCHITECT__LOGIN = request.user,
        stat = 'Pending')
    return render(request,'Architect/view_request.html',{'data':a})

@login_required(login_url='/myapp/login_view/')
def accept_request(request,id):
    ag=work_req.objects.filter(
        id=id,
        WORK_DESIGN__ARCHITECT__LOGIN = request.user
    ).update(stat="Accepted")
    return redirect('/myapp/view_request')

@login_required(login_url='/myapp/login_view/')
def reject_request(request,id):
    ad=work_req.objects.filter(
        id=id,
    WORK_DESIGN__ARCHITECT__LOGIN = request.user
    ).update(stat="Rejected")
    return redirect('myapp/view_request')

@login_required(login_url='/myapp/login_view/')
def ad_accept(request):
    vi = work_req.objects.filter(
        stat="Accepted",
        WORK_DESIGN__ARCHITECT__LOGIN=request.user
    )
    return render(request, 'Architect/accepted_request.html', {'data': vi})


@login_required(login_url='/myapp/login_view/')
def view_chat(request, id):
    receiver_id = id
    sender_id = request.user.id

    print("LOGGED USER:", request.user.id)
    print("RECEIVER ID:", id)

    messages = chatss.objects.filter(
        Q(fro_id=sender_id, to_id=receiver_id) |
        Q(fro_id=receiver_id, to_id=sender_id)
    ).order_by('id')

    return render(
        request,
        'Architect/chat.html',
        {
            'messages': messages,
            'sender_id': sender_id,
            'receiver_id': receiver_id
        }
    )


@login_required(login_url='/myapp/login_view/')
def send_message(request):
    if request.method == "POST":
        receiver_id = request.POST['receiver_id']
        message = request.POST['mess']

        chatss.objects.create(
            fro_id=request.user.id,
            to_id=receiver_id,
            mess=message,
            date=datetime.now()
        )

    return redirect(f'/myapp/view_chat/{receiver_id}')


@login_required(login_url='/myapp/login_view/')
def fetch_chat(request):
    sender_id = int(request.GET.get("sender_id"))
    receiver_id = int(request.GET.get("receiver_id"))

    msgs = chatss.objects.filter(
        Q(fro_id=sender_id, to_id=receiver_id) |
        Q(fro_id=receiver_id, to_id=sender_id)
    ).order_by("id").values("mess", "fro_id", "to_id")

    return JsonResponse({"messages": list(msgs)})







def register_user(request):
    username = request.POST['username']
    password = request.POST['password']
    name = request.POST['name']
    phone = request.POST['phone']
    email = request.POST['email']
    place = request.POST['place']
    dist = request.POST['dist']
    image = request.FILES['image']

    print(username)
    print(User.objects.filter(username=username))

    if User.objects.filter(username=username).exists():
        print('kkkkkkkkkkkkkkkkk')
        return JsonResponse({'key': 'user already exists'})
    else:
        print('lllllllllllllllllllll')

        fs = FileSystemStorage()
        path1 = fs.save(image.name, image)

        user = User.objects.create(
            username=username,
            password=make_password(password),
            first_name=name,
            email=email
        )

        mobile_group, created = Group.objects.get_or_create(name='Mobile')
        user.groups.add(mobile_group)
        user.save()

        by = mobile_user()
        by.name = name
        by.phone = phone
        by.email = email
        by.dist = dist
        by.place = place
        by.image = path1
        by.LOGIN = user
        by.save()

        return JsonResponse({'key': 'Registration Successful'})



def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.groups.filter(name='Mobile').exists():

                data={
                    'lid':str(user.id)
                }
                return JsonResponse({'key':'Login Successfull','data':data})
            else:
                return JsonResponse({'key':'Not a member of Mobile group'})
        else:
            return JsonResponse({'key':'Invalid username or password'}) 

def view_user_profile(request):
    lid = request.POST.get('lid')
    user = mobile_user.objects.get(LOGIN_id=lid)

    data = {
        'name': user.name,
        'phone': user.phone,
        'email': user.email,
        'dist' : user.dist,
        'place': user.place,
        'image': user.image.url if user.image else "",
    }

    return JsonResponse({'status': 'success', 'data': data})


def get_user_edit(request):
    lid = request.POST['lid']
    try:
        user = mobile_user.objects.get(LOGIN_id=lid)
        return JsonResponse({
            'status': 'success',
            'data': {
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'place': user.place,
                'dist': user.dist,
                'image': user.image.url if user.image else ""
            }
        })
    except:
        return JsonResponse({'status': 'error', 'message': 'Not found'})

def update_user_profile(request):
    lid = request.POST['lid']
    user = mobile_user.objects.get(LOGIN_id=lid)

    user.name = request.POST['name']
    user.email = request.POST['email']
    user.phone = request.POST['phone']
    user.place = request.POST['place']
    user.dist = request.POST['dist']

    if 'image' in request.FILES:
        user.image = request.FILES['image']

    user.save()

    return JsonResponse({'status': 'success'})



def user_view_architect(request):
    lid = request.POST['lid']
    a = mobile_user.objects.get(LOGIN_id=lid)
    requests = work_req.objects.filter(MOBILE=a, stat="Accepted")
    a=[]
    for i in requests:
        arch = i.WORK_DESIGN.ARCHITECT

        a.append({
            'id':arch.id,
            "login_id": arch.LOGIN.id,
            'name':str(arch.name),
            'email':str(arch.email),
            'phone':str(arch.phone),
            'place':str(arch.place),
            'image': arch.image.url if arch.image else ""
        })
    return JsonResponse({'status':'ok','data':a})

def view_architect_design(request):
    lid = request.POST['lid']
    a=mobile_user.objects.get(LOGIN_id = lid)
    b=work_design.objects.all()
    c=[]
    for i in b:
        c.append({
            'id':i.id,
            'title': str(i.title),
            'details':str(i.details),
            'architect_name':i.ARCHITECT.name,
            'architect_phone':i.ARCHITECT.phone,
            'architect_email':i.ARCHITECT.email,
            'image': i.image.url if i.image else ""
        })
    return JsonResponse({'status':'ok','data':c})

def user_send_req(request):
    lid = request.POST['lid']
    did = request.POST['did']
    requ = request.POST['requ']
    image = request.FILES['image']

    fs=FileSystemStorage()
    path=fs.save(image.name,image)

    a=work_req()
    a.date = datetime.now()
    a.MOBILE_id = mobile_user.objects.get(LOGIN_id = lid).id
    a.image=path
    a.requ=requ
    a.WORK_DESIGN_id = work_design.objects.get(id = did).id
    a.save()
    return JsonResponse({'key':'Request Send Successfully'})



def send_complaints(request):
    compla=request.POST['complai']
    lid= request.POST['lid']

    cc=complai()
    cc.date=datetime.now()
    cc.complai=compla
    cc.reply='Pending'
    cc.MOBILE = mobile_user.objects.get(LOGIN_id=lid)
    cc.save()
    return JsonResponse({'key':'Succsss'})

def reply_byst(request):
    lid = request.POST['lid']
    bid = mobile_user.objects.get(LOGIN_id = lid)
    complint = complai.objects.filter(MOBILE_id = bid).values(
        'id',
        'complai',
        'reply',
    )
    return JsonResponse({'key':list(complint)})


from django.http import JsonResponse
from django.db.models import Q

def user_chat(request):
    lid = request.POST['lid']   # mobile LOGIN.id
    aid = request.POST['aid']   # architect LOGIN.id

    messages = chatss.objects.filter(
        Q(fro_id=lid, to_id=aid) |
        Q(fro_id=aid, to_id=lid)
    ).order_by('id').values('mess', 'fro_id', 'to_id')

    return JsonResponse({'key': list(messages)})


def send_user(request):
    lid = request.POST['lid']   # mobile LOGIN.id
    aid = request.POST['aid']   # architect LOGIN.id
    mess = request.POST['mess']

    chatss.objects.create(
        fro_id=lid,
        to_id=aid,
        mess=mess,
        date=datetime.now()
    )

    return JsonResponse({'key': 'Success'})









# import base64
# import torch
# from diffusers import StableDiffusionPipeline
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from io import BytesIO
#
# # Load model once at server startup
# model_id = "prompthero/openjourney"
# pipe = StableDiffusionPipeline.from_pretrained(
#     model_id,
#     torch_dtype=torch.float16
# ).to("cuda")
#
# def generate_interior(prompt):
#     interior_prompt = (
#         f"{prompt}, interior design, ultra realistic, 8k, soft ambient lighting, "
#         f"detailed textures, architectural photography, warm tones"
#     )
#     image = pipe(interior_prompt).images[0]
#
#     # Convert to Base64
#     buffer = BytesIO()
#     image.save(buffer, format="PNG")
#     base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
#
#     return base64_image
#
# @csrf_exempt
# def interior_api(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST only"}, status=400)
#
#     body = json.loads(request.body)
#     prompt = body.get("prompt")
#
#     if not prompt:
#         return JsonResponse({"error": "Prompt missing"}, status=400)
#
#     try:
#         img_b64 = generate_interior(prompt)
#         return JsonResponse({"image_base64": img_b64})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
#
#
#
# from myapp.Geminiapi import generate_gemini_response
#
# def aichatbot(request):
#     user_message = request.POST['message']
#     gemini_response = generate_gemini_response(user_message)
#
#     return JsonResponse({
#         'status': 'success',
#         'response': gemini_response
#     })
