from django.shortcuts import render
from django.views import View
from pirates.models import Tesouro
from django.db.models import F,ExpressionWrapper,DecimalField
from django import forms
from django.http import HttpResponseRedirect
from django.urls.base import reverse

class ListaTesourosView(View):
  def get(self, request):
    lista_tesouros = Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('preco')*F('quantidade'),\
                                                    output_field=DecimalField(max_digits=10,\
                                                    decimal_places=2,\
                                                     blank=True)\
                                                    )\
                            )
    total_geral = 0
    for tesouro in lista_tesouros:
        total_geral+= tesouro.valor_total

    return render(request,
              "lista_tesouros.html",
              {'lista_tesouros': lista_tesouros,
                'total_geral':total_geral})

class TesouroForm(forms.ModelForm):
    class Meta:
        model = Tesouro
        fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
        labels = {"img_tesouro": "Imagem"}

class SalvarTesouro(View):
    def get(self, request, id=None):
      tesouro = Tesouro.objects.get(id=id) if id != None else None
      return render(request,
                          "salvar_tesouro.html",
                          {"tesouroForm":TesouroForm(instance=tesouro)})
    def post(self,request, id=None):
      tesouro = Tesouro.objects.get(id=id) if id != None else None
      form = TesouroForm(request.POST, request.FILES, instance=tesouro)
      if form.is_valid():
        form.save()
        # processa o formulario (usando form.cleaned_data)
        return HttpResponseRedirect(reverse('home') )

      return render(request, "salvar_tesouro.html", {'tesouroForm': form})

class RemoverTesouro(View):
     def get(self, request, id):
        Tesouro.objects.get(id=id).delete()
        return HttpResponseRedirect(reverse('home') )
