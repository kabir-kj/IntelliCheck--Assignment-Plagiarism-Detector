from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views 

urlpatterns  = [path ('', views.index, name = "index"),
                path('Login_Teacher/', views.Lteacher, name = "Lteacher"),
                path('Login_Student/', views.LStudent, name="LStudent"),
                path('Signup_Student/', views.SStudent, name = "SStudent"),
                path('Signup_Teacher/', views.STeacher, name = "STeacher"),
                path('Student_Assinment/', views.SDashboard, name = "SDashboard"),
                path('Teacher_Dashboard/', views.TDashboard,name  = "TDashboard"),
                path('logout/', views.Slogout, name='logout'),
                path('Teacher_logout/', views.Tlogout, name='Tlogout'),
                path('Sucess/',views.Sassingment, name = "Sassingment"),
                path('verifykey/', views.keyverify,name = "keyverify"),
                path('Submitassigments/', views.Subassignments, name = "Subassignments"),
                path('showassigments/', views.Show_Student_assingment, name = "Show_Student_assingment"),
                path('showassigmentst/', views.show_assignment_teacher, name = "show_assignment_teacher"),
                path('view_submissions/<int:assingment_key>/', views.view_submissions, name='view_submissions'),
                ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    