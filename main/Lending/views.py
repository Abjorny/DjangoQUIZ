from django.shortcuts import render 
from .models import LendingPage, UploadInfo, Quiz, ImagesQuiz, UtmExampleWork
from django.http import Http404
import json


def lendingForamted(lending: LendingPage, utmContent = None):
    utmExampleWork = UtmExampleWork.objects.filter(utm_content = utmContent).first()

    response_data = {
        "domain" : lending.domain,
        "title" : lending.title,
        "title_meta" : lending.title_meta,
        "description_meta" : lending.description_meta,
        "logo" : lending.logo.url,
        "chatid" : lending.chatid, 
        "number" : lending.number,
        "examples" : lending.examplesOfWork if utmExampleWork is None else utmExampleWork.examplesOfWork,
        "number_whatsap" : lending.number_whatsap,
        "username_telegram" : lending.username_telegram,
        "blackout" : lending.blackout,
        "description" : lending.description,
        "title_slider" : lending.title_slider,
        "preview_slider" : lending.preview_slider.url,
        "imageArrow" : lending.imageArrow.url,
        "imageCheckBoxPolit" : lending.imageCheckBoxPolit.url,
        "imageCheckBox" : lending.imageCheckBox.url,
        "title_swaper" : lending.title_swaper,
        "target_feedback" : lending.target_feedback,
        "target_quiz" : lending.target_quiz,
        "target_quiz_set" : lending.target_quiz_set,
        "EndFrameTextButton" : lending.quiz.endFrame.text_button,
        "icons" : [{"title" : icon.title,
                   "file" : icon.file.url} for icon in lending.icons.all()]
    }
    return response_data

def index(request): 
    utm_content = request.GET.get('utm_content', None)

    
    host = request.get_host()
    lengingPage = LendingPage.objects.filter(
        domain = str(host)
    ).first()

        
    if lengingPage is None : 
        raise Http404 
        

    quiz = lengingPage.quiz
    if utm_content is not None:
        quizs = Quiz.objects.all()
        for qui in quizs:
            if qui.utm_content is not None:
                if str(utm_content) in qui.utm_content:
                    quiz = qui
                    break

    questions = quiz.questionJson
    lending_data = lendingForamted(lending=lengingPage, utmContent= utm_content)

    question_data = []
    endFrameData = []

    for quest in questions:
        text  = quest['text']
        question_type = quest['question_type']
        inputs = quest['options']
        inputs_data = [{"text": input['text'],"placeholder" : input['placeholder'], "type_text" : input['type_text']} for input in inputs]
        question_data.append({
            "text" : text,
            "question_type" : question_type,
            "inputs_data" : inputs_data
        })
        
    endFrameData = {
        "title" : quiz.endFrame.title,
        "text_button" : quiz.endFrame.text_button,
        "text_phone" : quiz.endFrame.text_phone,
        "text_telegram" : quiz.endFrame.text_telegram,
        "text_whatsapp" : quiz.endFrame.text_whatsapp,
    }
    
    quizzes_json = {
        "title" : quiz.title,
        "endFrame" : endFrameData,
        "questions" : question_data[::-1],
    }

    
    if utm_content is not None:
        if utm_content.isdigit():
            utm_content = int(utm_content)
            uploadInfo = UploadInfo.objects.filter(
                app = utm_content
            ).first()            
            if uploadInfo is not None:
                lending_data["description"] = uploadInfo.title
                lending_data["title_slider"] = uploadInfo.subtitle
      
    if utm_content is not None:
        imagesQuiz = ImagesQuiz.objects.all()
        for image in imagesQuiz:
            if image.utm_content is not None:
                if str(utm_content) in image.utm_content:
                    lending_data['preview_slider'] = image.file.url
                    break 
              
    return render(request, "index.html", {
        "quizzes_json": json.dumps(quizzes_json),
        "landingPage": lending_data,
        "head" : lengingPage.head,
        "accentColor" : lengingPage.accentColor
    })

def polit(request):
    return render(request, "polit.html")