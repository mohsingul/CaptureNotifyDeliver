import random
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
import firebase_admin
import firestore as firestore
import pandas as pd
from django.shortcuts import render, redirect
import spacy
import pickle
import nltk

from django.http import HttpResponse
# Create your views here.

import pyrebase
import html
import firebase
from firebase import Database
from pyfcm import FCMNotification

from . import models

from firebase_admin import credentials, firestore
# def index(request):
#     return render(request, 'Admin_dashboard_html_view/index.html')

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
import django_tables2

import pusher

pusher_client = pusher.Pusher(
  app_id='967593',
  key='f32834e6dbaf46b5b529',
  secret='5f2620f1111f3c0cb025',
  cluster='ap2',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

firebaseConfig = {
    'apiKey': "AIzaSyDwms8eJIXd463tuvXPCfSaSFwcEA-7Seo",
    'authDomain': "practicedatabase-a87eb.firebaseapp.com",
    'databaseURL': "https://practicedatabase-a87eb.firebaseio.com",
    'projectId': "practicedatabase-a87eb",
    'storageBucket': "practicedatabase-a87eb.appspot.com",
    'messagingSenderId': "697315903934",
    'appId': "1:697315903934:web:070b103c0ae416233a11ef",
    'measurementId': "G-DNJ45NKVKQ"
  }

# firebaseConfig = {
#     'apiKey': "AIzaSyDTu1PNqHiUbVmY47MGFQ7d5qQhueJCKoI",
#     'authDomain': "fypdatabase-d39d3.firebaseapp.com",
#     'databaseURL': "https://fypdatabase-d39d3.firebaseio.com",
#     'projectId': "fypdatabase-d39d3",
#     'storageBucket': "fypdatabase-d39d3.appspot.com",
#     'messagingSenderId': "400254986820",
#     'appId': "1:400254986820:web:0c4b80983ac5077ceaea11",
#     'measurementId': "G-MFHBTBXNSN"
#   };
firebase = pyrebase.initialize_app(firebaseConfig)

GOOGLE_APPLICATION_CREDENTIALS = 'C:\\Users\\mohsi\\PycharmProjects\\Admin_View\\ServiceAccountKey.json'
# GOOGLE_APPLICATION_CREDENTIALS = 'C:\\Users\\mohsi\\PycharmProjects\\Admin_View\\Servicekey.json'
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def registration(request):
    errors = []
    if request.method == "POST":
        print("inside post")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        password2 = request.POST.get("pass2")

        if password == password2:
            if User.objects.filter(email=email).exists():
                errors.append("Email Taken! Try using another Email")

                return render(request, "Admin_dashboard_html_view/registration.html", {"message": "Email is already Registered"})
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                print("user created")
                user.save()
                return HttpResponseRedirect(reverse("login"))

        else:
            errors.append('Password not matching')
            return HttpResponseRedirect(reverse("registration"))

    return render(request, "Admin_dashboard_html_view/registration.html", {"errors": errors})


def login(request):
    errors=[]
    if request.method == "POST":
        print("inside post login")
        username = request.POST.get("username")
        print(username)
        password = request.POST.get("pass")
        print(password)
        user_auth = auth.authenticate(username=username, password=password)
        print(user_auth)
        if user_auth is not None:
            auth.login(request, user_auth)
            print("login successful")
            return HttpResponseRedirect(reverse("home"))
        else:
            errors.append("Invalid Credentials")
            print(errors)
            print("login unsuccessful")
            return (request, "Admin_dashboard_html_view/login_form.html", {"errors": errors})
    else:
        return render(request, "Admin_dashboard_html_view/login_form.html")

def fcm_token(Email):
    # pass name in the function of recipient so that it goes only in that document
    token = ""
    Recipientcol = db.collection("Recipient").list_documents()
    name_query = db.collection("Recipient").where("Email", "==", Email)
    for doc in Recipientcol:
        if name_query:
            token_col = doc.collection("FCM_token").get()
            for doc_token in token_col:
                token = doc_token.to_dict().get('token_ID')
    return token

def all_packages(request):
    Recipient_list = []
    Letter_list=[]
    recipient_col = db.collection('Recipient').list_documents()
    Recipient_list1=[]
    key_list=[]
    value_list=[]
    for docs in recipient_col:

        doc_letter = docs.collection('Letter').get()
        for docss in doc_letter:

            Recipient_list.append(docs.get(field_paths={'Name', 'Email', 'Deptname'}).to_dict())
            Recipient_list.append(docss.to_dict())

    final_recipientlist = []
    for i in range(len(Recipient_list)-1):
        if i == 0 or i % 2 == 0:
            z = Recipient_list[i].copy()
            z.update(Recipient_list[i+1])
            final_recipientlist.append(z)
    print(f'Final recipient list {final_recipientlist}')




    for recipients in Recipient_list:
        for key, val in recipients.items():
            key_list.append(key)
            value_list.append(val)
        Recipient_list1.append(value_list)


    key_dic = {}
    i=0
    key_lists = []
    for keys in list(dict.fromkeys(key_list)):
        i = i+1
        key_dic[i] = keys
        key_lists.append(key_dic)


    return render(request, "Admin_dashboard_html_view/all_packages.html",  {"Recipient_keys": (dict.fromkeys(key_list)),
                                                                          "Recipient_values": value_list,
                                                                            "Recipient": final_recipientlist})


def pendingpackages(request):
    Recipient_list = []
    Letter_list = []
    recipient_col = db.collection('Recipient').list_documents()
    Recipient_list1 = []
    key_list = []
    value_list = []
    for docs in recipient_col:

        doc_letter = docs.collection('Letter').where("Status", "==", "pending").get()
        for docss in doc_letter:
            Recipient_list.append(docs.get(field_paths={'Name', 'Email', 'Deptname'}).to_dict())
            Recipient_list.append(docss.to_dict())

    final_recipientlist = []
    for i in range(len(Recipient_list) - 1):
        if i == 0 or i % 2 == 0:
            z = Recipient_list[i].copy()
            z.update(Recipient_list[i + 1])
            final_recipientlist.append(z)
    print(f'Final recipient list {final_recipientlist}')

    for recipients in Recipient_list:
        for key, val in recipients.items():
            key_list.append(key)
            value_list.append(val)
        Recipient_list1.append(value_list)
    return render(request, "Admin_dashboard_html_view/pendingpackages.html", {"Recipient_keys": (dict.fromkeys(key_list)),
                                                                           "Recipient_values": value_list,
                                                                           "Recipient": final_recipientlist})

def collectedpackages(request):
    Recipient_list = []
    Letter_list = []
    recipient_col = db.collection('Recipient').list_documents()
    Recipient_list1 = []
    key_list = []
    value_list = []
    for docs in recipient_col:

        doc_letter = docs.collection('Letter').where("Status", "==", "collected").get()
        for docss in doc_letter:
            Recipient_list.append(docs.get(field_paths={'Name', 'Email', 'Deptname'}).to_dict())
            Recipient_list.append(docss.to_dict())

    final_recipientlist = []
    for i in range(len(Recipient_list) - 1):
        if i == 0 or i % 2 == 0:
            z = Recipient_list[i].copy()
            z.update(Recipient_list[i + 1])
            final_recipientlist.append(z)
    print(f'Final recipient list {final_recipientlist}')

    for recipients in Recipient_list:
        for key, val in recipients.items():
            key_list.append(key)
            value_list.append(val)
        Recipient_list1.append(value_list)
    return render(request, "Admin_dashboard_html_view/collectedpackages.html",
                  {"Recipient_keys": (dict.fromkeys(key_list)),
                   "Recipient_values": value_list,
                   "Recipient": final_recipientlist})


def home(request):

    if request.method == "POST":
        id = (request.POST.get('id'))
        row_index = request.POST.get('row_index')
        print(f'row index{row_index}')
        doc_id = request.POST.get('doc_id')
        if len(row_index) > 0:
            r_index = int(row_index)
        print(f'doc_id {doc_id}')
        doc_id_editdist = request.POST.getlist('doc_id_editdist')
        sender = request.POST.get('sender')
        DOA = request.POST.get('date')
        status = request.POST.get('status')
        dict_letter={}
        dict_letter2={}


        dict_letter["DOA"] = DOA
        dict_letter["LetterID"] = id
        dict_letter["Sender"] = sender
        dict_letter["Status"] = status


        dict_letter2["LetterID"] = id
        dict_letter2["Sender"] = sender
        dict_letter2["DOA"] = DOA

        if len(doc_id_editdist) > 0:
            print(r_index)
            Recipient_query = db.collection("Recipient").document(doc_id_editdist[r_index])
            letter_query = Recipient_query.collection("Letter").add(dict_letter)
            notify_query = Recipient_query.collection("Notification").add(dict_letter2)
            email_dist = request.POST.get("email_editdt")
            print(email_dist)
            token = fcm_token(email_dist)
            notification = fcm_send_single_device_notification(token)
            print(notification)

        elif len(doc_id) > 0:
            Recipient_query = db.collection("Recipient").document(doc_id)
            letter_query = Recipient_query.collection("Letter").add(dict_letter)
            notify_query = Recipient_query.collection("Notification").add(dict_letter2)
            email = request.POST.get("email")
            print(email)
            token = fcm_token(email)
            notification = fcm_send_single_device_notification(token)
            print(notification)



    return render(request, 'Admin_dashboard_html_view/home.html')

FCM_SERVER_KEY = "AAAAoltESb4:APA91bHnd8HJ6HKnqHNurcKUTr5kpVTUkCeIGe5da5UV3x_7BenDYoFs-gEaSEWPItsLeYarsQ9amDeaERoZdZlamPEcEnGKY-4yXsn-693JkIKya5ITtTVqLjbHaOim5pVqfDOY8voR"
def fcm_send_single_device_notification(
        registration_id,
        title=None,
        body="New Letter Recieved",
        icon=None,
        data=None,
        sound="Default",
        badge=None,
        low_priority=False,
        condition=None,
        time_to_live=None,
        collapse_key=None,
        delay_while_idle=False,
        restricted_package_name=None,
        dry_run=False,
        color=None,
        tag=None,
        body_loc_key=None,
        body_loc_args=None,
        title_loc_key=None,
        title_loc_args=None,
        content_available=None,
        extra_kwargs={},
        api_key=None,
        **kwargs):
    push_service = FCMNotification(api_key=FCM_SERVER_KEY if api_key is None else api_key)
    result = push_service.notify_single_device(
        registration_id=registration_id,
        message_title=title,
        message_body=body,
        message_icon=icon,
        data_message=data,
        sound=sound,
        badge=badge,
        collapse_key=collapse_key,
        low_priority=low_priority,
        condition=condition,
        time_to_live=time_to_live,

        delay_while_idle=delay_while_idle,
        restricted_package_name=restricted_package_name,
        dry_run=dry_run,
        color=color,
        tag=tag,
        body_loc_key=body_loc_key,
        body_loc_args=body_loc_args,
        title_loc_key=title_loc_key,
        title_loc_args=title_loc_args,
        content_available=content_available,
        extra_kwargs=extra_kwargs,
        **kwargs
    )
    return result


def recipient_name_after_thresholding(final_receplist, words):
    min_list = []
    recipient_dict = {}
    edit_distance = []
    for w in range(len(words)):
        for i in final_receplist:
            for j in i:
                edit_dist = nltk.edit_distance(words[w], j)
                min_list.append(edit_dist)

        recipient_dict[words[w]] = min(min_list)
        min_list = []

    print(edit_distance)

    print(f'recipient dictionary {recipient_dict}')
    recipient_name = ""
    for key, value in recipient_dict.items():
        if value <= 2:
            recipient_name = recipient_name + key
            recipient_name = recipient_name + " "

    print(recipient_name.rstrip())
    return recipient_name.rstrip()





def notification(request):
    o = models.OCR()
    edit_names=[]
    error = []
    len_list_threshold = 0
    len_error = 0
    len_list_name = 0
    heading = ""
    email_editdist = ""
    doc_id_editd = []
    edit_dist_list = []
    list_threshold = []
    list_name = []
    final_editlist=[]
    list_key = []
    allrecipient_list = []
    doc_id_editdist = []
    email = " "
    doc_id_user = " "
    id = ' '
    output_recipientname = " "
    output_departmentname = " "
    binarized_image = ""
    from datetime import datetime
    t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == "POST":
        imagepath = request.FILES['fileup']
        binarized_image = o.output(imagepath.name)
        print(binarized_image.lower())
        # output_recipientname = ocr_nlp(binarized_image)


        # output_departmentname = ner(binarized_image)

        recipient_name=""
        department_name=""
        crf_dict = CRF_NER(binarized_image)
        for key, values in crf_dict.items():
            if key == "Recipient Name":
                recipient_name = values
            elif key == "Department Name":
               department_name = values
        print(f'Recipient_name {recipient_name}')
        print(f'Department_name {department_name}')

        token = ""
        # print(f'recipient {output_recipientname}')
        # print(f'department {output_departmentname}')
        Recipientcol = db.collection("Recipient").get()

        for all_recipients in Recipientcol:
            allrecipient_list.append(all_recipients.to_dict())

        print(f'allrecipient_list {allrecipient_list}')

        recipient_query = db.collection("Recipient")

        check_name_query = recipient_query.where("Name", "==", recipient_name.strip()).where("Deptname", "==",
                                                                                            department_name.strip()).get()

        listk= [1, 2, 3, 4]
        dictkey={}
        counter= 0


        for user in check_name_query:
            list_name.append(user.to_dict())
            doc_id_user = user.id
        print(f'listname {list_name}')
        for users in list_name:
            for key, val in users.items():
                dictkey[listk[counter]] = key
                counter = counter+1
        list_key.append(dictkey)
        print(list_key)
        registered_users=[]
        len_list_name = len(list_name)
        if len(list_name) > 0:
            print("User is Registered in Database!")
            heading="Select User From Given List"
            for users in list_name:
                for key, val in users.items():
                    if key == "Email":
                        email = val
                        id = random.randint(1, 10000)
        else:
            list_threshold = []
            final_recipientlist = []
            id = random.randint(1, 10000)
            words = binarized_image.split()
            for values in allrecipient_list:
                for key, val in values.items():
                    if key == "Name":
                        name = val.split()
                        final_recipientlist.append(name)

            recep_name_edit = recipient_name_after_thresholding(final_recipientlist, words)
            for values in allrecipient_list:
                for key, val in values.items():
                    if key == "Name":
                        edit_distance = nltk.edit_distance(recep_name_edit.lower(), val)
                        if edit_distance <= 7:
                            list_threshold.append(values)

            len_list_threshold = len(list_threshold)
            if len(list_threshold) < 0:
                error.append("User is not Registered")
                len_error = len(error)

            heading = "Smart Suggestions"
            for user_edit in list_threshold:
                for k, v in user_edit.items():
                    if k == 'Name':
                        edit_names.append(v)

            for n in edit_names:
                edit_names_query = recipient_query.where("Name", "==", n).get()
                final_editlist.append(edit_names_query)

            for edit_user in final_editlist:
                for usr in edit_user:
                    user_id = usr.id
                    doc_id_editdist.append(user_id)



            for us in list_threshold:
                for key, val in us.items():
                    if key == "Email":
                        email_editdist = val

        print(f'List_threshold {list_threshold}')
        print(f'doc_id_editdist {doc_id_editdist}')

    return render(request, "Admin_dashboard_html_view/notification.html", {"registered_user": list_name, "keys": list_key,
                                                                           "doc_id": doc_id_user, "email": email,
                                                                           "id": id,
                                                                           "error": error,
                                                                           "time":t,
                                                                           "heading": heading,
                                                                           "email_editdist": email_editdist,
                                                                           "doc_id_editdist": doc_id_editdist,
                                                                           "edit_dist_list": list_threshold,
                                                                           "len_list_threshold":len_list_threshold,
                                                                           "len_error":len_error,
                                                                           "len_register_user": len_list_name,
                                                                                                    })


def members(request):
    members_list=[]
    members_keys=[]
    members_values=[]
    query_recep= db.collection("Recipient").list_documents()
    for recep in query_recep:
        members_list.append(recep.get(field_paths={'Name', 'Email', 'Deptname'}).to_dict())
    for recipients in members_list:
        for key, val in recipients.items():
            members_keys.append(key)
            members_values.append(val)
    print(members_keys)
    return render(request, "Admin_dashboard_html_view/members.html", {"membervalues": members_values,
                                                                      "memberkeys": members_keys,
                                                                      "members": members_list})



def query(request):

    # doc_ref = db.collection("Recipient").document.getDocument().getReference().collection("Letter")
    # .whereEqualTo("Status", "pending")
    # .addSnapshotListener(new EventListener < QuerySnapshot > () {

    # Rec_name = db.document.getDocument().getString("Name")
    # Depname = db.document.getDocument().getString("Deptname")

    # doc_ref = db.collection('Recipient').stream()
    # doc_letter = db.collection('Recipient').document.getDocument().getReference().collection("Letter").stream()

    # Recipient_list = []

    # if request.method == "GET":
    #     print("hello")
        # all = request.GET.get('all')
        # if not all:
        #     print("hello mohsin")
        # else:
        # all=request.GET.get('all')
        # print(all)

    # if request.method == "GET":
    #     recipient_col = db.collection('Recipient').list_documents()


        # for docs in recipient_col:
                            # print(u'{} => {}'.format(docs.id, docs.to_dict()))
                            # doc_letter = docs.doc().collection('Letter').stream()
            # doc_letter = docs.collection('Letter').get()
                            # docs.stream()
                            # print('{} => {}.'.format(docs.id, docs.to_dict()))
                            # Recipient_list.append(docs.to_dict())
                            # print(docs.get().to_dict())

                            # Recipient_list.append(docs.get().to_dict())
            # for docss in doc_letter:
                                # print(u'{} => {}'.format(docss.id, docss.to_dict()))
                                # print(docss.to_dict())
                                # Letter_list.append(docss.to_dict())
                                # recipient_dict[Recipient_list] = Letter_list
                # Recipient_list.append(docs.get(field_paths={'ID', 'Name', 'Email', 'Deptname'}).to_dict())
                # Recipient_list.append(docss.to_dict())

                    # RecipientListView(Recipient_list)

    # elif request.GET.get("parameter") == "pendingpackages":
    #
    #         recipient_col = db.collection('Recipient').list_documents()
    #
    #
    #         for docs in recipient_col:
    #
    #             doc_letter = docs.collection('Letter').where("Status", "==", "pending").get()
    #             for docss in doc_letter:
    #
    #                 Recipient_list.append(docs.get(field_paths={'ID', 'Name', 'Email', 'Deptname'}).to_dict())
    #                 Recipient_list.append(docss.to_dict())
    # elif request.GET.get("parameter") == "collectedpackages":
    #
    #     recipient_col = db.collection('Recipient').list_documents()
    #     for docs in recipient_col:
    #
    #         doc_letter = docs.collection('Letter').where("Status", "==", "collected").get()
    #         for docss in doc_letter:
    #             Recipient_list.append(docs.get(field_paths={'ID', 'Name', 'Email', 'Deptname'}).to_dict())
    #             Recipient_list.append(docss.to_dict())

    # paginator = Paginator(Recipient_list, 10)
    # # page = request.GET.get('page', 1)
    # Recipient_list = paginator.get_page(page)
    # page = 1
    # if request.is_ajax():
    #     print("ajax")
    #     query = request.GET.get('page')
    #     if query is not None:
    #         page = query
    #
    # try:
    #     Recipient_list = paginator.get_page(page)
    # except (EmptyPage, InvalidPage):
    #     Recipient_list = paginator.page(paginator.num_pages)
    # o = models.OCR()
    # binarized_image = ""
    # if request.method == "POST":
    #     imagepath = request.FILES['fileup']
    #     binarized_image = o.output(imagepath.name)
    # output_recipient_name = ocr_nlp(binarized_image)
    # output_department_name = ner(binarized_image)
    # print(output_recipient_name)
    # print(output_department_name)

    # is_registered(output)

    return render(request, 'main_navbar.html')
    # except PageNotAnInteger:
    #     Recipient_list = paginator.page(1)
    # except EmptyPage:
    #     Recipient_list = paginator.page(paginator.num_pages)

# def is_registered(recipient_name):
#     recipient_col = db.collection('Recipient').list_documents()
#
#     for docs in recipient_col:
#         name = docs.get(field_paths={'Name'}).to_dict()
#         if name == recipient_name:
#
#             #got to the next page comprising of letter info
#             #else register the person in android app also then move to the next letter info page

def test_sentence_getter(data):
    agg_func = lambda s: [(w, p) for w, p in zip(s["Words"].values.tolist(), s["POS"].values.tolist())]
    test_grouped = data.groupby("Sentences").apply(agg_func)
    test_sentences = [s for s in test_grouped]
    return test_sentences



    # Feature Extraction
def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][0]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3]': word[-3:],
        'word[-2]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }

    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })

    else:
        features['EOS'] = True

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def CRF_NER(binarized_image):
    filename = 'C:\\Users\\mohsi\\CRF_FYP\\finalized_model.sav'
    raw_list = []
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(binarized_image.lower())
    counter = 0
    for token in doc:
        raw_list.append(f"Sentence:{counter}|{token.text}|{token.pos_}")
    print(f'rawlist: {raw_list}')
    test_sent_list = []
    for i in raw_list:
        test_sent_list.append(i.split("|"))

    print(test_sent_list[1])
    data = pd.DataFrame(test_sent_list[0:100], columns=["Sentences", "Words", "POS"])

    test_sen = test_sentence_getter(data)
    x = [sent2features(s) for s in [test_sen[0]]]

    model_crf_load = pickle.load(open(filename, 'rb'))

    y_pred = model_crf_load.predict(x)

    list_sen = []
    list_pred = []
    list_final = []

    for i in test_sen:
        for j in i:
            list_sen.append(j)
    for i in y_pred:
        for j in i:
            list_pred.append(j)

    for i, j in zip(list_sen, list_pred):
        i = i + (j,)
        list_final.append(i)

    pred_dataframe = pd.DataFrame(list_final, columns=['Words', 'POS', 'Predictions'])

    pred_dataframe2 = pred_dataframe.set_index("Predictions", drop=False)

    recipient_name = []
    depar_name = []
    out_dict = {}
    print(pred_dataframe2)
    try:
        recipient_name = pred_dataframe2.loc[['B-Recipient_name'], 'Words'].values.tolist()
        print(f"Recipient Name {recipient_name}")
    except KeyError:
        recipient_name = " "

    try:
        depar_name = pred_dataframe2.loc[['B-Department_name', 'I-Department_name'], 'Words'].values.tolist()
    except KeyError:
        depar_name = pred_dataframe2.loc[['B-Department_name'], 'Words'].values.tolist()


    output_rec = []
    output_dep = []
    t1 = ""
    t2 = ""
    for rec in recipient_name:
        t1 = t1 + rec
        t1 = t1 + " "

    out_dict['Recipient Name'] = t1
    print(f't1{t1}')

    for dep in depar_name:
        t2 = t2 + dep
        t2 = t2 + " "

    out_dict['Department Name'] = t2
    return out_dict

def ner_recipientname(binarized_image):
    nlp = spacy.load("C:\\Users\\mohsi\\PycharmProjects\\FirstPractice\\Recipient_names_trainedmodel1")
    name_list = []
    output_string = " "
    binarized_image = binarized_image.lower()
    for word in binarized_image.split():
        print(f'word: {word}')
        doc = nlp(word)
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)

            output_string = output_string + ent.text
            output_string = output_string + " "
            print(f'outputstring: {output_string}')
    # name_list.append(output_string)
    # output_string.rstrip()
    return output_string

def ner(binarized_image):
    nlp = spacy.load("C:\\Users\\mohsi\\PycharmProjects\\FirstPractice\\Departmentnames_trainedmodel")
    doc = nlp(binarized_image)
    for ent in doc.ents:
         print(ent.text, ent.start_char, ent.end_char, ent.label_)
         return ent.text























































# from django.contrib.auth.models import User
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#
# def index(request):
#     user_list = User.objects.all()
#     page = request.GET.get('page', 1)
#
#     paginator = Paginator(user_list, 10)
#     try:
#         users = paginator.page(page)
#     except PageNotAnInteger:
#         users = paginator.page(1)
#     except EmptyPage:
#         users = paginator.page(paginator.num_pages)
#
#     return render(request, 'core/user_list.html', { 'users': users })



# import django_tables2 as tables
#
#
# class SimpleTable(tables.Table):
#     class Meta:
#         model = Simple
#
#
# class TableView(tables.SingleTableView):
#     table_class = SimpleTable
#     queryset = Simple.objects.all()
#     template_name = "practice.html"
#

    #     String
    # DOA = doc.getDocument().getString("DOA");
    # String
    # DOD = doc.getDocument().getString("DOD");
    # String
    # status = doc.getDocument().getString("Status");
