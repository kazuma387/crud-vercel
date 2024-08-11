from django.forms import DateInput, ModelForm
from .models import Representante, Alumno


# creando un modelform le colocamos el mismo nombre del models
class RepresentanteForm(ModelForm):
    class Meta:
        model = Representante
        fields = '__all__'
def clean_cedula(self):
	cedula = self.cleaned_data['cedula']

	if User.objects.filter(cedula=cedula).exists():
		raise forms.ValidationError('Ya existe un representante con esta cédula.')
	return cedula

# creando un modelform le colocamos el mismo nombre del models
class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'
        widgets = {
            'fecha_de_nacimiento': DateInput(attrs={'type' : 'date'}),
        }