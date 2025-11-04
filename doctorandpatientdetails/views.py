from .models import Patient,Student,Teachar, Hobby, Hospital , AdmittePatientDetails
from .serializers import DoctorSerializer, StudentSerializer, TeacherSerializer, HobbySerializer, HospitalSerializer, AdmittePatientDetailsSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class StudentCreateListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]


class StudentRetriveUpdateeDestoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]


class TeacherCrateListView(generics.ListCreateAPIView):
    queryset = Teachar.objects.all()
    serializer_class = TeacherSerializer

class TeacherRetriveupdatedestoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teachar.objects.all()
    serializer_class = TeacherSerializer


class HobbyCraeteListView(generics.ListCreateAPIView):
    queryset = Hobby.objects.all()
    serializer_class = HobbySerializer


class HobbyRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hobby.objects.all()
    serializer_class = HobbySerializer

from django.db.models import Q

class CreatelistView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):

        queryset = Student.objects.all()
        params = request.query_params

        dd = Student.objects.filter(name__in = ['surendrans','sur'])

        for i in dd:
            print(i.id,i.name,i.age , i.teachar.name)

        df = Student.objects.select_related('teachar')
        for i in df:
            print(i.name, i.teachar.name , i.teachar.age)

        dm = Student.objects.prefetch_related('habbice')

        for i in dm:
            habbice_name = [h.name for h in i.habbice.all()]
            print("first",i.name,habbice_name)

        allt = Student.objects.all()
        for i in allt:
            habbice_name = [h.name for h in i.habbice.all()]
            print("secount",i.name,habbice_name)

        dmf = Student.objects.prefetch_related('habbice').filter(habbice__name__iexact = 'car drive').values('name','habbice__name')
        print("dmf",dmf)
        for i in dmf:
            habbice_name = [h.name for h in i.habbice.all()]
            print("val",i.name,habbice_name)

        filter_map ={
            "age_gt":"age__gte",
            "age_lt":"age__lte",
            "teachar":"teachar__name__icontains",
            "habbice":"habbice__name__icontains",
            "name":"name__iexact",
        }

        filter_kwargs = {}
        print(filter_map.items())
        for param, lookup in filter_map.items():

            print("ch",param,lookup)
            value = params.get(param)
            print("vch",value)
            if value is not None and str(value).strip().lower() not in ("", "none", "null"):
                filter_kwargs[lookup] = value
                print("dch",filter_kwargs)

        print("aftersr",filter_kwargs)
        che = queryset.filter(**filter_kwargs)
        print(che)
        queryset = queryset.filter(**filter_kwargs)


        # name_search = request.query_params.get("name")
        # age_gt = request.query_params.get("age_gt")
        # age_lt = request.query_params.get("age_lt")
        # age_gte = request.query_params.get("age_gte")
        # age_lte = request.query_params.get("age_lte")
        # age_search = request.query_params.get("age")
        # teacher_search = request.query_params.get("teacher")
        # hobby_search = request.query_params.get("hobby")


        # queryset = Student.objects.all()

        # if name_search:
        #     queryset = queryset.filter(name__icontains=name_search)

        # if age_search:
        #     queryset = queryset.filter(age=age_search)

        # if age_gt:
        #     queryset = queryset.filter(age__gt=age_gt)

        # if age_lt:
        #     queryset = queryset.filter(age__lt=age_lt)

        # if age_gte:
        #     queryset = queryset.filter(age__gte=age_gte)

        # if age_lte:
        #     queryset = queryset.filter(age__lte=age_lte)

        # if teacher_search:
        #     queryset = queryset.filter(teachar__name__icontains=teacher_search)

        # if hobby_search:
        #     queryset = queryset.filter(habbice__name__icontains=hobby_search)
        
        serializer = StudentSerializer(queryset, many=True)

        res = []
        for data in serializer.data:
            res.append({
                "student_name": data["name"],
                "student_age": data["age"],
                "teacher_name": data["teachar"]["name"],
                "habbice_name": [h["name"] for h in data.get("habbice", [])]
            })

        return Response(res, status=status.HTTP_200_OK)


    def post(self, request):

        teacher_id = request.data.get("teachar")
        habbice_ids = request.data.get("habbice", [])
        name = request.data.get("name")
        age = request.data.get("age")

        if not name:
            return Response({"error":"name field is required"})
        habbice_i = Hobby.objects.values_list('id', flat=True)
        # [1,2,3,4]

        invalid = []
        for hid in habbice_ids: #[1,2]
            if hid not in habbice_i:
                invalid.append(hid)

        if invalid:
            return Response(
                {"error": f"Hobby IDs {invalid} do not exist. Please create them first."},
                status=400
            )

        student = Student.objects.create(
            name=name,
            age=age,
            teachar_id=teacher_id
        )

        if habbice_ids:
            student.habbice.set(habbice_ids)

        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Studentupdate(APIView):
    def get(self, request, pk):
        queryset = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = get_object_or_404(Student, pk=pk)
        print(queryset)
        serializer = StudentSerializer(queryset, data=request.data, partial=True )
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = get_object_or_404(Student, pk=pk)
        queryset.delete()
        return Response({"message":"delete Successfully"})


class AdmittePatientDetailsView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        queryset = AdmittePatientDetails.objects.all()

        # Manger Custom
        gtall = AdmittePatientDetails.active.all().values_list("patient__name", flat=True)
        print("get all data for custom manager",gtall)

        gtfilter = AdmittePatientDetails.active.filter(patient__name__iexact = 'surendran').values('patient__name', 'hospital__name')
        # for i in gtfilter:
        #     print(list(i))
        print("get filter used to data ", gtfilter)

        gget = AdmittePatientDetails.active.get(id=1)
        print("get for method used",gget)

        filterobject = AdmittePatientDetails.objects.filter(is_activate = False)
        print("get for filter object userd",filterobject)

        getobjectuse = AdmittePatientDetails.objects.get(id=1)
        print("get for object id=1 ",getobjectuse)

        # Quary and manager Custom
        qtfilter = AdmittePatientDetails.active_custom.inactivate()
        print("qtfilter",qtfilter)

        ch = AdmittePatientDetails.patientage_custom.child()
        print("child age patient",ch)

        boy = AdmittePatientDetails.patientage_custom.boys()
        print("boys age patients", boy)

        mens = AdmittePatientDetails.patientage_custom.mens()
        print("mens age patient", mens)

        serializer = AdmittePatientDetailsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
