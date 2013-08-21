from django.db import models
import neomodel
from neomodel import (StrcturedNode, StringProperty, IntegerProperty, RelationshipTo, RelationshiopFrom)
from neo4django.db import 

class Book(models.Model):
    ISBN= models.IntegerField(primary_key=True)
    title=models.CharField(max_length=50)
    price= models.IntegerField(default=0)
    sales= models.IntegerField(default=0)           #This should be a moving sum of the last two weeks of sales
    onsale_date=models.DateField()
    
    
class ebook(StructuredNode):
    ISBN=models.IntegerProperty(unique_index=True)
    title=models.StringProperty(max_length=30)
    
    def neighbors(self):
        results, metadata = self.cypher("START n=node({self}) MATCH n-[r]->(m) WHERE r.Type="Co-Purchased" WITH r, m ORDER BY r.weight DESC LIMIT 10 RETURN m");
        return [self.__class__.inflate(row[0]) for row in results]
