from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.decorators import classonlymethod
import asyncio

from agents import ClassifierAgent, EmailParserAgent, JSONAgent, PDFAgent

# Create your views here.

class ProcessInputView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @classonlymethod
    def as_view(cls, **initkwargs):
        # Make the view async-compatible
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine  # for Django <4.2
        return view

    async def post(self, request):
        input_text = request.data.get('input_text')
        file = request.FILES.get('file')

        classifier = ClassifierAgent()
        email_agent = EmailParserAgent()
        json_agent = JSONAgent()
        pdf_agent = PDFAgent()

        # 1. Classify input
        if file:
            # Assume PDF
            file_bytes = file.read()
            classification = await classifier.classify("PDF file uploaded")
            agent_result = await pdf_agent.parse(file_bytes)
        elif input_text:
            classification = await classifier.classify(input_text)
            if classification.format.lower() == 'email':
                agent_result = await email_agent.parse(input_text)
            elif classification.format.lower() == 'json':
                agent_result = await json_agent.process(input_text)
            else:
                agent_result = {"error": "Unknown format"}
        else:
            return Response({"error": "No input provided."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "classification": classification.dict(),
            "agent_result": agent_result
        }, status=status.HTTP_200_OK)
