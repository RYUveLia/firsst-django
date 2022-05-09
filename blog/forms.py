from django import forms

class BoardForm(forms.Form):
    ### 태그 추가 부분 ###
    game = forms.CharField(required = False, label = "게임")