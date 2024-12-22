import json
from .forms import KnapsackForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gurobipy import Model, GRB, quicksum

def knapsack_view(request):
    if request.method == 'POST':
        form = KnapsackForm(request.POST)
        if form.is_valid():
            capacity = form.cleaned_data['capacity']
            profits = list(map(int, request.POST.getlist('profits')))
            weights = list(map(int, request.POST.getlist('weights')))
            names = request.POST.getlist('names')
            required_items_input = request.POST.getlist('required_items')

            required_items = [i for i, name in enumerate(names) if str(i) in required_items_input]
            try:
                items_selected, total_profit = solve_knapsack(capacity, profits, weights, names, required_items)
            except ValueError as e:
                request.session['error_message'] = str(e)
                return redirect('knapsack')

            if 'error_message' in request.session:
                del request.session['error_message']

            labels = [item['name'] for item in items_selected]
            data = [item['profit'] for item in items_selected]

            # Calcul de la proportion des poids pour la distribution
            weights_percentage = [item['weight'] for item in items_selected]
            somme_weights = sum(weights_percentage)

            # Calculer la capacité restante
            capacity_restante = capacity - somme_weights

            # Ajouter la capacité restante au tableau weights_percentage
            weights_percentage.append(capacity_restante)
            
            return render(request, 'result.html', {
                'items_selected': items_selected,
                'total_profit': total_profit,
                'capacity': capacity,
                'labels': json.dumps(labels),
                'data': json.dumps(data),
                'weights': json.dumps(weights_percentage)  # Passer les données de poids pour le graphique de distribution
            })

    else:
        form = KnapsackForm()

    error_message = request.session.pop('error_message', None)

    return render(request, 'index.html', {'form': form, 'error_message': error_message})



def solve_knapsack(capacity, profits, weights, names, required_items):
    n = len(profits)
    model = Model()
    model.params.LogToConsole = False

    x = model.addVars(n, vtype=GRB.BINARY, name="x")

    model.setObjective(quicksum(profits[i] * x[i] for i in range(n)), GRB.MAXIMIZE)

    model.addConstr(quicksum(weights[i] * x[i] for i in range(n)) <= capacity)

    total_required_weight = sum(weights[i] for i in required_items)
    if total_required_weight > capacity:
        raise ValueError("The total capacity is exceeded by the mandatory items.")
    for i in required_items:
        model.addConstr(x[i] == 1, f"required_item_{i}")

    model.optimize()

    items_selected = []
    for i in range(n):
        if x[i].X > 0.5:
            item_name = names[i] if names[i] else f"Item {i + 1}"
            items_selected.append({'name': item_name, 'profit': profits[i],'weight': weights[i]})

    total_profit = int(model.ObjVal)
    return items_selected, total_profit



def home_view(request):
    return render(request, 'home.html') 