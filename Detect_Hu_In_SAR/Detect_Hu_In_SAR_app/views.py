import datetime
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from Detect_Hu_In_SAR_app.models import *


projectemail = "humandetectionyolo@gmail.com"
projectpassword = "fwru sdlu hajh htta"


def log(request):
    return render(request,"index.html")


def logout(request):

    return HttpResponse("<script>alert('Logout Success');window.location='/';</script>")

def log_post(request):
    uname=request.POST['textfield']
    password=request.POST['textfield2']
    data=login.objects.filter(username=uname,password=password)
    if data.exists():
        ldata=data[0]
        request.session['lid']=ldata.id
        request.session['head'] = ""
        if ldata.usertype=='admin':
            return HttpResponse("<script>alert('login Success');window.location='/adminhome';</script>")
        else:
            return HttpResponse("<script>alert('Invalid user');window.location='/';</script>")
    else:
        return HttpResponse("<script>alert('data not found');window.location='/';</script>")

def addrt(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/';</script>")
    request.session['head'] = "ADD RESCUE TEAM"
    return render(request,"admin/add_rescue_team.html")


def generate_password():
    while True:
        import string
        import re
        # Generate a password with at least one uppercase, one lowercase, and one digit
        pwd = random.choice(string.ascii_uppercase)  # Ensure at least one uppercase
        pwd += random.choice(string.ascii_lowercase)  # Ensure at least one lowercase
        pwd += random.choice(string.digits)  # Ensure at least one digit
        pwd += ''.join(random.choices(string.ascii_letters + string.digits, k=5))  # Fill remaining length

        # Shuffle to randomize character positions
        pwd = ''.join(random.sample(pwd, len(pwd)))

        # Validate password pattern
        if re.fullmatch(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}", pwd):
            return pwd


def addrt_post(request):
    uname=request.POST['textfield']
    email=request.POST['textfield2']
    phone=request.POST['textfield3']
    role=request.POST['textfield4']
    data=login.objects.filter(username=email)
    if data.exists():
        return HttpResponse("<script>alert('Email already exists');window.location='/addrt#services';</script>")
    else:
        # pwd = generate_password()
        pwd = random.randint(0000,9999)

        l=login()
        l.username=email
        l.password= pwd
        l.usertype='rescue'
        l.save()

        obj=rescue_team()
        obj.username=uname
        obj.email=email
        obj.phone=phone
        obj.specialization=role
        obj.LOGIN=l
        obj.save()

        import smtplib
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("humandetectionyolo@gmail.com", "fwru sdlu hajh htta")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "humandetectionyolo@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for Human detection"
        body = "Your Password is:- - " + str(pwd)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)

        return HttpResponse("<script>alert('Rescue team added');window.location='/viewrt#services';</script>")

def edit(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/';</script>")
    request.session['head'] = "EDIT RESCUE TEAM"
    res=rescue_team.objects.get(id=id)
    return render(request,"admin/edit.html",{"data":res})

def edit_post(request,id):
    uname = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    role = request.POST['textfield4']
    rescue_team.objects.filter(id=id).update(username=uname,email=email,phone=phone,specialization=role)
    return HttpResponse("<script>alert('Rescue team edited');window.location='/viewrt#services';</script>")

def changep(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/';</script>")
    request.session['head'] = "CHANGE PASSWORD"
    return render(request,"admin/change_password.html")

def changep_post(request):
    oldpas = request.POST['textfield']
    newpas = request.POST['textfield2']
    confirmpas = request.POST['textfield3']
    if newpas==confirmpas:

        data=login.objects.filter(password=oldpas,id=request.session['lid'])
        if data.exists():
            login.objects.filter(id=request.session['lid']).update(password=newpas)
            return HttpResponse("<script>alert('password changed');window.location='/';</script>")
        else:
            return HttpResponse("<script>alert('no such data found');window.location='/changep#services';</script>")

    else:
        return HttpResponse("<script>alert('password mismatched');window.location='/changep#services';</script>")


def viewf(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/';</script>")
    request.session['head'] = "VIEW FEEDBACK"
    view=feedback.objects.all()
    return render(request,"admin/view_feedback.html",{"data":view})


def viewrt(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/';</script>")
    request.session['head'] = "VIEW RESCUE TEAM"
    view=rescue_team.objects.all()
    return render(request,"admin/view_r_t.html",{"data":view})

def deletert(request,id):
    rescue_team.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Rescue team deleted');window.location='/viewrt';</script>")

def viewst(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/';</script>")
    res=work_allocation.objects.filter(RESCUET_id=id)
    request.session['head'] = "VIEW STATUS"
    return render(request,"admin/view_status.html",{'data':res})


def workall(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/';</script>")
    request.session['head'] = "ALLOCATE WORK"
    request.session['rid'] = id
    return render(request,"admin/work_allocation.html",{'id':id})

def workall_post(request,id):
    work=request.POST['textfield']
    details=request.POST['textfield2']
    longitude=request.POST['textfield3']
    latitude=request.POST['textfield4']
    place=request.POST['textfield5']
    post=request.POST['textfield6']
    pincode=request.POST['textfield7']
    rid = request.session['rid']
    data = work_allocation.objects.filter(RESCUET_id=id,work=work)
    if data.exists():
        return HttpResponse("<script>alert('Already allocated');window.location='/viewst/"+rid+"''</script>")
    else:

        obj=work_allocation()
        obj.RESCUET_id=id
        obj.work=work
        obj.details=details
        obj.longitude=longitude
        obj.latitude=latitude
        obj.place=place
        obj.post=post
        obj.pin=pincode
        obj.date=datetime.datetime.now().date()
        obj.status='pending'
        obj.amount='pending'
        obj.save()
        rid=request.session['rid']
        return HttpResponse("<script>alert('Work allocated');window.location='/viewst/"+rid+"';</script>")


def adminhome(request):
    return render(request,"admin/index.html")

#         rescue team



def login_res(request):
    un=request.POST['username']
    pw=request.POST['password']
    data = login.objects.filter(username=un, password=pw)
    if data.exists():
        lid = data[0].id
        type = data[0].usertype
        return JsonResponse({"status":"ok","lid":lid,"type":type})
    else:
        return JsonResponse({"status":None})

def view_work_allocation(request):
    # longitude = request.POST['longitude']
    # latiitude = request.POST['latitude']

    lid=request.POST['lid']
    data = work_allocation.objects.filter(RESCUET__LOGIN=lid)
    ar = []
    for i in data:
        ar.append(
            {
                "wid":i.id,"date":i.date,"work":i.work,"details":i.details,"place":i.place,"pin":i.pin,"post":i.post,"longitude":i.longitude,"latitude":i.latitude,"status":i.status
            }
        )

    return JsonResponse({"status": "ok","data":ar})

def view_detection(request):
    data = detection.objects.all()
    ar = []
    for i in data:
        ar.append(
            {
                "date":i.date,"image":i.image
            }
        )
    return JsonResponse({"status": "ok","data":ar})

def send_feedback(request):
    feed=request.POST['feedback']
    lid=request.POST['lid']

    obj = feedback()
    obj.date=datetime.datetime.now().date()
    obj.feedback=feed
    obj.RESCUET=rescue_team.objects.get(LOGIN=lid)
    obj.save()
    return JsonResponse({"status": "ok"})

def change_password(request):
    op=request.POST['oldpassword']
    np=request.POST['newpassword']
    cp=request.POST['confirmpassword']
    lid=request.POST['lid']
    data = login.objects.filter(password=op)
    if data.exists():
        if np==cp:


            login.objects.filter(id=lid).update(password=np)
            return JsonResponse({"status":"ok"})
        else:
            return JsonResponse({"status":"no"})

    else:
        return JsonResponse({"status":None})


def update_status(request):
    wid = request.POST['wid']
    am=request.POST['amount']
    work_allocation.objects.filter(id=wid).update(status="Completed",amount=am)
    return JsonResponse({"status": "ok"})

def payment_method(request,id,am):
    return render(request,"admin/payment_method.html",{'id':id,"amount":am})


def payment_submit(request,id,am):
    type = request.POST['radio']

    print("idddddddddddddddd",id)

    if type =="Offline":

        obj=payment()
        obj.WORK_ALLOCATION_id=id
        obj.amount=am
        obj.payment_status="offline"
        obj.payment_date = datetime.datetime.now()
        obj.save()

        work_allocation.objects.filter(id=id).update(status='paid')

        return HttpResponse("<script>alert('Payment offline success');window.location='/viewrt';</script>")



    else:

        return HttpResponse("<script>alert(' Online Payment ');window.location='/default/"+id+"'</script>")


def default(request,id):
    import razorpay
    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    amount1= work_allocation.objects.filter(RESCUET=id)
    amount2=amount1[0].amount

    print(amount2,"amountttttttt")
    amount = int(amount2)*100

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }
    return render(request, 'admin/payment.html', {'razorpay_api_key': razorpay_api_key,
                                            'amount': order_data['amount'],
                                            'currency': order_data['currency'],
                                            'order_id': order['id'],"id":id})






def online(request,id,amount):

    obj=payment()
    obj.amount=amount
    obj.WORK_ALLOCATION_id=id
    obj.payment_status="online"
    obj.payment_date = datetime.datetime.now()
    obj.save()
    rid = request.session['rid']
    work_allocation.objects.filter(id=id).update(status='paid')

    return HttpResponse("<script>alert('Payment online success');window.location='/viewst/"+rid+"';</script>")





def forgot_password(request):
    return render(request,'forgot password.html')

def forgot_passwordbuttonclick(request):
    mail = request.POST['email']
    request.session['otp'] = str(random.randint(1000,9999))
    request.session['mail'] = mail

    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(projectemail, projectpassword)
    msg = MIMEMultipart()  # create a message.........."
    msg['From'] = projectemail
    msg['To'] = mail
    msg['Subject'] = 'otp'
    body = str(request.session['otp'])
    msg.attach(MIMEText(body,'plain'))
    s.send_message(msg)
    return HttpResponse("<script>alert('otp sended successfully');window.location='/otp'</script>")


def otp(request):
    return render(request,"otp.html")

def otpbuttonclick(request):
    OTP = request.POST['otp']

    new_password = login.objects.get(username = request.session['mail']).password

    if OTP == request.session['otp']:
       try:
           import smtplib
           s = smtplib.SMTP(host='smtp.gmail.com', port=587)
           s.starttls()
           s.login(projectemail, projectpassword)
           msg = MIMEMultipart()  # create a message.........."
           msg['From'] = projectemail
           msg['To'] = request.session['mail']
           msg['Subject'] = 'your password changed'
           body = new_password
           msg.attach(MIMEText(body, 'plain'))
           s.send_message(msg)
       except:
           pass

       return HttpResponse("<script>alert('Check your mail');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('invalid');window.location='/'</script>")






# --------------------------------- MAIN ----------------------------------


import os
import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from newcam import process_uploaded_video
from .models import upload_video  # Ensure this import is correct

STATIC_PATH = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static"

def upload_gallery(request):
    """Render the video upload page."""
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/';</script>")

    request.session['head'] = "UPLOAD VIDEO"
    return render(request, "upload_videos.html")


def upload_gallery_post(request):
    """Handle video upload and process it."""
    if request.method == 'POST' and request.FILES.get('fileField'):
        video_file = request.FILES['fileField']
        fs = FileSystemStorage(location=os.path.join(STATIC_PATH, "videos"))  # Store in static/videos
        dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = fs.save(f"{dt}.mp4", video_file)

        print("filename:", filename)

        # ✅ Store only the relative path
        video_path = os.path.join("videos", filename)

        print("video_path:", video_path)
        frame_count = 0

        frame_image_filename = f"a_{frame_count}.jpg"

        print("frame_image_filename",frame_image_filename)

        # ✅ Process the uploaded video for human detection
        process_uploaded_video(os.path.join(STATIC_PATH, video_path))

        # ✅ Save record to database
        obj = upload_video(video=frame_image_filename, date=datetime.datetime.now().date())
        obj.save()

        return HttpResponse("<script>alert('Video Uploaded and Processed');window.location='/'</script>")




# ---- real time


import datetime
import cv2
import os
from DBConnection import Db
from django.http import HttpResponse
from django.shortcuts import render
from newcam import play_alert_sound
from newcam import detect_humans

# Static path where images are stored
staticpath = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static"

# Paths for YOLO model files
yolo_cfg = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static\yolo_files\yolo.cfg"
yolo_weights = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static\yolo_files\yolo.weights"
coco_names = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static\yolo_files\coco.names"

# Load YOLO model
net = cv2.dnn.readNet(yolo_weights, yolo_cfg)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Load COCO labels
with open(coco_names, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Initialize database
db = Db()

# Define path for detection images
detection_folder = os.path.join(staticpath, "detections")
os.makedirs(detection_folder, exist_ok=True)  # Ensure the directory exists


def real_detection(request):
    """Trigger human detection and capture an image when human is detected."""

    # Open the camera
    cam = cv2.VideoCapture(0)  # 0 for default camera

    # Get current timestamp
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            return HttpResponse(
                "<script>alert('Error: Unable to access camera.'); window.location.href = '/';</script>")

        # Detect humans in the frame
        human_detected, frame_with_detections = detect_humans(frame)

        if human_detected:
            # Capture the frame and save it
            image_name = f"detection_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            image_path = os.path.join(detection_folder, image_name)
            cv2.imwrite(image_path, frame_with_detections)

            # Insert detection event into database
            query = "INSERT INTO Detect_Hu_In_SAR_app_detection (date, image) VALUES (%s, %s)"
            params = (date, f"/static/detections/{image_name}")  # Save relative path in DB
            db.insert(query, params)

            # Play alert sound
            play_alert_sound()

            # Stop the camera feed after capturing the detection image
            cam.release()
            cv2.destroyAllWindows()

            # Send response with JavaScript to play sound in browser
            sound_path = "/static/attack2t22wav-14511.mp3"  # Ensure correct static path
            response_script = f"""
            <script>
                alert('Human Detected!');
                var audio = new Audio('{sound_path}');
                audio.play();
                window.location.href = '/';
            </script>
            """
            return HttpResponse(response_script)

        # Display the frame in a window (for testing purposes)
        cv2.imshow("Real-Time Human Detection", frame_with_detections)

        # Exit condition to stop camera feed (press 'q')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera
    cam.release()
    cv2.destroyAllWindows()

    return HttpResponse("<script>alert('No human detected.'); window.location.href = '/';</script>")







# realtime 2

# import datetime
# import cv2
# import os
# import threading
# from DBConnection import Db
# from django.http import HttpResponse
# from django.shortcuts import render
# from newcam import play_alert_sound
# from newcam import detect_humans
#
# # Static path where images are stored
# staticpath = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static"
#
# # Paths for YOLO model files
# yolo_cfg = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static\yolo_files\yolo.cfg"
# yolo_weights = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static\yolo_files\yolo.weights"
# coco_names = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static\yolo_files\coco.names"
#
# # Load YOLO model
# net = cv2.dnn.readNet(yolo_weights, yolo_cfg)
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
#
# # Load COCO labels
# with open(coco_names, "r") as f:
#     classes = [line.strip() for line in f.readlines()]
#
# # Initialize database
# db = Db()
#
# # Define path for detection images
# detection_folder = os.path.join(staticpath, "detections")
# os.makedirs(detection_folder, exist_ok=True)  # Ensure the directory exists
#
#
# # Function to display frames in the background
# def display_frame(cam):
#     while True:
#         ret, frame = cam.read()
#         if not ret:
#             break
#         cv2.imshow("Real-Time Human Detection", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cv2.destroyAllWindows()
#
#
# def real_detection(request):
#     """Trigger human detection and capture an image when human is detected."""
#
#     # Open the camera
#     cam = cv2.VideoCapture(0)  # 0 for default camera
#
#     # Start a separate thread for displaying the frame
#     frame_thread = threading.Thread(target=display_frame, args=(cam,))
#     frame_thread.daemon = True
#     frame_thread.start()
#
#     # Get current timestamp
#     date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#     while cam.isOpened():
#         ret, frame = cam.read()
#         if not ret:
#             return HttpResponse(
#                 "<script>alert('Error: Unable to access camera.'); window.location.href = '/';</script>")
#
#         # Detect humans in the frame
#         human_detected, frame_with_detections = detect_humans(frame)
#
#         if human_detected:
#             # Capture the frame and save it
#             image_name = f"detection_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
#             image_path = os.path.join(detection_folder, image_name)
#             cv2.imwrite(image_path, frame_with_detections)
#
#             # Insert detection event into database
#             query = "INSERT INTO Detect_Hu_In_SAR_app_detection (date, image) VALUES (%s, %s)"
#             params = (date, f"/static/detections/{image_name}")  # Save relative path in DB
#             db.insert(query, params)
#
#             # Play alert sound
#             play_alert_sound()
#
#             # Stop the camera feed after capturing the detection image
#             cam.release()
#             cv2.destroyAllWindows()
#
#             # Send response with JavaScript to play sound in browser
#             sound_path = "/static/attack2t22wav-14511.mp3"  # Ensure correct static path
#             response_script = f"""
#             <script>
#                 alert('Human Detected!');
#                 var audio = new Audio('{sound_path}');
#                 audio.play();
#                 window.location.href = '/';
#             </script>
#             """
#             return HttpResponse(response_script)
#
#     # Release the camera
#     cam.release()
#     cv2.destroyAllWindows()
#
#     return HttpResponse("<script>alert('No human detected.'); window.location.href = '/';</script>")


import datetime
import cv2
import os
from DBConnection import Db
from django.http import HttpResponse
from newcam import play_alert_sound, process_uploaded_video, detect_humans

# Define paths
STATIC_PATH = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static"
VIDEO_PATH = os.path.join(STATIC_PATH, "3545736297-preview.mp4")  # This file is only used for processing

def detect_human(request):
    """Trigger human detection, play an alert sound, capture an image, and log detection in the database."""

    # Play alert sound
    play_alert_sound()

    # Get current timestamp
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Open video file
    cam = cv2.VideoCapture(VIDEO_PATH)
    ret, frame = cam.read()

    if ret:
        # Detect humans in the frame
        human_detected, frame_with_detections = detect_humans(frame)

        if human_detected:
            # Save detected frame
            image_name = f"detection_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            image_path = os.path.join(STATIC_PATH, "detections", image_name)
            cv2.imwrite(image_path, frame_with_detections)
            cam.release()

            print("Image Name:", image_name)
            print("Image Path:", image_path)

            # Insert detection event into database
            db = Db()
            query = "INSERT INTO Detect_Hu_In_SAR_app_detection (date, image) VALUES (%s, %s)"
            params = (date, f"/static/detections/{image_name}")  # Save only detected image path
            db.insert(query, params)

            # Send response with JavaScript to play sound in browser
            sound_path = "/static/attack2t22wav-14511.mp3"
            response_script = f"""
            <script>
                alert('Human Detected!');
                var audio = new Audio('{sound_path}');
                audio.play();
                window.location.href = '/';
            </script>
            """
            return HttpResponse(response_script)

    # If no human detected or error reading video
    return HttpResponse("<script>alert('No human detected or unable to access video.'); window.location.href = '/';</script>")
