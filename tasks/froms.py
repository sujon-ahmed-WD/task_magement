from django import forms
from tasks.models import Task ,TaskDetail
# Django from
class TaskForm(forms.Form):
    title=forms.CharField(max_length=250,label="Task Title")
    decripation=forms.CharField(
        widget=forms.Textarea,label='Task Description'
    )
    due_date=forms.DateField(widget=forms.SelectDateWidget)
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    
    def __init__(self,*args,**kwargs):
        # print(args,kwargs)
        employees=kwargs.pop("employees",[])
        super().__init__(*args,**kwargs)
        
        self.fields['assigned_to'].choices = [
            (emp.id, emp.username) for emp in employees 
        ]


class StyledFormMixin:
    """ Mixinge to apply style to from field"""
    def __init__(self,*arg,**kwargs):
        super().__init__(*arg,**kwargs)
        self.apply_styled_widgets()
    
    default_classes="border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter{field.label.lower()}"
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                # print("InSide Date")
                field.widget.attrs.update({
                    "class":"border-2 border-gray-300  p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                
                field.widget.attrs.update({
                    'class':"space-y-2"
                })
            else:
               
                field.widget.attrs.update({
                    'class':self.default_classes
                })
    
    
# Django Model From
class TaskModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description','due_date','assigned_to']
        widgets={
            'due_date':forms.SelectDateWidget,
            'assigned_to':forms.CheckboxSelectMultiple
        }
       
        
    """ Widget Using in Mixing  """
    def __init__(self,*arg,**kwargs):
        super().__init__(*arg,**kwargs)
        self.apply_styled_widgets()

class TaskDetailModelForm(forms.ModelForm):
    class Meta:
        model=TaskDetail
        fields=['priority','notes','asset']