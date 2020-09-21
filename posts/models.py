from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title=models.CharField(max_length=50, null=False)
    content=models.TextField()
    view_count=models.IntegerField(default=0)#데이터 타입:정수형
    image = models.ImageField(upload_to='images/', null=True)
    created_at=models.DateTimeField(auto_now_add=True)#datetime:날짜+시간/date=날짜
    updated_at=models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)#유저가 없어지면 포스트를 지우기 위해서 케스케이드(on _delete) 넣음
    like_user_set = models.ManyToManyField(User, blank=True, related_name="like_user_set", through="Like")

    @property
    def like_count(self):
        return self.like_user_set.count()

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now = True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE) 
    #on_delete속성은 1:n의 관계에서 user가 없어지면 comment를 어떻게 할 것이냐 설정해주는 것, casade는 댓글도 같이 지울것을 의미
    #realated name을 쓰면 set을 사용할 수 없음

class Like(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=(('user', 'post'))