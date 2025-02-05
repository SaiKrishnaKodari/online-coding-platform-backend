from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import problem,test_case
from django.core import serializers
import json
import requests
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

CODE_EVALUATION_URL = u'https://api.hackerearth.com/v4/partner/code-evaluation/submissions/'
CLIENT_SECRET = '8331c729bada537c508c7036dbdad95118694c64'
CLIENT_ID ='d3983383345f7eaab23be3d801dede79f6f9900b3eed.api.hackerearth.com'


def questions(request):
    problems =problem.objects.all()
    data = serializers.serialize('json', problems)
    return HttpResponse(data,content_type="application/json")
# def code(request,title,id):
#     question = problem.objects.get(id =id)
#     question =[question]
#     data = serializers.serialize('json',question)
#     return HttpResponse(data,content_type="application/json")
def code(request,title,id):
    question = problem.objects.get(id =id)
    testcases = list(test_case.objects.filter(problem = question,isPublic=True))
    question =[question]+testcases
    print("hello")
    data = serializers.serialize('json',question)
    
    return HttpResponse(data,content_type="application/json")

@csrf_exempt
def compile(request,code="",language="PYTHON3",input=""):
    print("In compile ------------------------------------>>>>>>>>>>>>>>>>>>>>>")
    if request.method=="POST":
        data_from_post = json.load(request)['post_data']
        #print(data_from_post)
        code=data_from_post.get('code',"")
        user_input=data_from_post.get('input',"")
        language=data_from_post.get('language',"")
        print("user input",user_input)
        print("code ",code)
        print("language",language)

        COMPILE_URL = 'https://api.hackerearth.com/v3/code/compile/'
        RUN_URL = 'https://api.hackerearth.com/v3/code/run/'
        # CLIENT_SECRET="7b9e5877ccb804b9ae5e690c33e47fcfc72d31ec"
        source="for i in range(5):\n    print(5)"
        data = {
            'client_secret': CLIENT_SECRET,
            'async': 0,
            'source': code,
            'lang': language,
            'time_limit': 5,
            'memory_limit': 262144,
            'input':user_input
        }
 
        r = requests.post(RUN_URL, data=data)
        # print(r.json(),type(r.json()))
        print(r)
        resp=r.json()
        return JsonResponse(resp)

@csrf_exempt
def submit_code(request):
    # question
    if request.method=="POST":
        data_from_post = json.load(request)['post_data']
        print(data_from_post)
        code=data_from_post["code"]
        language= data_from_post["language"]
        question_pk=data_from_post["question_pk"]
    
    question =problem.objects.get(pk = question_pk)
    # print(question)
    private_testcases = list( test_case.objects.filter(problem=question,isPublic= False) )
    print(private_testcases)


    COMPILE_URL = 'https://api.hackerearth.com/v3/code/compile/'
    RUN_URL = 'https://api.hackerearth.com/v3/code/run/'
    # CLIENT_SECRET="7b9e5877ccb804b9ae5e690c33e47fcfc72d31ec"
    data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': code,
        'lang': language,
        'time_limit': 5,
        'memory_limit': 262144,
        'input':""
    }
 
    final_response=[]
    for tc in private_testcases:
        data["input"] = tc.__dict__["input"]
        r = requests.post(RUN_URL, data=data)
        resp=r.json()
        run_status = resp.get("run_status",None),
        print('wwwwwwww',run_status)
        if run_status!=None:
            # print(run_status)
            output = run_status[0].get("output","ERROR")

            print(output.strip() == tc.__dict__["output"].strip())
            if output.strip() == tc.__dict__["output"].strip():
                final_response.append(
                    {
                        "status":"Passed"
                    }
                )

            else:
                final_response.append(
                    {
                        "status":"Failed"
                    }
                )

            
        else:
            final_response.append(
                    {
                        "status":"Error"
                    }
                )
        print()
        print()
        print()
    return JsonResponse(final_response,safe=False)        