import numpy as np

def input(request):
	return render(request, 'search_form.html')

def output(request):
	if 'isbn_input' in request.GET:
		isbn_input= request.GET['isbn_input']
		existing= NetezzaData.objects.filter(ISBN=isbn_input)
		
		if existing:
			model_recommends= existing.recommendation
			last_update= existing.today
			try:
				existing_also=GraphData.objects.get(ISBN=isbn_input).recommendation
				consumer_data_recommends= existing_also.recommendation
			except:
				consumer_data_recommends= "No recommendation."
			
			return render(request, 'results.html', {'queried_before'=True, 'neo4j_recommends'=consumer_data_recommends,'netezza_recommends'=model_recommends}
		else:
			model_inputs=NetezzaData.read_netezza(isbn_input)
		
			if model_inputs:
				elasticity= NetezzaData.predict_elasticity(model_inputs)
				model_recommends=NetezzaData.make_recommendation(elasticity)
				
				try:
					neighbor_price = GraphData.Neighbor_price_fetch(isbn_input)
					self_price = GraphData.Price_fetch(isbn_input)
					consumer_data_recommends=GraphData.make_recommendation(self_price, neighbor_price)
				except:
					copurchase_data_recommends="No recommendation."
				
				today=datetime.today().strftime('$Y-%m-%d')
				NetezzaData.save(ISBN=isbn_input, day_of_update=today, onsale_date=model_inputs[0], subject=model_inputs[1], category=model_inputs[2], pre_sales=model_inputs[3], price=model_inputs[4], maximum_amazon_rank= model_inputs[5], elasticity=elasticity, recommendation=model_recommends)
			
				GraphData.save(ISBN=isbn_input, Price= model_inputs[4], Neighbor_price= neighbor_price, recommendation=copurchase_info_recommends)
				
				return render(request, 'results.html', {'queried_before'=False, 'neo4j_recommends'= consumer_data_recommends, 'netezza_recommends'= model_recommends} 
			
			else:
				return HttpResponse("I'm sorry. I can't seem to find that. Could you try again?")
			
	else:
		return HttpResponse("Please do enter a valid ISBN.")
