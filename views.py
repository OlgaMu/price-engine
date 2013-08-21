from django.http import HttpResponse
from models import Book, Title
import pyodbc
import sklearn
from sklearn import neighbors
import cPickle
import datetime
from datetime import date
from datetime import timedelta
import time
from time import strftime

def search(request):
        return render(request, 'search.html')

def simple_output(request):
        if request:
                q= request.POST['q']
                conn= pyodbc.connect('DRIVER={NetezzaSQL};SERVER=netezza;DATABASE=STATS_GROUP_SANDBOX;UID=omusayev;PWD=yellow0444;Trusted_Connection=yes')
                cur=conn.cursor()

                query= "select b.ONSALE_DATE as onsale_date, b.rhsubject_desc as SUBJECT, b.subject_grp1 as CATEGORY, sum(a.qty_sld_amz) as PRE_SALES, \
                max(a.consumer_price_amz) as PRE_PRICE, max(a.SALES_RANK_AMZ) as MAX_RANK_PRE\
                from FAST_F_PROD_PRICE_SUMMARY as a\
                left join FAST_D_CMP_PROD as b\
                on b.prod_key=a.prod_key\
                where\
                b.format='EL'\
                and b.PUB_HOUSE_DESC='Random House'\
                and a.Date between '{date1}' and '{date2}'\
                and b.material='{isbn}'\
                group by b.MATERIAL, b.rhsubject_desc, b.subject_grp1, b.ONSALE_DATE"

                today=datetime.today().strftime('%Y-%m-%d')
                two_weeks_ago=  (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")
                params={'isbn': q, 'date2': today, 'date1': two_weeks_ago}
                cur.execute(query, params=params)
                data= cur.fetchone()
                names= data[0]
			        	conn.close()
		        		with open('ELASTICITYmodel.pkl', 'rb') as fid:  
		        		    pred_model= cPickle.load(fid)

                elasticity= pred_model.predict(names))
                return render(request, 'output_script.html', {"elast": elasticity})
                                              
			         	return render(request, 'simple_output.html', {"results": names})
        else:
			        	return HttpResponse('No results')
											  
