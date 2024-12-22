from django import forms

class KnapsackForm(forms.Form):
    capacity = forms.IntegerField(
        label="Knapsack Capacity",
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter capacity'}),
    )
