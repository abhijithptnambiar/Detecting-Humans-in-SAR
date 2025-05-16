from django.db import models

# Create your models here.
class login(models.Model):
    username=models.CharField(max_length=200)
    usertype=models.CharField(max_length=200)
    password=models.CharField(max_length=200)

class rescue_team(models.Model):
    LOGIN=models.ForeignKey(login,on_delete=models.CASCADE)
    username= models.CharField(max_length=200)
    email= models.CharField(max_length=200)
    phone= models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)

class work_allocation(models.Model):
    RESCUET=models.ForeignKey(rescue_team,on_delete=models.CASCADE)
    work= models.CharField(max_length=200)
    details= models.CharField(max_length=200)
    status= models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    pin = models.CharField(max_length=200)
    post = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)

class feedback(models.Model):
    RESCUET=models.ForeignKey(rescue_team,on_delete=models.CASCADE)
    date= models.CharField(max_length=200)
    feedback= models.CharField(max_length=200)

class detection(models.Model):
    date=models.CharField(max_length=200)
    image= models.CharField(max_length=200)



class payment(models.Model):
    payment_status=models.CharField(max_length=200)
    amount=models.CharField(max_length=200)

    payment_date=models.CharField(max_length=200)
    # RESCUET=models.ForeignKey(rescue_team,on_delete=models.CASCADE)
    WORK_ALLOCATION=models.ForeignKey(work_allocation,on_delete=models.CASCADE)



class camera(models.Model):
    camera_number = models.CharField(max_length=20)
    RESCUET = models.ForeignKey(rescue_team, on_delete=models.CASCADE)


class upload_video(models.Model):
    video = models.CharField(max_length=20)
    date = models.CharField(max_length=20)