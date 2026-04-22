from typing import List

# Project specific imports
from models import *

class GraphGen:
	def importPDF():
		"""
		Function to import a single PDF file (e.g a chapter or entire textbook)

		"""
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
