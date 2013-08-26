#models.py
from django.db import models
import py2neo
from py2neo import neo4j, cypher
import datetime
from datetime import datetime, strftime
try:
	import cPickle as pickle
except ImportError:
	import pickle
import numpy as np
	

class Book(models.Model)
	ISBN=IntegerProperty(unique_index=True)
	Name=StringProperty(max_length=25)

	class Meta:
		abstract= True
		
class NetezzaData(Book):
	day_of_update=models.DateField()
	
	
	def read_netezza(self, isbn):
		conn= pyodbc.connect('DRIVER={NetezzaSQL};SERVER=netezza;DATABASE=STATS_GROUP_SANDBOX;UID=omusayev;PWD=yellow0444')
		cur=conn.cursor()
		
		today=datetime.today().strftime('%Y-%m-%d')
		two_weeks_ago=  (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")	
		
		query= "select b.ONSALE_DATE as onsale_date, b.rhsubject_desc as SUBJECT, b.subject_grp1 as CATEGORY, sum(a.qty_sld_amz) as PRE_SALES, max(a.consumer_price_amz) as PRE_PRICE, max(a.SALES_RANK_AMZ) as MAX_RANK_PRE
		from FAST_F_PROD_PRICE_SUMMARY as a
		left join FAST_D_CMP_PROD as b
		on b.prod_key=a.prod_key
		where
		b.format='EL'
		and a.Date between '{date1}' and '{date2}'
		and b.material='{isbn}'
		group by b.MATERIAL, b.rhsubject_desc, b.subject_grp1, b.ONSALE_DATE"
					
		
		params={'isbn': isbn, 'date2': today, 'date1': two_weeks_ago}
		cur.execute(query, params=params)
		model_inputs= cur.fetchone()
		conn.close()
		
		return model_inputs
	
	onsale_date, subject, category, pre_sales, price, maximum_amazon_rank=  property(read_netezza)
	
	def predict_elasticity(self, model_inputs):
		inputs= np.array(model_inputs)
		elast_model = pickle.load("ELASTICITYmodel.pkl")
		forecast = elast_model.predict(inputs)
		
		return prediction
	
	elasticity= property(make_recommendation)
	def make_recommendation(self, elasticity):
		if elasticity <0:
			return "Do not discount."
		elif elasticity >0:
			return "Discount away."
		else:
			return "Something just went horribly wrong."
		
	model_recommends= property(make_recommendation)
	
	
	
	
class GraphData(Book):
	graphDB= neo4j.GraphDatabaseService("http://nycold:7474/db/data/")
	
	def Price_fetch(self, isbn):
		query= "START n=node:ni(ISBN="{isbn}") return n.Price"
		data, metadata =cypher.execute(graphDB, query)
	Price= property(Price_fetch)

	def Neighbor_price_fetch(self, ISBN):
		query= "START n=node:ni(ISBN={ISBN}) MATCH n-[r]-m WHERE has(m.Type) and has(m.Price) and m.Type='Title' with n, r ORDER BY r.weight DESC LIMIT 15 RETURN avg(m.Price)"
		data = cypher.execute(graphDB, query)
		if isinstance(data[0][0], list):
			return data[0][0][0]
		else:
			return data[0][0]
	Neighbor_price= property(Neighbor_price_fetch)

	def make_recommendation(self, self_price, neighbor_price):
		
		dif= self.Neighbor_price - self.Price
		if dif>1:
			return "Raise Price"
			
		elif dif<-1:
			return "Lower Price"
		
		else:
			return "Priced about right."
			
	consumer_data_recommends= property(decide)
