import numpy as np

def input(request):
	return render(request, 'search_form.html')

def output(request):
	if 'q' in request.GET:
		isbn_input= request.GET['q']
		existing= Book.objects.filter(ISBN=isbn_input)
		
		if existing:
			rec= existing.recommendation
			last_update= existing.today
			return render(request, 'results.html', {'queried_before'=True, 
		else:
			model_inputs=NetezzaData.read_netezza(isbn_input)
		
			if model_inputs:
				elasticity= NetezzaData.predict_elasticity(model_inputs)
				try:
					neighbor_price = GraphData.Neighbor_price_fetch(isbn_input)
					self_price = GraphData.Price_fetch(isbn_input)
				except:
					return render("Neo4j is having trouble with this query.")
					
				model_recommends=NetezzaData.make_recommendation(elasticity)
				copurchase_data_recommends=GraphData.make_recommendation(self_price, neighbor_price)
				
				today=datetime.today().strftime('$Y-%m-%d')
				NetezzaData.save(ISBN=isbn_input, day_of_update=today, onsale_date=model_inputs[0], subject=model_inputs[1], category=model_inputs[2], pre_sales=model_inputs[3], price=model_inputs[3], maximum_amazon_rank= model_inputs[5], recommendation=model_recommends, elasticity=elasticity, recommendation=model_recommends)
			
				GraphData.save(ISBN=isbn_input, Price= self.price, Neighbor_price= neighbor_price, recommendation=copurchase_info_recommends)
				
				return render("results.html', {'neo4j_recommends'= copurchase_data_recommends, "netezza_recommends'= model_recommends} 
			
			else:
				return render("I'm sorry. I can't seem to find that. Could you try again.")
			
	else:
		return render(request, "Please do enter a valid ISBN.")
