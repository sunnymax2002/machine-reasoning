!pip install spacy_layout
import spacy
from spacy_layout import spaCyLayout
from typing import List

# Project specific imports
from models import *

class GraphGen:
	def importPDF(file_path:str):
		"""
		Function to import a single PDF file (e.g a chapter or entire textbook)
		and return a spaCy pipeline object

		"""
		nlp = spacy.blank("en")
		layout = spaCyLayout(nlp)

		# Process PDF directly into a spaCy Doc object
		doc = layout(file_path)

		# Access extracted text and layout features
		print(doc.text)
		print(doc._.tables) # Access extracted tables
		pass

	def extractSentences(pdfText: str) -> List[str]:
		"""
		Function to extract sentences from the imported PDF text

		"""
		pass

	def sentenceToTriplet(sentenceText: str) -> KnowledgeTriplet:
		"""
		Function to convert a sentence to a knowledge triplet

		"""
		pass

	def relateTriplets(triplet1: KnowledgeTriplet, triplet2: KnowledgeTriplet, triplet3: KnowledgeTriplet) -> Relation:
		"""
		Function to relate knowledge triplets

		"""
		pass

	def buildAnswer(Relation: Relation) -> str:
		"""
		Function to build an answer based on the related knowledge triplets

		"""
		pass
