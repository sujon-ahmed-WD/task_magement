from django.shortcuts import render
 

# Create your views here.
def manager_dashboard(request):
    return render(request,'deshborad/manager_desborard.html')

def user_dashboard(request):
    return render(request,'deshborad/user_deasborad.html')
     

def test(request):
    # names=["Maud","Ahmed","John","tus tus"]
    # count=0
    # for name in names:
    #     count+=1
    # context={
    #     "names":["Maud","Ahmed","John","tus tus"],
    #     "age":22
         
    # }
    context={
        "names":["M","tu","ahm","tabu"],
        "age":22
    }
    return render(request,'test.html',context)
    


  