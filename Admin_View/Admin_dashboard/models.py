from django.db import models

from django.contrib.auth import get_user_model
from django.db import models
from django_tables2 import SingleTableView

import cv2
import pytesseract
from PIL import Image
import spacy
import plac
import random
import pdb;
from pathlib import Path
from spacy.util import minibatch, compounding
from tqdm import tqdm
from spacy.matcher import PhraseMatcher


# class Vocabulary:
#     PAD_token = 0  # Used for padding short sentences
#     SOS_token = 1  # Start-of-sentence token
#     EOS_token = 2  # End-of-sentence token
#
#     def __init__(self, name):
#         self.name = name
#         self.word2index = {}
#         self.word2count = {}
#         self.index2word = {self.PAD_token: "PAD",self.SOS_token: "SOS", self.EOS_token: "EOS"}
#         self.num_words = 3
#         self.num_sentences = 0
#         self.longest_sentence = 0
#
#     def add_word(self, word):
#         if word not in self.word2index:
#             # First entry of word into vocabulary
#             self.word2index[word] = self.num_words
#             self.word2count[word] = 1
#             self.index2word[self.num_words] = word
#             self.num_words += 1
#         else:
#             # Word exists; increase word count
#             self.word2count[word] += 1
#
#     def add_sentence(self, sentence):
#         sentence_len = 0
#         for word in sentence.split(' '):
#             sentence_len += 1
#             self.add_word(word)
#         if sentence_len > self.longest_sentence:
#             # This is the longest sentence
#             self.longest_sentence = sentence_len
#         # Count the number of sentences
#         self.num_sentences += 1
#
#     def to_word(self, index):
#         return self.index2word[index]
#
#     def to_index(self, word):
#         return self.word2index[word]


sourcepath = "D:/BS(CS) 7-A/FInal FYP proposal/"

im = ""
class OCR:

    def binarization(self, image, imagepath):
        grayscale = cv2.imread(image, 0)
        retval , threshold = cv2.threshold(grayscale, 100, 255, cv2.THRESH_BINARY)
        gausian = cv2.adaptiveThreshold(grayscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 12)
        cv2.imwrite(sourcepath + "/gausianadaptive_" + imagepath, gausian)
        tessaract = pytesseract.image_to_string(
        Image.open(sourcepath + "gausianadaptive_" + imagepath))
        return tessaract

    def output(self, imagepath):

        result = self.binarization(sourcepath + imagepath, imagepath)
        return result

class NER:
    def trained_model(self):
        TRAIN_DATA = [(
                      'Department of Computer Engineering is committed to excellence in teaching, research and inculcating a sense of pride and confidence in our students. ',
                      {'entities': [(14, 34, 'Department_name')]}), (
                      'he aim of the department is to pursue excellence in Computer Engineering through teaching and research and we are achieving our objectives with the help of our highly qualified and distinguished faculty of national and international repute.\r',
                      {'entities': [(52, 72, 'Department_name')]}),
                      (
                      'Department of Computer Engineering endeavors to provide best learning and professional opportunities to our students and work hard for their bright future\r',
                      {'entities': [(14, 34, 'Department_name')]}), (
                      'The Department of Computer Sciences at Bahria University is home of quality education and multidisciplinary research',
                      {'entities': [(18, 35, 'Department_name')]}), (
                      'The BS Computer Science program provides understanding of the fundamental and advanced concepts.\r',
                      {'entities': [(7, 24, 'Department_name')]}),
                      (
                      'The aim of the department is to pursue excellence in Computer Engineering through teaching and research and we are achieving our objectives with the help of our highly qualified and distinguished faculty of national and international repute.\r',
                      {'entities': [(53, 73, 'Department_name')]}),
                      (
                      'Department of Computer Engineering is committed to excellence in teaching, research and inculcating a sense of pride and confidence in our students. We target to enhance not only their academic knowledge but to nurture their practical skills and provide professional grooming so that our students are ready to serve as they join industry and provide valuable contribution.\r',
                      {'entities': [(14, 35, 'Department_name')]}),
                      (
                      'Department of Computer Engineering endeavors to provide best learning and professional opportunities to our students and work hard for their bright future.\r',
                      {'entities': [(14, 34, 'Department_name')]}),
                      (
                      'Department of Software Engineering aims to be recognized as a leader in Software Engineering education and research through excellence in modern education and targeted research in emerging areas of Software Engineering',
                      {'entities': [(14, 34, 'Department_name')]}), (
                      'The mission of Bachelor of Software Engineering program is to prepare technically strong Software Engineers who can contribute effectively towards the nation, society and the world at large through effective problem solving skills, application of engineering knowledge, leadership and healthy lifelong learning attitude.\r',
                      {'entities': [(26, 47, 'Department_name')]}),
                      (
                      'Software Engineering department aims to deliver a strong and coherent Software Engineering program for the development of skilled Software Engineers. The curriculum is inline with PEC and HEC regulations to equip students with latest skills for industry and research activities. Software Engineering graduates should achieve the following educational objectives:\r',
                      {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'Graduates should demonstrate competence in applying Software Engineering knowledge & practices in various phases of software/system development life cycle in their respective professional career.\r',
                      {'entities': [(52, 73, 'Department_name')]}),
                      ('An ability to apply knowledge of computer science.',
                       {'entities': [(33, 50, 'Department_name')]}),
                      ('Software engineering fundamentals and an engineering specialization to the solution',
                       {'entities': [(0, 20, 'Department_name')]}),
                      ('Of complex software engineering problems', {'entities': [(11, 31, 'Department_name')]}),
                      (
                      'An ability to identify, formulate, research literature and analyze complex software engineering problems reaching substantiated conclusions using software engineering principles, natural sciences and engineering sciences',
                      {'entities': [(75, 95, 'Department_name')]}), (
                      'An ability to design solutions for complex software engineering problems and design systems, components or processes that meet specified needs with appropriate consideration for public health and safety, cultural, societal, and environmental considerations.\r',
                      {'entities': [(43, 63, 'Department_name')]}),
                      (
                      'Programming language theory considers approaches to the description of computational processes, while software engineering involves the use of programming languages and complex systems',
                      {'entities': [(102, 122, 'Department_name')]}),
                      (
                      'Computer science is the study of processes that interact with data and that can be represented as data in the form of programs. It enables the use of algorithms to manipulate, store, and communicate digital information. A computer scientist studies the theory of computation and the design of software systems',
                      {'entities': [(0, 16, 'Department_name')]}), (
                      'This branch of computer science aims to manage networks between computers worldwide',
                      {'entities': [(15, 31, 'Department_name')]}),
                      (
                      'Open the door to sought-after technology careers with a world-class online Bachelor of Science (BSc) in Computer Science degree from the University of London.\r',
                      {'entities': [(104, 120, 'Department_name')]}), (
                      'The course material ranges from entry-level subjects to specialised topics. Hold a degree outside of computer science',
                      {'entities': [(101, 117, 'Department_name')]}), (
                      'Whether you have high school qualifications or experience working in a computer science field, earning a valuable degree helps move your career forward. \r',
                      {'entities': [(70, 88, 'Department_name')]}),
                      (
                      'The course material ranges from entry-level subjects to specialised topics. If you already have a degree outside of computer science, the curriculum will bring you up-to-date on the latest industry applications and practices',
                      {'entities': [(116, 132, 'Department_name')]}),
                      (
                      'With the BSc Computer Science, you can apply for a range of computational and mathematical jobs in the creative industries, business, finance, education, medicine, engineering and science',
                      {'entities': [(13, 29, 'Department_name')]}),
                      (
                      'The University of London offers a number of online taster courses and Massive Open Online Courses (MOOCs), designed to introduce you to themes included in degree programmes. Choose from three open courses that explore topics covered in the BSc Computer Science degrees',
                      {'entities': [(244, 260, 'Department_name')]}),
                      (
                      'No background in Computer science is required. If you satisfy the admissions requirements you will be admitted on to the course. Please see the admissions requirements for further information about the entry routes available.\r',
                      {'entities': [(17, 33, 'Department_name')]}),
                      ('Computer science students have excellent graduate prospects',
                       {'entities': [(0, 16, 'Department_name')]}),
                      ('Check out our Computer Science subject table, look down the Graduate Prospects column',
                       {'entities': [(14, 30, 'Department_name')]}),
                      (
                      "Computer Science students stand a pretty good chance of being professionally employed, or in further study, within six months of leaving uni. And that chance is strengthened if you go to one of the UK's best unis for the subject",
                      {'entities': [(0, 16, 'Department_name')]}),
                      (
                      'Computer science departments at typically benefit from having one of the more culturally diverse cohorts at their respective unis.',
                      {'entities': [(0, 16, 'Department_name')]}),
                      ('According to HESA data almost 20,000 computer science students come from overseas',
                       {'entities': [(37, 54, 'Department_name')]}),
                      (
                      'Computers have gone global, and it would be silly for Computer Science education providers to not reflect this fact',
                      {'entities': [(54, 70, 'Department_name')]}),
                      (
                      'A number of universities offer four-year undergraduate or integrated masters degrees (MSci) in computer science. Many also offer an opportunity to work in industry for a year or study abroad as part of the degree',
                      {'entities': [(95, 111, 'Department_name')]}),
                      (
                      'Computer graphics is the study of digital visual contents and involves the synthesis and manipulation of image data. The study is connected to many other fields in computer science, including computer vision, image processing, and computational geometry, and is heavily applied in the fields of special effects and video games',
                      {'entities': [(164, 180, 'Department_name')]}),
                      (
                      'Conferences are important events for computer science research. During these conferences, researchers from the public and private sectors present their recent work and meet',
                      {'entities': [(36, 53, 'Department_name')]}),
                      (
                      'A number of universities offer four-year undergraduate or integrated masters degrees (MSci) in computer science. Many also offer an opportunity to work in industry for a year or study abroad as part of the degree',
                      {'entities': [(95, 111, 'Department_name')]}),
                      (
                      'To get on to a computer science related degree you will usually require at least two A levels or equivalent.  Entry requirements range from CDD to AAA, with the universities and colleges most commonly asking for BBC',
                      {'entities': [(15, 31, 'Department_name')]}),
                      (
                      'In addition to the different A level requirements above, you will also need at least five GCSEs (A-C) including science, English, and maths. Some universities require a maths GCSE for computer science degrees',
                      {'entities': [(184, 200, 'Department_name')]}),
                      (
                      'Computer science is the study of processes that interact with data and that can be represented as data in the form of programs. It enables the use of algorithms to manipulate, store, and communicate digital information.',
                      {'entities': [(0, 16, 'Department_name')]}),
                      (
                      'Software engineering is the systematic application of engineering approaches to the development of software.',
                      {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'Modern, generally accepted best-practices for software engineering have been collected by the ISO/IEC JTC 1/SC 7 subcommittee and published as the Software Engineering Body of Knowledge (SWEBOK)',
                      {'entities': [(46, 66, 'Department_name')]}),
                      ('The origins of the term "software engineering" have been attributed to various sources.',
                       {'entities': [(25, 45, 'Department_name')]}),
                      (
                      'The term "software engineering" appeared in a list of services offered by companies in the June 1965 issue of COMPUTERS and AUTOMATION and was used more formally in the August 1966 issue of Communications of the ACM (Volume 9, number 8)',
                      {'entities': [(10, 30, 'Department_name')]}),
                      (
                      'ACM membership� by the ACM President Anthony A. Oettinger;,[8] it is also associated with the title of a NATO conference in 1968 by Professor Friedrich L. Bauer, the first conference on software engineering',
                      {'entities': [(186, 206, 'Department_name')]}),
                      (
                      'Independently, Margaret Hamilton named the discipline "software engineering" during the Apollo missions to give what they were doing legitimacy',
                      {'entities': [(55, 75, 'Department_name')]}),
                      (
                      'At the time there was perceived to be a "software crisis".[11][12][13] The 40th International Conference on Software Engineering (ICSE 2018) celebrates 50 years',
                      {'entities': [(108, 128, 'Department_name')]}),
                      (
                      'Modern, generally accepted best-practices for software engineering have been collected by the ISO/IEC JTC 1/SC 7 subcommittee and published as the Software Engineering Body of Knowledge (SWEBOK)',
                      {'entities': [(46, 66, 'Department_name')]}),
                      (
                      'Electrical engineering is an engineering discipline concerned with the study, design and application of equipment, devices and systems which use electricity, electronics, and electromagnetism',
                      {'entities': [(0, 22, 'Department_name')]}),
                      (
                      'However, the design of complex software systems is often the domain of software engineering, which is usually considered a separate discipline',
                      {'entities': [(71, 91, 'Department_name')]}),
                      ('Jalote, Pankaj (31 January 2006). An Integrated Approach to Software Engineering',
                       {'entities': [(60, 80, 'Department_name')]}),
                      (
                      'Software engineering is an engineering branch associated with development of software product using well-defined scientific principles, methods and procedures',
                      {'entities': [(0, 20, 'Department_name')]}),
                      ('Let us first understand what software engineering stands for',
                       {'entities': [(29, 49, 'Department_name')]}),
                      (
                      'Software engineering is an engineering branch associated with development of software product using well-defined scientific principles, methods and procedures.',
                      {'entities': [(0, 20, 'Department_name')]}),
                      ('The outcome of software engineering is an efficient and reliable software product',
                       {'entities': [(15, 35, 'Department_name')]}),
                      (
                      'Software engineering is the establishment and use of sound engineering principles in order to obtain economically software that is reliable and work efficiently on real machines.',
                      {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'The process of developing a software product using software engineering principles and methods is referred to as software evolution',
                      {'entities': [(51, 71, 'Department_name')]}),
                      (
                      'There are many methods proposed and are in work today, but we need to see where in the software engineering these paradigms stand',
                      {'entities': [(87, 107, 'Department_name')]}),
                      (
                      'This Paradigm is known as software engineering paradigms where all the engineering concepts pertaining to the development of software are applied. It includes various researches and requirement gathering which helps the software product to build',
                      {'entities': [(26, 46, 'Department_name')]}),
                      (
                      'The need of software engineering arises because of higher rate of change in user requirements and environment on which the software is working',
                      {'entities': [(12, 32, 'Department_name')]}),
                      (
                      'The always growing and adapting nature of software hugely depends upon the environment in which user works. If the nature of software is always changing, new enhancements need to be done in the existing one. This is where software engineering plays a good role',
                      {'entities': [(222, 242, 'Department_name')]}),
                      (
                      'In short, Software engineering is a branch of computer science, which uses well-defined engineering concepts required to produce efficient, durable, scalable, in-budget and on-time software products',
                      {'entities': [(10, 30, 'Department_name')]}),
                      (
                      'Software Development Life Cycle, SDLC for short, is a well-defined, structured sequence of stages in software engineering to develop the intended software product',
                      {'entities': [(101, 121, 'Department_name')]}),
                      (
                      'Software engineering is defined as a process of analyzing user requirements and then designing, building, and testing software application which will satisfy those requirements',
                      {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'IEEE, in its standard 610.12-1990, defines software engineering as the application of a systematic, disciplined, which is a computable approach for the development, operation, and maintenance of software.',
                      {'entities': [(43, 63, 'Department_name')]}),
                      (
                      "Boehm defines software engineering, which involves, 'the practical application of scientific knowledge to the creative design and building of computer programs. It also includes associated documentation needed for developing, operating, and maintaining them",
                      {'entities': [(14, 34, 'Department_name')]}),
                      (
                      'Solution was to the problem was transforming unorganized coding effort into a software engineering discipline',
                      {'entities': [(78, 98, 'Department_name')]}),
                      ('The late 1970s saw the widespread uses of software engineering principles',
                       {'entities': [(42, 62, 'Department_name')]}),
                      (
                      'Whenever the software process was based on scientific and engineering, it is easy to re-create new software with the help of software engineering',
                      {'entities': [(125, 145, 'Department_name')]}),
                      (
                      'In this sector, software engineering helps you in resource estimation and cost control. Computing system must be developed, and data should be maintained regularly within a given budget',
                      {'entities': [(16, 36, 'Department_name')]}),
                      (
                      'Software engineering is labor-intensive work which demands both technical and managerial control. Therefore, it is widely used in management science',
                      {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'Most software is a component of a much larger system. For example, the software in an Industry monitoring system or the flight software on an airplane. Software engineering methods should be applied to the study of this type of systems',
                      {'entities': [(152, 172, 'Department_name')]}),
                      (
                      'Software engineering is a process of analyzing user requirements and then designing, building, and testing software application which will satisfy that requirements',
                      {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'Important reasons for using software engineering are: 1) Large software, 2) Scalability 3) Adaptability 4) Cost and 5) Dynamic Nature',
                      {'entities': [(28, 48, 'Department_name')]}),
                      ('The late 1970s saw the widespread uses of software engineering principles',
                       {'entities': [(42, 62, 'Department_name')]}),
                      (
                      'Increased market demands for fast turnaround time is the biggest challenges of software engineering field',
                      {'entities': [(79, 106, 'Department_name')]}),
                      (
                      'A backlash against the overemphasis of processes in software development resulted in a group of software engineering consultants publishing the Manifesto for Agile Software Development',
                      {'entities': [(96, 116, 'Department_name')]}),
                      (
                      'In this millennium, researchers in software engineering have performed numerous studies linking software metrics to post-release failures',
                      {'entities': [(34, 55, 'Department_name')]}),
                      (
                      'V&V tasks should be performed by a team of senior software personnel lead by a member of the software engineering team',
                      {'entities': [(93, 113, 'Department_name')]}),
                      (
                      'The software engineering literature has stressed the importance of software development processes and their influence on product quality for decades [2,4]',
                      {'entities': [(4, 25, 'Department_name')]}),
                      ('A. Bener, ... E. Kocaguneli, in Perspectives on Data Science for Software Engineering, 2016',
                       {'entities': [(65, 85, 'Department_name')]}),
                      (
                      'Software engineering is more than just programming. It includes computer science, project management, engineering and other spheres. This lesson will discuss the different processes involved in it and the common methods used in developing software',
                      {'entities': [(0, 20, 'Department_name')]}),
                      ('You just applied the principles of software engineering to your business',
                       {'entities': [(35, 55, 'Department_name')]}),
                      (
                      "Software engineering essentially follows the same steps. The only difference is that you are running a 'software' business instead of a card business",
                      {'entities': [(0, 20, 'Department_name')]}),
                      ('The end result of software engineering is a streamlined and reliable software product',
                       {'entities': [(18, 38, 'Department_name')]}),
                      ("Let's take a look at each of the steps involved in a typical software engineering process",
                       {'entities': [(61, 81, 'Department_name')]}),
                      (
                      'Graduates of University of Maryland�s Computer Science Department are lifetime learners; they are able to adapt quickly with this challenging field',
                      {'entities': [(38, 54, 'Department_name')]}),
                      (
                      'In a nutshell, computer science degrees deal with the theoretical foundations of information and computation, taking a scientific and practical approach to computation and its applications',
                      {'entities': [(15, 32, 'Department_name')]}),
                      (
                      'Computer science is considered by many of its practitioners to be a foundational science - one which makes other knowledge and achievements possible',
                      {'entities': [(0, 16, 'Department_name')]}),
                      (
                      'The study of computer science involves systematically studying methodical processes (such as algorithms) in order to aid the acquisition, representation, processing, storage, communication of, and access to information',
                      {'entities': [(13, 29, 'Department_name')]}),
                      (
                      'This is done by analyzing the feasibility, structure, expression and mechanization of these processes and how they relate to this information. In computer science, the term �information� refers usually to information which is encoded in bits and bytes in computer memory',
                      {'entities': [(146, 162, 'Department_name')]}),
                      ('You may also find the term computer science', {'entities': [(27, 43, 'Department_name')]}),
                      (
                      'used to refer to information technology (IT) degrees, although many institutions now distinguish between the two (exactly how and where they draw this line varies)',
                      {'entities': [(17, 39, 'Department_name')]}),
                      (
                      'The QS World University Rankings by Subject includes a ranking of the world�s top universities for computer science',
                      {'entities': [(99, 115, 'Department_name')]}),
                      (
                      'Entry requirements for computer science degrees usually emphasize further mathematics, with some institutions asking for a background in physics',
                      {'entities': [(23, 39, 'Department_name')]}),
                      (
                      'Some institutions offer joint courses, in which computer science is studied alongside subjects such as mathematics, engineering and computing',
                      {'entities': [(48, 64, 'Department_name')]}),
                      (
                      'If you like solving problems and have a talent for mathematics and logical thinking, a degree in computer science could be the start of a rewarding career',
                      {'entities': [(97, 113, 'Department_name')]}),
                      (
                      'Computer science degrees are structured in an incremental way, starting by giving students an overview of the basic principles',
                      {'entities': [(0, 16, 'Department_name')]}),
                      (
                      'There is also likely to be some teaching about where modern computer science fits into society, either the history of the discipline, or a module on business or enterprise in the context of computer science',
                      {'entities': [(60, 76, 'Department_name')]}),
                      (
                      'If you want to study computer science at university you must be creative, diligent and strong in maths',
                      {'entities': [(21, 37, 'Department_name')]}),
                      (
                      'Most universities look for top marks in subjects like IT, computing, physics or further maths from applicants',
                      {'entities': [(53, 56, 'Department_name')]}),
                      (
                      'Therfore are many reasons that computer science is so popular, including exceptional job security, uncommonly high starting salaries, and diverse job opportunities across industries',
                      {'entities': [(31, 47, 'Department_name')]}),
                      (
                      'Due to the distinction between computers and computing, some of the research groups refer to computing or datalogy. The French refer to computer science as the term informatique',
                      {'entities': [(136, 152, 'Department_name')]}),
                      (
                      'Informatics is also distinct from computer science, which encompasses the study of logic and low-level computing issues',
                      {'entities': [(34, 50, 'Department_name')]}),
                      (
                      'Universities may confer degrees of ICS and CIS, not to be confused with a more specific Bachelor of Computer Science or respective graduate',
                      {'entities': [(100, 116, 'Department_name')]}),
                      (
                      'The QS World University Rankings is one of the most widely recognised and distinguished university comparisons. They ranked the top 10 universities for computer science and information systems in 2015',
                      {'entities': [(152, 168, 'Department_name')]}),
                      (
                      'Due the nature of this field, many topics are also shared with computer science and information systems',
                      {'entities': [(62, 79, 'Department_name')]}),
                      ('The discipline of Information and Computer Science spans a vast range of areas from basic',
                       {'entities': [(34, 50, 'Department_name')]}),
                      (
                      'computer science theory (algorithms and computational logic) to in depth analysis of data manipulation and use within technology',
                      {'entities': [(0, 16, 'Department_name')]}),
                      (
                      'and it�s predicted in the US that in the next decade there will be more than one million jobs in the technology sector than computer science graduates to fill them',
                      {'entities': [(124, 140, 'Department_name')]}),
                      (
                      'f you see yourself designing and creating software systems, then computer science might be the right course of study for you. If you are thinking of becoming a manager or administrator to a technical enterprise',
                      {'entities': [(65, 81, 'Department_name')]}),
                      (
                      'Computer science is a dynamic and rapidly growing area that has become an integral part of the world that we live in today. Having a degree in this field will provide you with a deep understanding of theories and emerging technologies',
                      {'entities': [(0, 16, 'Department_name')]}),
                      (
                      'you may not become a billionaire in computer science � there are only so many Steves Jobs and Bill Gates in the world � but, since it�s specialized knowledge and challenging skills, salaries tend to be solidly high.',
                      {'entities': [(36, 52, 'Department_name')]}),
                      (
                      'Before entering an information technology program, prospective students will wonder if a computer science degree is worth it',
                      {'entities': [(19, 41, 'Department_name')]}),
                      ('Over the last twenty years, the field of computer science has grown exponentially',
                       {'entities': [(41, 57, 'Department_name')]}),
                      (
                      'The median wage for those in the computer science industry is $86,320 annually, according to the Bureau of Labor Statistics. Jobs in the industry are expected to experience a growth of at least 14% over the next decade with as many as 557,000 new jobs being created',
                      {'entities': [(33, 49, 'Department_name')]}),
                      ('A computer science degree is worth it since technology is consistently evolving',
                       {'entities': [(2, 18, 'Department_name')]}),
                      (
                      'New specializations are always opening in the field of computer science as new technological advancements are made',
                      {'entities': [(55, 71, 'Department_name')]}),
                      ('Potential job opportunities for computer science degree holders include',
                       {'entities': [(31, 49, 'Department_name')]}),
                      (
                      'Several jobs in the computer science field will have a master�s degree requirement. For these jobs, median salaries will be upwards of $115,000 per year',
                      {'entities': [(19, 36, 'Department_name')]}),
                      ('It is possible to launch a career in the field of computer science with an associate�s degree',
                       {'entities': [(50, 66, 'Department_name')]}),
                      (
                      'Associate degree programs will teach students both hard and soft skills needed for the IT workforce',
                      {'entities': [(87, 89, 'Department_name')]}),
                      (
                      'n some incidences, an employer may not even ask for a college degree, but instead, look exclusively at past job experience and any certifications earned related to computer science',
                      {'entities': [(164, 180, 'Department_name')]}),
                      (
                      'Computer science degree programs are being offered more and more online. Online degrees are widely accepted as long as they are earned from an accredited college or university',
                      {'entities': [(0, 16, 'Department_name')]}),
                      (
                      'Any school chosen by the prospective computer science student should have the proper accreditation in order to successfully secure a position post-graduation',
                      {'entities': [(37, 53, 'Department_name')]}),
                      (
                      ' An accredited computer science degree online will have the same value as a traditional program. Non-accredited programs may disqualify the applicant from a position',
                      {'entities': [(15, 31, 'Department_name')]}),
                      ('The following are frequently asked questions regarding computer science accreditation',
                       {'entities': [(55, 71, 'Department_name')]}),
                      (
                      'Online programs have a separate accreditation process than traditional computer science and engineering types',
                      {'entities': [(71, 87, 'Department_name')]}),
                      (
                      'Many employers are now requiring new hires in the field of computer science to have graduated from ABET-accredited program',
                      {'entities': [(59, 75, 'Department_name')]}),
                      (
                      'The STEM field is looking for a global standard to determine if college graduates have the technical prowess to succeed in the industry. ABET programs confirm job readiness for computer science students',
                      {'entities': [(177, 193, 'Department_name')]}),
                      (
                      ' Along with computer science programs, ABET accredits engineering and applied/natural science programs',
                      {'entities': [(12, 29, 'Department_name')]}),
                      (
                      'Computer science degree requirements will also include general education classes in math, history, philosophy, writing, and more',
                      {'entities': [(0, 16, 'Department_name')]}),
                      (
                      'Students should look at specialization options as well as accreditation to narrow down the best undergraduate computer science schools',
                      {'entities': [(110, 126, 'Department_name')]}),
                      (
                      'Instead of a general overview, the master degree program will delve into advanced computer science topics',
                      {'entities': [(82, 98, 'Department_name')]}),
                      (
                      'A technology firm could choose to send employees for a computer science degree online�allowing the worker to take courses in the evenings and weekends',
                      {'entities': [(55, 71, 'Department_name')]}),
                      (
                      'Types of computer science degrees at the graduate level include database systems, homeland security',
                      {'entities': [(9, 25, 'Department_name')]}),
                      (
                      'Accelerated computer science degree programs may be finished in one year or less, but have a larger per semester course load',
                      {'entities': [(12, 28, 'Department_name')]}),
                      (
                      'Computer science degree types include traditional, hybrid, and online. Traditional degree tracks require that students attend courses exclusively on campus',
                      {'entities': [(0, 16, 'Department_name')]}),
                      (
                      ' Online computer science degrees are 100 percent online. In some cases, the student may only have a weekend campus visit requirement once or twice a year',
                      {'entities': [(8, 24, 'Department_name')]}),
                      (
                      'Most aspects of computer science can be learned anywhere, which means that there�s nothing inherently better about a traditional residential program over an online program',
                      {'entities': [(16, 32, 'Department_name')]}),
                      (
                      'A computer science certificate online program may have pre-requisites before a person can complete it',
                      {'entities': [(2, 18, 'Department_name')]}),
                      (
                      " Considering these factors, it's no wonder that you consider studying Computer Science or Information Technology degree",
                      {'entities': [(70, 86, 'Department_name')]}),
                      (
                      'Choosing your studies can be a tough choice, with this guide we hope to help you decide if you want to study Computer Science',
                      {'entities': [(109, 125, 'Department_name')]}),
                      (
                      'Although there is some overlap. When you study Computer Science you will learn to design and develop computer programs, applications and software',
                      {'entities': [(47, 63, 'Department_name')]}),
                      (
                      'Being able to find a job after graduating is something a lot of people are struggling with. Good news, this is not the case for people with a degree in Computer Science',
                      {'entities': [(152, 168, 'Department_name')]}),
                      (
                      'Computer engineering (CE) is a branch of engineering that integrates several fields of required to develop computer hardware and software',
                      {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'In many institutions of higher learning, computer engineering students are allowed to choose areas of in-depth study in their junior and senior year because the full breadth of knowledge used in the design and application of computers is beyond the scope of an undergraduate degree',
                      {'entities': [(41, 62, 'Department_name')]}),
                      (
                      'The first computer engineering degree program in the United States was established in 1971 at Case Western Reserve University in Cleveland, Ohio',
                      {'entities': [(10, 30, 'Department_name')]}),
                      (
                      "some tertiary institutions around the world offer a bachelor's degree generally called computer engineering",
                      {'entities': [(87, 108, 'Department_name')]}),
                      (
                      'Both computer engineering and electronic engineering programs include analog and digital circuit design in their curriculum',
                      {'entities': [(5, 25, 'Department_name')]}),
                      ("Most entry-level computer engineering jobs require at least a bachelor's degree in computer",
                       {'entities': [(17, 37, 'Department_name')]}),
                      ('computer engineering (ECE) and has been divided into many subcategories',
                       {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'Computer Engineering is generally practiced within larger product development firms, and such practice may not be subject to licensing',
                      {'entities': [(0, 21, 'Department_name')]}),
                      (
                      ' offered a Principles and Practice of Engineering Examination for Computer Engineering[33] in 2003',
                      {'entities': [(65, 86, 'Department_name')]}),
                      ('There are many specialty areas in the field of computer engineering',
                       {'entities': [(47, 67, 'Department_name')]}),
                      (
                      'This specialty of computer engineering requires adequate knowledge of electronics and electrical systems',
                      {'entities': [(18, 38, 'Department_name')]}),
                      (
                      'computer embedded computer engineering specializations include system-on-chip design, architecture of edge computing and the Internet of things',
                      {'entities': [(18, 38, 'Department_name')]}),
                      ('Media related to Computer engineering at Wikimedia Commons',
                       {'entities': [(17, 37, 'Department_name')]}),
                      ('IT is the use of computers to store, retrieve, transmit, and manipulate data[1] or information',
                       {'entities': [(0, 2, 'Department_name')]}),
                      (
                      'IT is typically used within the context of business operations as opposed to personal or entertainment technologies',
                      {'entities': [(0, 2, 'Department_name')]}),
                      ('IT is considered to be a subset of information and communications technology (ICT)',
                       {'entities': [(0, 2, 'Department_name')]}),
                      ('We shall call it IT', {'entities': [(17, 19, 'Department_name')]}), (
                      'is possible to distinguish four distinct phases of IT development',
                      {'entities': [(51, 54, 'Department_name')]}),
                      ('As the IT industry evolved from the mid-20th', {'entities': [(7, 9, 'Department_name')]}),
                      ('can be included in the IT domain', {'entities': [(23, 25, 'Department_name')]}),
                      ('IT architectures have evolved to include virtualization and cloud computing',
                       {'entities': [(0, 2, 'Department_name')]}),
                      ('Clouds may be distributed across locations and shared with other IT users',
                       {'entities': [(65, 67, 'Department_name')]}),
                      ('IT teams depend on a wide range of specialized information.',
                       {'entities': [(0, 2, 'Department_name')]}),
                      ('vendor support personnel augment the IT team', {'entities': [(37, 39, 'Department_name')]}),
                      ('Information Technology includes several layers of physical equipment',
                       {'entities': [(0, 22, 'Department_name')]}),
                      ('Information Technology teams depend on a wide range of specialized',
                       {'entities': [(0, 22, 'Department_name')]}),
                      ('Information technology is the use of any computers, storage',
                       {'entities': [(0, 22, 'Department_name')]}),
                      ('The term information technology was coined by the Harvard Business Review',
                       {'entities': [(9, 31, 'Department_name')]}),
                      (
                      'For many people, information technology is basically synonymous with the guys and gals you call when you need help with a computer issue',
                      {'entities': [(17, 39, 'Department_name')]}),
                      (
                      'While that view of information technology isn�t totally wrong, it drastically understates the scope of this critical career field',
                      {'entities': [(19, 42, 'Department_name')]}),
                      ('If you�re looking to get a better handle on what information technology is',
                       {'entities': [(49, 71, 'Department_name')]}),
                      ("The most basic information technology definition is that it's the application",
                       {'entities': [(15, 37, 'Department_name')]}),
                      ('There are three primary pillars of responsibility for an IT department',
                       {'entities': [(57, 59, 'Department_name')]}),
                      ('No matter the role, a member of an IT department works',
                       {'entities': [(35, 38, 'Department_name')]}),
                      ('computer and information technology occupations is projected to grow',
                       {'entities': [(13, 35, 'Department_name')]}),
                      ('those in information technology need to have a level of empathy',
                       {'entities': [(9, 31, 'Department_name')]}),
                      (
                      'Now that you�ve got a better handle on the basics of what information technology is and the important nature of the field',
                      {'entities': [(58, 80, 'Department_name')]}),
                      ('The information technology profession is extremely diverse',
                       {'entities': [(4, 26, 'Department_name')]}),
                      ('This person examines and changes IT functions to best support the business.',
                       {'entities': [(33, 35, 'Department_name')]}),
                      ('What is changing today about information technology roles?',
                       {'entities': [(29, 51, 'Department_name')]}),
                      ("Today's IT professionals need to be quicker to respond to new technologies",
                       {'entities': [(8, 10, 'Department_name')]}),
                      ('Hii sir!, am finding for the IT technician to help me some things can you help me',
                       {'entities': [(29, 31, 'Department_name')]}),
                      (
                      "I'm doing my research for how information technology has developed and contributed to shaping our society today and this article helped a lot",
                      {'entities': [(30, 53, 'Department_name')]}),
                      ('Sir, please tell me the definition of Information Technology',
                       {'entities': [(38, 60, 'Department_name')]}),
                      ('Now a days, what is Information Technology', {'entities': [(20, 42, 'Department_name')]}),
                      ('Programming and Information Technology should understand the objectives of the business',
                       {'entities': [(16, 38, 'Department_name')]}),
                      ('Information Technology is devising more user-friendly and supporting system',
                       {'entities': [(0, 22, 'Department_name')]}),
                      ('one day become a chief officer of Information Technology',
                       {'entities': [(34, 56, 'Department_name')]}),
                      ('am in Tanzania i need to know much about IT', {'entities': [(40, 43, 'Department_name')]}),
                      (
                      'i am in Kenya wanted to learner about Information Technology hoping that you will assist me thank you',
                      {'entities': [(38, 60, 'Department_name')]}),
                      ('I want to know what is infromation technology', {'entities': [(23, 46, 'Department_name')]}),
                      ('our new technics, that is information technology', {'entities': [(26, 48, 'Department_name')]}),
                      ('Thank you Margaret, because IT is my career', {'entities': [(28, 30, 'Department_name')]}),
                      ('CS is the study of processes that interact with data',
                       {'entities': [(0, 3, 'Department_name')]}),
                      ('A CS studies the theory of computation and the design',
                       {'entities': [(2, 4, 'Department_name')]}),
                      ('the term CS appears in a 1959 article in Communications of the ACM',
                       {'entities': [(8, 11, 'Department_name')]}),
                      ('Graduate School in CS analogous to the creation of Harvard Business School in 1921',
                       {'entities': [(19, 22, 'Department_name')]}),
                      ('funding aspects of CS tend to depend on whether a department.',
                       {'entities': [(19, 21, 'Department_name')]}),
                      ('which treats CS as a branch of mathematics.', {'entities': [(12, 15, 'Department_name')]}),
                      ('CS focuses on methods involved in design', {'entities': [(0, 2, 'Department_name')]}),
                      ('As a discipline, CS spans a range of topics from theoretical studies of algorithms',
                       {'entities': [(17, 19, 'Department_name')]}),
                      ('Theoretical CS is mathematical and abstract in spirit',
                       {'entities': [(12, 15, 'Department_name')]}),
                      ('the fundamental question underlying CS', {'entities': [(36, 38, 'Department_name')]}),
                      ('It falls within the discipline of CS both depending on and affecting',
                       {'entities': [(34, 36, 'Department_name')]}),
                      ('the application of a fairly broad variety of theoretical CS fundamentals',
                       {'entities': [(57, 59, 'Department_name')]}),
                      (
                      'The study is connected to many other fields in cs', {'entities': [(47, 49, 'Department_name')]}),
                      ('The philosopher of computing Bill Rapaport noted three Great Insights of cs',
                       {'entities': [(73, 75, 'Department_name')]}),
                      ('Further information List of cs conferences', {'entities': [(28, 31, 'Department_name')]}),
                      ('Unlike in most other academic fields, in cs', {'entities': [(41, 43, 'Department_name')]}),
                      ('cs to A level students', {'entities': [(0, 2, 'Department_name')]}),
                      ('and South Korea have included cs in their national secondary education curricula',
                       {'entities': [(30, 32, 'Department_name')]}),
                      ('states have adopted significant education standards for high school cs',
                       {'entities': [(68, 70, 'Department_name')]}),
                      ('In many countries, there is a significant gender gap in cs education',
                       {'entities': [(56, 58, 'Department_name')]}),
                      ('See the entry cs on Wikiquote for the history of this quotation',
                       {'entities': [(14, 16, 'Department_name')]}),
                      ('The problems that cs encounter range from the abstract',
                       {'entities': [(18, 20, 'Department_name')]}),
                      ('Graduates of University of Maryland�s cs Department',
                       {'entities': [(38, 41, 'Department_name')]}),
                      (
                      'Accounting & Finance is a highly specialised degree, preparing the graduate as having expertise',
                      {'entities': [(0, 21, 'Department_name')]}),
                      ('opportunities in accounting and finance than many other areas of study',
                       {'entities': [(17, 39, 'Department_name')]}),
                      ('Accounting & Finance program is aimed at giving students a solid foundation',
                       {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'in accounting and finance, rounded out with the all-important interpersonal, computer, and business communication skills',
                      {'entities': [(2, 25, 'Department_name')]}), (
                      'Accounting & Finance is a four-year degree program and consists of 130-136 credit hours of study',
                      {'entities': [(0, 20, 'Department_name')]}),
                      ('Accounting and Finance  was are the an ACCA accredited program',
                       {'entities': [(0, 22, 'Department_name')]}),
                      ('Accounting And Finance is an accredited program googing on in this session',
                       {'entities': [(0, 23, 'Department_name')]}),
                      ('The course is a blend of theory and practice of accounting and finance',
                       {'entities': [(48, 70, 'Department_name')]}),
                      ('Accounting and Finance program consist of four or five-course units per semester',
                       {'entities': [(0, 22, 'Department_name')]}),
                      (
                      'Accounting & Finance are the most significant and critical areas in the system of free enterprise',
                      {'entities': [(0, 21, 'Department_name')]}),
                      (
                      'The BS Accounting & Finance program is designed to prepare students to meet the challenges posed by this complex',
                      {'entities': [(7, 27, 'Department_name')]}),
                      (
                      'BS Accounting & Finance is tailored to first impart a broad-based education in the fundamentals of business',
                      {'entities': [(3, 24, 'Department_name')]}),
                      ('Accounting & Finance degree, a student must have', {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'A major in Accounting and Finance (ACF) in B.Sc. (Hons) provides students with a basis from which to continue',
                      {'entities': [(11, 33, 'Department_name')]}),
                      (
                      'At this time, students can follow a set of pre-identified courses to simultaneously complete professional certifications with their B.Sc. (Hons) Degree in Accounting and Finance',
                      {'entities': [(155, 177, 'Department_name')]}),
                      ('At the heart of accounting and financial  is the system known as double entry',
                       {'entities': [(16, 40, 'Department_name')]}),
                      (
                      'The bachelor degree program in Accounting and Finance prepares students for entry-level positions',
                      {'entities': [(31, 53, 'Department_name')]}),
                      ('The degree provides a strong foundation for a successful career in accounting and finance',
                       {'entities': [(67, 89, 'Department_name')]}),
                      (
                      'To make students able to understand and develop the skills to grasp broad range of accounting and finance techniques and concepts',
                      {'entities': [(83, 105, 'Department_name')]}),
                      (
                      'To provide the knowledge and skills to students for using computer technology in accounting and finance for the purpose of improving decision making in an organization setting',
                      {'entities': [(81, 103, 'Department_name')]}),
                      (
                      'To provide an opportunity for students to evaluate problems and innovations in accounting and finance with effects on managerial decision making',
                      {'entities': [(79, 101, 'Department_name')]}), (
                      'To make them able to apply integrated techniques of accounting and finance in evaluating the costs and benefits of strategic investments',
                      {'entities': [(52, 74, 'Department_name')]}), (
                      'To develop the understanding about ethical issues in Accounting And Finance',
                      {'entities': [(53, 76, 'Department_name')]}), (
                      'To mentor students to exploit newly created opportunities in Accounting And Finance profession',
                      {'entities': [(61, 83, 'Department_name')]}), (
                      'Students are required to complete a Project/ Internship Report in the final semester of their BS in Accounting and Finance program',
                      {'entities': [(100, 122, 'Department_name')]}),
                      (
                      'Accounting and Finance intends to prepare students in professional accounting and financial management',
                      {'entities': [(0, 22, 'Department_name')]}),
                      ('This programme covers the major tools and theories of ACCOUNTING & FINANCE',
                       {'entities': [(54, 75, 'Department_name')]}),
                      ('The BSc ACCOUNTING & FINANCE programme is primarily designed for students who are interested',
                       {'entities': [(8, 28, 'Department_name')]}),
                      ('then ACCOUNTING & FINANCE is the perfect career path for you',
                       {'entities': [(5, 25, 'Department_name')]}),
                      (
                      'Tri-city is the residence of many companies offering international ACCOUNTING & FINANCE services',
                      {'entities': [(67, 87, 'Department_name')]}),
                      (
                      'Develop specialist ACCOUNTING & FINANCE skills, and learn to apply them in an organisational context',
                      {'entities': [(19, 39, 'Department_name')]}),
                      ('Finance & Accounting Level are Undergraduate program',
                       {'entities': [(0, 20, 'Department_name')]}),
                      ('Our specialised ACCOUNTING & FINANCE degree aims to improve employability',
                       {'entities': [(16, 36, 'Department_name')]}),
                      (
                      'Lincoln�s ACCOUNTING & FINANCE degree aims to equip students with vocationally relevant and academically rigorous education in a programmer',
                      {'entities': [(10, 31, 'Department_name')]}),
                      (
                      'Students are required to complete 46 courses and a 6 credit hours of ?nal year project ACCOUNTING AND FINANCE',
                      {'entities': [(87, 110, 'Department_name')]}),
                      (
                      'This programme covers the major tools and differnt universites doing that theories of ACCOUNTING AND FINANCE is impotrant in universities',
                      {'entities': [(86, 108, 'Department_name')]}),
                      ('Our main purpose is specialised ACCOUNTING AND FINANCE degree aims do that about it',
                       {'entities': [(32, 54, 'Department_name')]}),
                      (
                      'To mentor students is get and many of the energy to exploit newly created opportunities in ACCOUNTING AND FINANCE  profession',
                      {'entities': [(91, 113, 'Department_name')]}),
                      (
                      'ACCOUNTING AND FINANCE make them able to apply integrated techniques of  in different universities',
                      {'entities': [(0, 22, 'Department_name')]}),
                      (
                      'A major in ACCOUNTING AND FINANCE (ACF) in B.Sc. (Hons) provides students with a basis from which the sytem that not really the gone',
                      {'entities': [(11, 33, 'Department_name')]}),
                      ('COMPUTER SCIENCES design and analyze algorithms to solve the problems',
                       {'entities': [(0, 17, 'Department_name')]}),
                      (
                      'The course material ranges from entry-level subjects to specialised topics. Hold a degree outside of COMPUTER SCIENCES',
                      {'entities': [(101, 118, 'Department_name')]}),
                      ('Students who earn a BA in COMPUTER SCIENCES must complete at least five courses',
                       {'entities': [(25, 43, 'Department_name')]}),
                      (
                      'Students majoring in COMPUTER SCIENCES may not earn a second major or a minor in business analytics and information systems',
                      {'entities': [(21, 38, 'Department_name')]}),
                      (
                      'Welcome to the Electrical Engineering Department (EED) at Information Technology University (ITU), Lahore',
                      {'entities': [(15, 37, 'Department_name')]}),
                      (
                      'The Department of Electrical Engineering has a carefully designed curriculum which offers a wide range of knowledge',
                      {'entities': [(18, 40, 'Department_name')]}),
                      (
                      'highlight that both Higher Education Commission (HEC) and Pakistan Engineering Council (PEC) recognize BS in electrical engineering program at ITU',
                      {'entities': [(109, 131, 'Department_name')]}),
                      (
                      'The Program Educational Objectives (PEO) of the BS in Electrical Engineering program are as under',
                      {'entities': [(54, 76, 'Department_name')]}),
                      (
                      'To produce creative graduates with core electrical engineering concepts to embark on real-world challenges',
                      {'entities': [(40, 62, 'Department_name')]}),
                      (
                      'The mission of School of Electrical Engineering is to provide graduates with a strong and stable foundation',
                      {'entities': [(25, 48, 'Department_name')]}),
                      (
                      'To inculcate graduates with technical competence through advanced and comprehensive knowledge of the practical aspect of electrical engineering, including analytical and design skills and of the technical tools to meet the engineering requirements',
                      {'entities': [(120, 143, 'Department_name')]}),
                      (
                      'To provide an undergraduate education that will further enable qualified students to pursue Graduate/Higher studies in electrical engineering and related fields',
                      {'entities': [(119, 141, 'Department_name')]}),
                      ('This versatile degree opens careers in different areas of electrical engineering',
                       {'entities': [(58, 80, 'Department_name')]}),
                      ('For the award of BS Electrical Engineering degree, a student must have',
                       {'entities': [(20, 43, 'Department_name')]}),
                      (
                      'engineering specialization Electrical Engineering to the solution of complex engineering problems',
                      {'entities': [(27, 49, 'Department_name')]}),
                      (
                      'An ability to design solutions in the domain of Electrical Engineering for complex engineering problems',
                      {'entities': [(48, 70, 'Department_name')]}),
                      (
                      'Electrical engineering is an engineering discipline concerned with the study, design and application of equipment',
                      {'entities': [(0, 22, 'Department_name')]}),
                      ('Electrical engineering is now divided into a wide range of fields including',
                       {'entities': [(0, 22, 'Department_name')]}),
                      (
                      'The IEC prepares international standards for electrical engineering, developed through consensus',
                      {'entities': [(45, 67, 'Department_name')]}),
                      (
                      'Electrical engineerings work in a very wide range of industries and the skills required are likewise variable',
                      {'entities': [(0, 23, 'Department_name')]}),
                      ('soon to be renamed the Institution of Electrical Engineering',
                       {'entities': [(38, 60, 'Department_name')]}),
                      (
                      "the world's first department of electrical engineering in 1882 and introduced the first degree course",
                      {'entities': [(32, 54, 'Department_name')]}),
                      (
                      'The first electrical engineering degree program in the United States was started at Massachusetts Institute of Technology (MIT) in the physics department',
                      {'entities': [(10, 32, 'Department_name')]}),
                      (
                      'Weinbach at University of Missouri soon followed suit by establishing the electrical engineering department in 1886',
                      {'entities': [(74, 96, 'Department_name')]}),
                      ('started to offer electrical engineering programs to their students all over the world',
                       {'entities': [(17, 39, 'Department_name')]}),
                      ('During these decades use of ELECTRICAL ENGINEERING increased dramatically',
                       {'entities': [(28, 50, 'Department_name')]}),
                      ('ELECTRICAL ENGINEERING has many subdisciplines, the most common of which are listed below',
                       {'entities': [(0, 23, 'Department_name')]}),
                      (
                      'the main aim of ELECTRICAL ENGINEERING may use electronic circuits, digital signal processors, microcontrollers, and programmable logic controllers (PLCs)',
                      {'entities': [(16, 38, 'Department_name')]}),
                      (
                      'ELECTRICAL ENGINEERING involves the design and testing of electronic circuits that use the properties of components such as resistors',
                      {'entities': [(0, 22, 'Department_name')]}),
                      (
                      'In the mid-to-late 1950s, the term radio engineering gradually gave way to the name ELECTRICAL ENGINEERING',
                      {'entities': [(84, 107, 'Department_name')]}),
                      (
                      'The field of ELECTRICAL ENGINEERING involves a significant amount of chemistry and material science and requires the electronic engineer',
                      {'entities': [(13, 35, 'Department_name')]}),
                      (
                      'he most common microelectronic components are semiconductor transistors, although all main ELECTRICAL ENGINEERING',
                      {'entities': [(91, 114, 'Department_name')]}),
                      ('The term mechatronics is typically used to refer to ELECTRICAL ENGINEERING macroscopic system',
                       {'entities': [(52, 74, 'Department_name')]}),
                      ('SOFTWARE ENGINEERING is the process of analyzing user needs and designing, constructing',
                       {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'Furthermore may SOFTWARE ENGINEERING involve the process of analyzing existing software and modifying it to meet current application needs',
                      {'entities': [(16, 36, 'Department_name')]}),
                      (
                      'There must be discipline and control during SOFTWARE ENGINEERING, much like any complex engineering endeavor',
                      {'entities': [(44, 64, 'Department_name')]}),
                      (
                      'SOFTWARE ENGINEERING is a direct sub-field of engineering and has an overlap with computer science and management science',
                      {'entities': [(0, 21, 'Department_name')]}),
                      (
                      'The term SOFTWARE ENGINEERING  appeared in a list of services offered by companies in the June 1965 issue of COMPUTERS.',
                      {'entities': [(9, 29, 'Department_name')]}),
                      (
                      "SOFTWARE ENGINEERING with the Plenary Sessions' keynotes of Frederick Brooks[14] and Margaret Hamilton",
                      {'entities': [(0, 20, 'Department_name')]}),
                      (
                      'Modern, generally accepted best-practices for SOFTWARE ENGINEERING have been collected by the ISO/IEC JTC 1/SC 7 subcommittee and published',
                      {'entities': [(46, 66, 'Department_name')]}),
                      (
                      'INFORMATION TECHNOLOGY system (IT system) is generally an information system, a communications system or, more specifically speaking, a computer system � including all hardware, software and peripheral equipment � operated by a limited group of users.',
                      {'entities': [(0, 22, 'Department_name')]}),
                      (
                      'the new technology does not yet have a single established name. We shall call it INFORMATION TECHNOLOGY (IT).',
                      {'entities': [(80, 103, 'Department_name')]}),
                      (
                      'but INFORMATION TECHNOLOGY also encompasses other information distribution technologies such as television and telephones',
                      {'entities': [(4, 26, 'Department_name')]}),
                      (
                      'in a business context, the INFORMATION TECHNOLOGY Association of America has defined information technology as the study, design',
                      {'entities': [(27, 49, 'Department_name')]}),
                      (
                      'Some of the ethical issues associated with the use of INFORMATION TECHNOLOGY include many terms',
                      {'entities': [(54, 76, 'Department_name')]}),
                      (
                      'On the later more broad application of the term IT, Keary comments in its original application INFORMATION TECHNOLOGY',
                      {'entities': [(48, 50, 'Department_name')]}),
                      (
                      'INFORMATION TECHNOLOGY (IT) is basically synonymous with the guys and gals you call when you need help with a computer issue and many term kept in mind',
                      {'entities': [(0, 23, 'Department_name')]}),
                      (
                      "The most basic INFORMATION TECHNOLOGY definition is that it's the application of technology to solve business or organizational problems on a broad scale and key is to success",
                      {'entities': [(15, 38, 'Department_name')]}),
                      (
                      'COMPUTER ENGINEERING students are allowed to choose areas of in-depth study in their junior and senior years and the intermession',
                      {'entities': [(0, 20, 'Department_name')]}),
                      ('Media related to COMPUTER ENGINEERING at Wikimedia Commons and this is the most important',
                       {'entities': [(16, 37, 'Department_name')]}),
                      (
                      'the most important computer embedded COMPUTER ENGINEERING specializations include system-on-chip design, architecture of edge computing and the Internet of things',
                      {'entities': [(37, 58, 'Department_name')]}),
                      (
                      'This specialty of a many times then different COMPUTER ENGINEERING requires adequate knowledge of electronics and electrical systems',
                      {'entities': [(46, 66, 'Department_name')]}),
                      (
                      'There are many specialty areas in the field of COMPUTER ENGINEERING we have many choices and this is many times',
                      {'entities': [(47, 67, 'Department_name')]}),
                      (
                      'this is offered a Principles and Practice of Engineering Examination for COMPUTER ENGINEERING [33] in 2003 and many times we can do that it',
                      {'entities': [(73, 93, 'Department_name')]}),
                      (
                      'bascially,we can COMPUTER ENGINEERING (ECE) and has been divided into many subcategories as we show many times',
                      {'entities': [(17, 37, 'Department_name')]}),
                      (
                      'COMPUTER ENGINEERING  is referred to as computer science and engineering at some universities as well as soon',
                      {'entities': [(0, 21, 'Department_name')]}),
                      (
                      'LLB programs give students a solid understanding of law, as well as the critical, analytical and strategic thinking skills necessary for the field of law',
                      {'entities': [(0, 3, 'Department_name')]}),
                      (
                      'An LLB, or Bachelor of Laws, is the professional law degree awarded after completing undergraduate education',
                      {'entities': [(3, 6, 'Department_name')]}),
                      (
                      'In most countries, holding an LLB with additional accreditation, allows for the practice of law',
                      {'entities': [(30, 33, 'Department_name')]}),
                      (
                      'Some examples of LLB programs are in law sectors such as business law, European law, international law, and criminal law',
                      {'entities': [(17, 20, 'Department_name')]}),
                      (
                      'Some universities also allow students to develop their own specialized LLB programs specific to their professional interests',
                      {'entities': [(71, 74, 'Department_name')]}),
                      ('LLB programs can usually be completed in 3 or 4 years',
                       {'entities': [(0, 3, 'Department_name')]}),
                      ("The variety of different LLB programs can be overwhelming - don't let it stop you",
                       {'entities': [(25, 28, 'Department_name')]}),
                      ('Start your search by looking at the most popular LLB and Bachelor of Law programs listed below',
                       {'entities': [(49, 52, 'Department_name')]}),
                      ('LLB programs are available at universities around the world',
                       {'entities': [(0, 3, 'Department_name')]}),
                      ('LLB programs are offered in a number of various fields',
                       {'entities': [(0, 3, 'Department_name')]}),
                      (
                      'There are many popular LLB programs offered by some of the highest ranking universities in the cities listed below',
                      {'entities': [(23, 26, 'Department_name')]}),
                      ('The University of London offers two schemes for the LLB degree',
                       {'entities': [(52, 55, 'Department_name')]}),
                      ('LLB is the abbreviation for the Bachelor of Laws', {'entities': [(0, 3, 'Department_name')]}),
                      (
                      "The degree abbreviates to LLB instead of due to the traditional name of the qualification in Latin, 'Legum Baccalaureus'",
                      {'entities': [(26, 29, 'Department_name')]}),
                      (
                      'Bachelor of Law is a three year undergraduate degree in law. If you want to join legal line then you must go for LLB after bachelors in any stream of study',
                      {'entities': [(0, 15, 'Department_name')]}),
                      ('the at Wikimedia Commons and this is the most important in Bachelor of Law',
                       {'entities': [(59, 75, 'Department_name')]}),
                      (
                      'Its a five year program and soon we shall write a separate detailed article on scope of Bachelor of Law',
                      {'entities': [(88, 104, 'Department_name')]}),
                      (
                      'is a better choice than any nonprofessional MA or MSc degree after graduation Bachelor of Law it will alleviate your social status in the society',
                      {'entities': [(78, 93, 'Department_name')]}),
                      (
                      'Science after but Bachelor of Law i think that should be their first choice as it will not only help them in their legal practice but also in judiciary papers',
                      {'entities': [(18, 33, 'Department_name')]}),
                      (
                      'this an student is referred to as Bachelor of Law and engineering at some universities as well as soon',
                      {'entities': [(34, 49, 'Department_name')]}),
                      (
                      'The main Bachelor of Law abbreviation stand for Literally Legum Baccalaureus which is a Latin pharse related to law education',
                      {'entities': [(9, 24, 'Department_name')]}),
                      (
                      'In india Bachelor of Law stand for Bachelor of legislative law and many different types of varity',
                      {'entities': [(9, 24, 'Department_name')]}),
                      ('An example of BACHELOR OF LAW is the title after the name of a solicitor from England',
                       {'entities': [(14, 29, 'Department_name')]}),
                      (
                      'The BACHELOR OF LAW initiates from the Latin abbreviation of Legum Baccalaureus and many different types of session',
                      {'entities': [(4, 19, 'Department_name')]}),
                      (
                      'this is many your search by looking at the most popular BACHELOR OF LAW and Bachelor of Law programs listed below',
                      {'entities': [(76, 91, 'Department_name')]}),
                      (
                      'It is usually outside of the United States. An example of BACHELOR OF LAW is the title after the name of a solicitor from England',
                      {'entities': [(58, 74, 'Department_name')]}),
                      ("It's in latin language and it's meaning is BACHELOR OF LAW in the end",
                       {'entities': [(43, 58, 'Department_name')]}),
                      (
                      'It is an undergraduate course presented by different universities in India. There are two options to pursue BACHELOR OF LAW course',
                      {'entities': [(108, 123, 'Department_name')]}),
                      (
                      'One BACHELOR OF LAW course runs for 3 years and other is an integrated dual specialization course of 5 years',
                      {'entities': [(4, 19, 'Department_name')]}),
                      ('The degree is pursued by the individual to become a legal professor and BACHELOR OF LAW',
                       {'entities': [(72, 87, 'Department_name')]}),
                      (
                      'BACHELOR OF LAW Full Form is Bachelor of Laws. It is also implied by the Latin term �Legum Baccalaureus�',
                      {'entities': [(0, 15, 'Department_name')]}),
                      (
                      'Most of these deal with writing and publishing. A few longer abbreviations use this as well BACHELOR OF LAW',
                      {'entities': [(92, 108, 'Department_name')]}),
                      (
                      'The Department of Earth and Environmental Sciences offers BS (4 years) and MS (2 years) degree programs',
                      {'entities': [(27, 50, 'Department_name')]}),
                      (
                      'employed by national and multinational companies have proven, that it strives for highest of the academic standards at ENVIRONMENTAL SCIENCES',
                      {'entities': [(119, 141, 'Department_name')]}),
                      (
                      'Environmental Sciences and Environmental is maximum Management Representative in industrial sector',
                      {'entities': [(0, 22, 'Department_name')]}),
                      (
                      'this is many ways to define Environmental Sciences courses teach knowledge pertaining to Environmental Impact Assessment',
                      {'entities': [(28, 50, 'Department_name')]}),
                      (
                      'Introduction to Environmental Science is necessary to maitntained different types and going to throughwalk',
                      {'entities': [(16, 37, 'Department_name')]}),
                      (
                      'The course load should be minimum in the final year for the purpose of giving in Environmental Sciences that it',
                      {'entities': [(81, 103, 'Department_name')]}),
                      (
                      'Environmental Sciences is different relief for final year�s project work and career-oriented activities',
                      {'entities': [(0, 22, 'Department_name')]}),
                      (
                      'To maintain the equivalence of duration of study at international level, the main purpose is ENVIRONMENTAL SCIENCES',
                      {'entities': [(93, 115, 'Department_name')]}),
                      (
                      'To illustrate these points, this course has been developed, which examines the history ENVIRONMENTAL SCIENCES and philosophical',
                      {'entities': [(87, 109, 'Department_name')]}),
                      (
                      'ENVIRONMENTAL SCIENCES Exploration of such topics will help them become better prepared for the inevitable public debates',
                      {'entities': [(0, 22, 'Department_name')]}),
                      (
                      'Historical and logical analysis of various types of scientific hypotheses and the data that support or undermine ENVIRONMENTAL SCIENCES them',
                      {'entities': [(113, 135, 'Department_name')]}),
                      (
                      'Introduction To Climatology and A Brief History, The Earth Four Spheres and ENVIRONMENTAL SCIENCES to provides different condition and man term has been used',
                      {'entities': [(76, 98, 'Department_name')]}),
                      (
                      'many differnt catagories of ENVIRONMENTAL SCIENCES understanding of adaptation and mitigation options in relation to climate change',
                      {'entities': [(28, 50, 'Department_name')]}),
                      (
                      'Hydrocarbons & their byproducts; Future Climates and the Consequences and ENVIRONMENTAL SCIENCES is necessary to used differnt catagories',
                      {'entities': [(74, 97, 'Department_name')]}),
                      (
                      'geophysics is an applied branch of geophysics and economic geology, which uses physical methods',
                      {'entities': [(0, 10, 'Department_name')]}),
                      (
                      'geophysics can be used to directly detect the target style of mineralization, via measuring its physical properties directly',
                      {'entities': [(0, 10, 'Department_name')]}),
                      (
                      'it is also used to map the subsurface structure of a region, to elucidate the underlying structures and geophysics are as follows',
                      {'entities': [(104, 114, 'Department_name')]}),
                      ('this techniques are the most widely used geophysics technique in hydrocarbon exploration',
                       {'entities': [(41, 51, 'Department_name')]}),
                      ('Ground magnetometric surveys can be used for detecting buried ferrous metals and geophysics',
                       {'entities': [(81, 91, 'Department_name')]}),
                      (
                      'They are used to map the subsurface distribution of stratigraphy and its structure geophysics into the categories',
                      {'entities': [(82, 93, 'Department_name')]}),
                      (
                      'geophysics Gravity and magnetics are also used, with considerable frequency, in oil and gas exploration',
                      {'entities': [(0, 10, 'Department_name')]}),
                      (
                      'These can be used to determine the geometry and geophysics depth of covered geological structures including uplifts',
                      {'entities': [(48, 58, 'Department_name')]}),
                      (
                      'round the geophysics penetrating radar is a non-invasive technique, and is used within civil construction and engineering for a variety of uses',
                      {'entities': [(10, 20, 'Department_name')]}),
                      (
                      'GEOPHYSICS The Spectral-Analysis-of-Surface-Waves (SASW) method is another non-invasive techniques',
                      {'entities': [(0, 10, 'Department_name')]}),
                      (
                      'The most direct method of detection of ore via magnetism involves detecting iron ore mineralisation via mapping magnetic anomalies at GEOPHYSICS',
                      {'entities': [(134, 144, 'Department_name')]}),
                      (
                      'This is an GEOPHYSICS indirect method for assessing the likelihood of ore deposits or hydrocarbon accumulations',
                      {'entities': [(11, 21, 'Department_name')]}),
                      (
                      'The most direct method of detection of ore via magnetism involves GEOPHYSICS detecting iron ore mineralisation via mapping magnetic.',
                      {'entities': [(66, 76, 'Department_name')]}),
                      (
                      'This can be used to directly detect Mississippi Valley Type ore deposits, iron oxide copper in GEOPHYSICS',
                      {'entities': [(95, 105, 'Department_name')]}),
                      (
                      'This helps in rig monitoring and prescriptive analysis and in many different ways GEOPHYSICS in at different home automatically',
                      {'entities': [(82, 92, 'Department_name')]}),
                      (
                      'GEOPHYSICS Electric-resistance methods such as induced polarization methods can be useful for directly detecting sulfide bodies',
                      {'entities': [(0, 10, 'Department_name')]}),
                      (
                      'Social science is the branch of science devoted to the study of human societies and the relationships among individuals within those societies',
                      {'entities': [(0, 15, 'Department_name')]}),
                      (
                      'Positivist social sciences use methods resembling those of the natural sciences as tools for understanding society',
                      {'entities': [(11, 26, 'Department_name')]}),
                      ('The history of the social sciences begins in the Age of Enlightenment after 1650',
                       {'entities': [(19, 34, 'Department_name')]}),
                      (
                      'describe the field, taken from the ideas of Charles Fourier; Comte also referred to the field as social sciences',
                      {'entities': [(97, 113, 'Department_name')]}),
                      (
                      'social and environmental factors affecting it, made many of the natural sciences interested in some aspects of social sciences methodology',
                      {'entities': [(111, 126, 'Department_name')]}),
                      (
                      'In the contemporary period, Karl Popper and Talcott Parsons influenced the furtherance of the social sciences',
                      {'entities': [(94, 110, 'Department_name')]}),
                      (
                      'The term "social sciences" may refer either to the specific sciences of society established by thinkers such as Comte',
                      {'entities': [(10, 25, 'Department_name')]}),
                      (
                      'Around the start of the 21st century, the expanding domain of economics in the social sciences has been described as economic imperialism',
                      {'entities': [(79, 95, 'Department_name')]}),
                      (
                      'The social sciences disciplines are branches of knowledge taught and researched at the college or university level',
                      {'entities': [(4, 19, 'Department_name')]}),
                      (
                      'Social science fields of study usually have several sub-disciplines or branches, and the distinguishing lines between these are often both arbitrary and ambiguous',
                      {'entities': [(0, 14, 'Department_name')]}),
                      (
                      'Economics is a social sciences that seeks to analyze and describe the production, distribution, and consumption of wealth',
                      {'entities': [(15, 31, 'Department_name')]}),
                      (
                      'The expanding domain of economics in the social sciences has been developed and used in different department',
                      {'entities': [(41, 56, 'Department_name')]}),
                      (
                      'geography bridges some gaps between the natural sciences and social sciences and its used variety of types',
                      {'entities': [(61, 76, 'Department_name')]}),
                      ('History has a base in both the social sciences and the humanities',
                       {'entities': [(31, 46, 'Department_name')]}),
                      (
                      'The Social Science History Association, formed in 1976, brings together scholars from numerous disciplines interested in social history',
                      {'entities': [(4, 18, 'Department_name')]}),
                      (
                      'The social science of law, jurisprudence, in common parlance, means a rule that (unlike a rule of ethics) is capable of enforcement through institutions',
                      {'entities': [(4, 18, 'Department_name')]}),
                      (
                      'Legal policy incorporates the practical manifestation of thinking from almost every SOCIAL SCIENCES and the humanities',
                      {'entities': [(84, 99, 'Department_name')]}),
                      ('can be clearly distinguished as having little to do with the SOCIAL SCIENCES',
                       {'entities': [(61, 76, 'Department_name')]}),
                      ('whereas a B.A. underlines a majority of SOCIAL SCIENCES credits',
                       {'entities': [(40, 55, 'Department_name')]}),
                      (
                      'whether they choose a balance, a heavy science basis, or heavy SOCIAL SCIENCES basis to their degree',
                      {'entities': [(63, 78, 'Department_name')]}),
                      ('Additional applied or interdisciplinary fields related to the SOCIAL SCIENCES include',
                       {'entities': [(61, 77, 'Department_name')]}),
                      ('branch of SOCIAL SCIENCES that addresses issues of concern to developing countries',
                       {'entities': [(10, 25, 'Department_name')]}),
                      (
                      'Computational SOCIAL SCIENCES is an umbrella field encompassing computational approaches within the input',
                      {'entities': [(14, 29, 'Department_name')]}),
                      (
                      'Environmental SOCIAL SCIENCES is the broad, transdisciplinary study of interrelations between humans and the natural environment',
                      {'entities': [(14, 29, 'Department_name')]}),
                      (
                      'Legal management is a SOCIAL SCIENCES discipline that is designed for students interested in the study of state and legal elements',
                      {'entities': [(21, 37, 'Department_name')]}),
                      (
                      'Business administration (also known as business management) is the administration of a business',
                      {'entities': [(0, 23, 'Department_name')]}),
                      (
                      "Bachelor of Commerce (Bcom. or BComm) is a bachelor's degree in commerce and business administration",
                      {'entities': [(77, 100, 'Department_name')]}),
                      (
                      "it is the is a master's degree in business administration with a significant focus on management",
                      {'entities': [(34, 57, 'Department_name')]}),
                      (
                      'he Doctor of Business Administration (abbreviated DBA, D.B.A., DrBA, or Dr.B.A.) is a research doctorate awarded on the basis of advanced study',
                      {'entities': [(13, 36, 'Department_name')]}),
                      ('Bachelor of Science in Economics program is designed for those students who',
                       {'entities': [(23, 32, 'Department_name')]}),
                      ('career oriented and market determined educational program in the field of Economics',
                       {'entities': [(74, 83, 'Department_name')]}),
                      (
                      'The program is the blend of different courses like theoretical, quantitative and applied areas in economics',
                      {'entities': [(98, 107, 'Department_name')]}),
                      (
                      'The main objective is to achieve the highest possible standards of education, teaching and research in economics more are different',
                      {'entities': [(103, 112, 'Department_name')]}),
                      ('Impart sound theoretical and applied knowledge of economics',
                       {'entities': [(50, 59, 'Department_name')]}),
                      (
                      'Provide a thorough understanding of the economics theory pertaining to global in the different society and many types',
                      {'entities': [(40, 49, 'Department_name')]}),
                      ('global economics issues and its impact on Pakistan�s economy',
                       {'entities': [(7, 16, 'Department_name')]}),
                      (
                      'Develop professionals with a sound knowledge in the field of economics who can understand and analyze problems faced by developing country like Pakistan',
                      {'entities': [(61, 70, 'Department_name')]}),
                      ('Prepare students for advanced studies in economics in different types in the sytle',
                       {'entities': [(41, 50, 'Department_name')]}),
                      (
                      'Some programs allow students to select a specialty within the economics field so they can tailor their curricula to their career goals',
                      {'entities': [(62, 71, 'Department_name')]}),
                      (
                      "Many students continue their studies in graduate programs by earning a master's or doctoral degree in economics",
                      {'entities': [(102, 111, 'Department_name')]}),
                      ('A Bachelor of Science in Economics gives students the necessary knowledge in math',
                       {'entities': [(25, 34, 'Department_name')]}),
                      (
                      'English is a West Germanic language that was first spoken in early medieval England and eventually',
                      {'entities': [(0, 7, 'Department_name')]}),
                      (
                      'The earliest forms of English, a group of West Germanic (Ingvaeonic) dialects brought to Great Britain by Anglo-Saxon settlers in the 5th century',
                      {'entities': [(22, 29, 'Department_name')]}),
                      (
                      'Modern English began in the late 15th century with the introduction of the printing press to London, the printing of the King James Bible and the start of the Great Vowel Shift',
                      {'entities': [(7, 14, 'Department_name')]}),
                      (
                      'English is the largest language by number of speakers,[10] and the third most-spoken native language in the world, after Standard Chinese and Spanish',
                      {'entities': [(0, 7, 'Department_name')]}),
                      (
                      'English is the majority native language in the United States, the United Kingdom, Canada, Australia, New Zealand and the Republic of Ireland',
                      {'entities': [(0, 7, 'Department_name')]}),
                      (
                      'Modern English grammar is the result of a gradual change from a typical Indo-European dependent marking pattern',
                      {'entities': [(7, 14, 'Department_name')]}),
                      (
                      'but in extreme cases can lead to confusion or even mutual unintelligibility between English speakers',
                      {'entities': [(84, 91, 'Department_name')]}),
                      (
                      'Unlike Icelandic and Faroese, which were isolated, the development of English was influenced by a long series of invasions of the British',
                      {'entities': [(70, 77, 'Department_name')]}),
                      ('Some scholars have argued that English can be considered a mixed language or a creole',
                       {'entities': [(31, 38, 'Department_name')]}),
                      ('most specialists in language contact do not consider English to be a true mixed language',
                       {'entities': [(53, 61, 'Department_name')]}),
                      (
                      'English is classified as a Germanic language because it shares innovations with other Germanic languages such as Dutch, German, and Swedish.[25]',
                      {'entities': [(0, 7, 'Department_name')]}),
                      ('Even after the vowel shift the language still sounded different from Modern English',
                       {'entities': [(76, 83, 'Department_name')]}),
                      (
                      'The countries where English is spoken can be grouped into different categories according to how',
                      {'entities': [(20, 27, 'Department_name')]}),
                      (
                      'English does not belong to just one country, and it does not belong solely to descendants and differet types of close',
                      {'entities': [(0, 7, 'Department_name')]}),
                      (
                      "The Bachelor of Business Administration (BBA or B.B.A.) is a bachelor's degree in business administration",
                      {'entities': [(4, 39, 'Department_name')]}),
                      (
                      'Bachelor of Business Administration is a quantitative variant on the BBA. General educational requirements are relatively mathematics intensive',
                      {'entities': [(0, 35, 'Department_name')]}),
                      (
                      'Bachelor of Bussiness Administration The Academy of Business Administration was established in the year of 1993 by Mr. Sudhasindhu Panda',
                      {'entities': [(0, 36, 'Department_name')]}),
                      (
                      'Germanic language that was first spoken in early medieval England and eventually in Bachelor of Bussiness Administration at different types',
                      {'entities': [(83, 120, 'Department_name')]}),
                      (
                      "The bachelor's degree program offers a progressive curriculum Bachelor of Bussiness Administration designed to teach business fundamentals and higher level leadership skills",
                      {'entities': [(62, 98, 'Department_name')]}),
                      (
                      'This specialization in Bachelor of business administration helps you develop the management, interpersonal, and professional skills you need to advance your career',
                      {'entities': [(23, 58, 'Department_name')]}),
                      (
                      'The Bachelor of Science in Bachelor of Business Administration (BSBA) is four-year (8 semesters) program and designed for candidates having 12-years education with commerce & business backgrounds.',
                      {'entities': [(27, 62, 'Department_name')]}),
                      (
                      'This program offers a progressive Bachelor of Business Administration curriculum designed to teach business fundamentals and higher level leadership skills, and equip students to function more effectively in a business-driven economy',
                      {'entities': [(34, 69, 'Department_name')]}),
                      (
                      'This program will Bachelor of Business Administration help students to examine how technology and innovation can help organizations develop a sustainable competitive advantage',
                      {'entities': [(18, 53, 'Department_name')]}),
                      (
                      'It is four-year full time study program spread over eight semesters. Each semester has at least 18 weeks duration for teaching and examinations etc Bachelor of Business Administration',
                      {'entities': [(160, 183, 'Department_name')]}),
                      (
                      'BBA The students� study progress evaluation mechanism is based on continuous assessment throughout the semester',
                      {'entities': [(0, 4, 'Department_name')]}),
                      (
                      'The mid and final term exams are conducted at VU�s designated exam centers and usually count for 80 to 85% of the total marks for a course BBA.',
                      {'entities': [(139, 142, 'Department_name')]}),
                      (
                      'Students are required to complete a Project/ Internship Report in the final semester of their BBA.',
                      {'entities': [(94, 97, 'Department_name')]}),
                      (
                      'The choice of the final project is at BBA the student�s discretion. However, consultation with the student advisor is compulsory.',
                      {'entities': [(38, 41, 'Department_name')]}),
                      (
                      'The students who are already in service shall be BBA exempted from Internship but required to submit the Project',
                      {'entities': [(49, 53, 'Department_name')]}),
                      (
                      'BBA Students have to submit a detailed write-up of the Project and may be required to give a presentation',
                      {'entities': [(0, 3, 'Department_name')]}),
                      (
                      'The students of BBA who are already in service shall be exempted from Internship but required to submit the Project',
                      {'entities': [(16, 19, 'Department_name')]}),
                      (
                      'To be eligible for the BBA award BS degree, the students are required to complete prescribed course work of 132 credit hours with a minimum Cumulative Grade Point Average (CGPA) of 2.0 out of 4',
                      {'entities': [(23, 26, 'Department_name')]}),
                      (
                      'The courses BBA may be revised time to time as a result of continuous review to bring them at par with courses',
                      {'entities': [(12, 16, 'Department_name')]}),
                      ('The University reserves the right to change fee structure from time to time BBA.',
                       {'entities': [(76, 79, 'Department_name')]}),
                      (
                      'A Bachelor of Business Administration (BBA) program can prepare students to manage companies by teaching subjects such as marketing and human resources.',
                      {'entities': [(14, 37, 'Department_name')]}),
                      (
                      'The 4-year degree program provides a fundamental education in business and management principles in BBA.',
                      {'entities': [(100, 103, 'Department_name')]}),
                      (
                      'Programs typically allow students to BBA specialize in one of multiple concentration areas, including international business, finance, real estate',
                      {'entities': [(37, 40, 'Department_name')]}),
                      (
                      'BBA programs can offer practical management training that can prepare students to successfully work within a large or small organization.',
                      {'entities': [(0, 3, 'Department_name')]}),
                      (
                      'Programs may emphasize the development of communications, quantitative reasoning, and business analysis skills. Through BBA courses.',
                      {'entities': [(120, 123, 'Department_name')]}),
                      (
                      'Through the BBA programs, students can pursue business education and learn skills that will help them pursue various management and administrative roles within a company.',
                      {'entities': [(12, 15, 'Department_name')]}),
                      (
                      'BBA is a 4-year degree program which prepares students for a variety of different management and administrative roles within a company.',
                      {'entities': [(0, 3, 'Department_name')]}),

            ('management science is also concerned with so-called soft-operational analysis, which concerns methods for strategic planning, strategic decision support, and problem structuring methods (PSM).',
             {'entities': [(0, 18, 'Department_name')]}),
            (
             'management science is a peer-reviewed academic journal that covers research on all aspects of management related to strategy, entrepreneurship, innovation, information technology, and organizations as well as all functional areas of business, such as accounting, finance, marketing, and operations.',
             {'entities': [(0, 18, 'Department_name')]}), (
             "It is published by the Institute for Operations Research and the management sciences and was established in 1954 by the Institute's precursor, The Institute of management sciences. C. West Churchman was the founding editor-in-chief.",
             {'entities': [(65, 84, 'Department_name')]}), (
             'The Institute of management sciences (IMS Lahore), formerly known as Pak-American Institute of management sciences (Pak-AIMS), is a project of AKEF established in Lahore, Pakistan in 1987 which offers undergraduate and graduate programs in management and computer sciences.',
             {'entities': [(17, 36, 'Department_name')]}), (
             "Pak-AIMS was issued 'No Objections Certificate (NOC)' by the University Grants Commission, now known as the Higher Education Commission (Pakistan) for the award of charter in 1995. Consequently, the institute was chartered as Institute of management sciences (IMS) by the Government of Punjab (Pakistan) under the Punjab Ordinance XXIII of 2002 and given degree-awarding status.",
             {'entities': [(239, 258, 'Department_name')]}), (
             "The Pak-American Institute of management sciences (Pak-AIMS) to reflect the Institute's Articulation Agreement with the College of Staten Island of City University of New York (CSI/CUNY), USA.",
             {'entities': [(30, 49, 'Department_name')]}), (
             'The Institute for Operations Research and the management sciences (INFORMS) is an international society for practitioners in the fields of operations research (O.R.).',
             {'entities': [(46, 65, 'Department_name')]}), (
             'The Institute of management sciences (TIMS). The 2019 president of the institute is Dean Ramayya Krishnan of Carnegie Mellon University.',
             {'entities': [(17, 36, 'Department_name')]}), (
             "According to INFORMS' constitution, the Institute's purpose is to improve operational processes, decision-making, and management by individuals and organizations through operations research, the management sciences, analytics and related scientific methods.",
             {'entities': [(195, 214, 'Department_name')]}), (
             'The constitution provides that the mission of INFORMS is to lead in the development, dissemination and implementation of knowledge, basic and applied research and technologies in operations research, the management sciences, analytics and related methods of improving operational processes, decision-making, and management.',
             {'entities': [(204, 223, 'Department_name')]}), (
             'INFORMS members are operations researchers and analytics professionals who work for universities, corporations, consulting groups, military, the government, and health care. Many are academics who teach operations research, management science, analytics, and the quantitative sciences in engineering and business schools.',
             {'entities': [(224, 242, 'Department_name')]}), (
             'The Army Public College of management and sciences, commonly known as APCOMS, is a private college located in Rawalpindi, Punjab, Pakistan.',
             {'entities': [(27, 50, 'Department_name')]}), (
             'It is often considered to be a sub-field of applied mathematics.[2] The terms management science and decision science are sometimes used as synonyms.',
             {'entities': [(78, 96, 'Department_name')]}), (
             'In 1967 Stafford Beer characterized the field of management science as the business use of operations research ',
             {'entities': [(49, 67, 'Department_name')]}), (
             ' Like operational research itself, management science (MS) is an interdisciplinary branch of applied mathematics devoted to optimal decision planning, with strong links with economics, business, engineering, and other sciences.',
             {'entities': [(35, 53, 'Department_name')]}), (
             "The management scientist's mandate is to use rational, systematic, science-based techniques to inform and improve decisions of all kinds. Of course, the techniques of management science are not restricted to business applications but may be applied to military, medical, public administration, charitable groups, political groups or community groups.",
             {'entities': [(167, 185, 'Department_name')]}), (
             'management science is concerned with developing and applying models and concepts that may prove useful in helping to illuminate management issues and solve managerial problems, as well as designing and developing new and better models of organizational excellence.',
             {'entities': [(0, 18, 'Department_name')]}), (
             'The application of these models within the corporate sector became known as management science.',
             {'entities': [(76, 94, 'Department_name')]}), (
             'The Institute for Operations Research and the management sciences (INFORMS) publishes thirteen scholarly journals about operations research, including the top two journals in their class, according to 2005 Journal Citation Reports.',
             {'entities': [(46, 65, 'Department_name')]}), (
             'management science, or MS, is the discipline of using mathematics, and other analytical methods, to help make better business decisions.',
             {'entities': [(0, 18, 'Department_name')]}), (
             'Some of the fields that are englobed within management science include: decision analysis, optimization, simulation, forecasting, game theory, network/transportation models, mathematical modeling, data mining, probability and statistics, Morphological analysis, resources allocation, project management as well as many others.',
             {'entities': [(44, 62, 'Department_name')]}), (
             "The management scientist's mandate is to use rational, systematic, science-based techniques to inform and improve decisions of all kinds. Of course, the techniques of management science are not restricted to business applications but may be applied to military, medical, public administration, charitable groups, political groups or community groups.",
             {'entities': [(167, 185, 'Department_name')]}), (
             'Institute of management sciences (management education with public spirit and market dynamism)',
             {'entities': [(13, 32, 'Department_name')]}), (
             'This is normally a two years program comprising of 4 semesters. There will be a Fall and a Spring semester in each year. The maximum duration to complete MS in management sciences is 4 years.',
             {'entities': [(160, 179, 'Department_name')]}), (
             'In the pursuit of delivering quality education at your door step, the Department of management sciences has established a diversified academic portfolio both at graduate and undergraduate levels.',
             {'entities': [(84, 103, 'Department_name')]}), (
             'The Department of management sciences aims to offer educationally sound and directly relevant programs to those areas of industry, commerce, the professions and public service.',
             {'entities': [(18, 37, 'Department_name')]}), (
             'The overall objective of the management sciences department is to develop managers and business leaders with the vision, knowledge, creativity, skills, ethics and entrepreneurial ability necessary to integrated, critical aware, dynamic and strategic view of organizations and to play an effective role within them.',
             {'entities': [(29, 48, 'Department_name')]}), (
             'We aim to deliver quality education at your door step by offering wide array of educational programs in the field of management sciences among a diverse community of learners and develop future business leaders of the world.',
             {'entities': [(117, 136, 'Department_name')]}), (
             'The Department of management sciences offers a large number of diversified educational programs thereby producing a maximum number of graduating students at the moment.',
             {'entities': [(18, 37, 'Department_name')]}), (
             'The Department of management sciences (DMS) was established in 1994 to fulfill the demands for quality business professionals by organizations. Since then, the Department has won accolades of success in the business world by producing scintillating results year after year.',
             {'entities': [(18, 37, 'Department_name')]}), (
             'The MS in management program is designed to develop the intellectual ability of researchers through understanding the academic body of knowledge in the field of management sciences with specializations in Human Resource Management.',
             {'entities': [(161, 180, 'Department_name')]}), (
             'The electives can be taken from graduate level courses in the Faculty of management sciences with the recommendation of the supervisor.',
             {'entities': [(73, 92, 'Department_name')]})

        ]

        def train_spacy(data, iterations):
            TRAIN_DATA = data
            nlp = spacy.blank('en')
            if 'ner' not in nlp.pipe_names:
                ner = nlp.create_pipe('ner')
                nlp.add_pipe(ner, last=True)


            for _, annotations in TRAIN_DATA:
                for ent in annotations.get('entities'):
                    ner.add_label(ent[2])

            other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
            with nlp.disable_pipes(*other_pipes):
                optimizer = nlp.begin_training()
                for itn in range(iterations):
                    print("Starting iteration " + str(itn))
                    random.shuffle(TRAIN_DATA)
                    losses = {}
                    for text, annotations in TRAIN_DATA:
                        nlp.update(
                            [text],
                            [annotations],
                            drop=0.2,
                            sgd=optimizer,
                            losses=losses)
                    print(losses)
            return nlp


class data_preparation:

    def training(self):
        nlp = spacy.load('en_core_web_sm')
        if 'ner' not in nlp.pipe_names:
            ner = nlp.create_pipe('ner')
            nlp.add_pipe(ner, last=True)
        else:
            ner = nlp.get_pipe('ner')
        Recipient_names_dic = {
        'a': [
        "aslam",
        "abbas",
        "abbasi",
        "abdul hanan",
        "abdul ghaffar",
        "abdul",
        "abdul moiz",
        "abdur",
        "abid",
        "abu bakr",
        "abu baker",
        "adam",
        "adan",
        "adeel",
        "adil",
        "adnan",
        "afridi",
        "aftaab",
        "aftab",
        "ahad",
        "ahmad",
        "alam",
        "ahmed",
        "ahsen",
        "ahsan",
        "aiman",
        "ajmal",
        "akbar",
        "akhtar",
        "akmal",
        "akram",
        "ali",
        "amin",
        "amir",
        "amjad",
        "ammar",
        "anas",
        "anees",
        "aansa",
        "ansar",
        "anwar",
        "aqeel",
        "abdullah",
        "arbaaz",
        "arbab",
        "arham",
        "arif",
        "arif ur rahman",
        "arish",
        "arshad",
        "arslan",
        "arsalan",
        "asad",
        "asfand",
        "asfand yar",
        "asghar",
        "asher",
        "ashfaq",
        "ashraf",
        "asif",
        "asim",
        "ata",
        "ateeb",
        "atif",
        "atiq",
        "awan",
        "awais",
        "ayaan",
        "ayaaz",
        "aybad",
        "ayaz",
        "ayub",
        "ayyub",
        "azaan",
        "azad",
        "azeem",
        "azhar",
        "aziz ullah",
        "aziz",
        "azlan",
        "azmat",
        "azam",
        "afia",
        "asia",
        "abdul basit",
        "abeer",
        "abeera",
        "amara"
        "abidah",
        "abrar",
        "adeela",
        "adeelah",
        "adila",
        "afeefa",
        "afia",
        "afreen",
        "afshan",
        "afsheen",
        "aimal",
        "aimen",
        "aiyla",
        "aiza",
        "aizah",
        "ajwa",
        "aleem",
        "aleemah",
        "aleena",
        "aleeza",
        "alesha",
        "alyia",
        "alina",
        "alishba",
        "aliyah",
        "aliza",
        "almas",
        "altaf",
        "ambar",
        "ambrina",
        "ambreena",
        "amina",
        "amjad",
        "amna",
        "amra",
        "amrah",
        "amreen",
        "anam",
        "andaleeb",
        "andalib",
        "aneeqa",
        "anila",
        "anisa",
        "anisha",
        "aniya",
        "anjum",
        "anousha",
        "anum",
        "anwar",
        "aqeela",
        "aqsa",
        "areebah",
        "areej",
        "arfa",
        "arij",
        "arisha",
        "aroosa",
        "asifa",
        "asiya",
        "asma",
        "asmara",
        "asrar",
        "ateeqah",
        "atifa",
        "atika",
        "ayaat",
        "ayan",
        "ayesha",
        "azeeza",
        "azhar",
        "aziz",
        "aziza",
        ],
        'b': [
        "babar",
        "baber",
        "badial zaman",
        "bashar",
        "basharat",
        "bashir",
        "bin",
        "bilal",
        "bhatti",
        "butt",
        "bakht",
        "basma",
        "batool",
        "batul",
        "beenish",
        "benazir",
        "bibi",
        "bilqees",
        "bilqis",
        "binish",
        "bin",
        "bisma",
        "bushra",
        ],
        'c': [
        "chugtai",
        "chaudhary",
        ],
        'd': [
        "daanish",
        "deeba",
        "danish",
        "dar",
        "danial",
        "daud",
        "dawoud",
        "dania",
        "daniah",
        "dua",
        ],
        'e':[
        "ehsan",
        "ejaz",
        "ellahi",
        "eiman",
        "eman",
        "eraj",
        "erum",
        "eshaal",
        "eshal",
        ],
        'f':[
        "fahad",
        "fahd",
        "faheem",
        "fahim",
        "faiq",
        "faisal",
        "faiyaz",
        "faiz",
        "faizan",
        "fakhir",
        "fakhar",
        "faraz",
        "fareed",
        "farhan",
        "farid",
        "faris",
        "farooq",
        "farrukh",
        "faseeh",
        "fateh",
        "fawad",
        "fawwaz",
        "fayaaz",
        "faysal",
        "fazal",
        "feroz",
        "fida",
        "fahima",
        "fahmida"
        "faima",
        "faiqa",
        "faiza",
        "falak",
        "farah",
        "fareeda",
        "farha",
        "farhana",
        "farhat",
        "farida",
        "fariha",
        "farihah",
        "farisha",
        "farkhandah",
        "farwa",
        "faryal",
        "farzana",
        "faseelah",
        "fatima",
        "fauzia",
        "fehmida",
        "fida",
        "firdous",
        "fiza",
        "fouzia",
        "fozia",
        ],
        'g':[
        "ghani",
        "ghayoor",
        "ghazanfar",
        "ghulam",
        "gilani",
        "gillani",
        "gohar",
        "gul",
        "gulfam",
        "gulshan",
        "gulzar",
        "gazala",
        "ghazala",
        ],
        'h':[
        "habeebullah",
        "habib",
        "habib ur rehman",
        "hadi",
        "hafiz",
        "haider",
        "haji",
        "hakeem",
        "hakim",
        "hamid",
        "hammad",
        "hamza",
        "hunzala",
        "hanzala",
        "hanif",
        "haq",
        "haris",
        "haroon",
        "hasan",
        "hasham",
        "hashim",
        "hashir",
        "hashmat",
        "hasnain",
        "hassan",
        "hayat",
        "hayaat",
        "hesam",
        "hisham",
        "humayun",
        "humera",
        "humza",
        "hurairah",
        "husnain",
        "hussain",
        "habiba",
        "hadeeqa",
        "hadiya",
        "hadiyah",
        "hafiza",
        "hafizah",
        "hafsa",
        "hafsah",
        "hajra",
        "haleema",
        "halima",
        "hamnah",
        "hamra",
        "hanan",
        "haneefa",
        "hania",
        "hanifa",
        "hareem",
        "haseena",
        "hasna",
        "haya",
        "hiba",
        "hifza",
        "hira",
        "hoda",
        "hoor",
        "hooria",
        "hooriya",
        "horia",
        "huda",
        "huma",
        "humaira",
        "hur",
        "huriya",
        "husna",
        ],
        'i':[
        "ibaad",
        "ibn",
        "ibrahim",
        "idrees",
        "iftikhar",
        "ihsan",
        "ihtesham",
        "ihtisham",
        "ihtsham",
        "ijaz",
        "ilyas",
        "imad",
        "imran",
        "imtiaz",
        "inam",
        "inayat",
        "intikhab",
        "iqbal",
        "irfan",
        "ishaq",
        "isma",
        "ismail",
        "israr",
        "ibtihaj",
        "ibtisam",
        "iffat",
        "ifra",
        "iftikar",
        "iftikhar",
        "ijabo",
        "ijaz",
        "ikram",
        "iman",
        "inaam",
        "inaaya",
        "inam",
        "inaya",
        "inayah",
        "inayat",
        "insha",
        "intisar",
        "iqra",
        "iraj",
        "iram",
        "irum",
        "ishaal",
        "ishfaq",
        "isma",
        "isra",
        ],
        'j':[
        "jan",
        "jawwad",
        "jatt",
        "jutt",
        "jafar",
        "jafri",
        "jaffar",
        "jaffer",
        "jahangir",
        "jahanzeb",
        "jaleel",
        "jalil",
        "jamal",
        "jamalaldin",
        "jameel",
        "jamil",
        "javaid",
        "javed",
        "jawad",
        "jazib",
        "jehanzeb",
        "jibran",
        "jibril",
        "junaid",
        "jodat",
        "joddat",
        "jannat",
        "javeria",
        ],
        'k':[
        "kamil",
        "kashif",
        "kaleem",
        "kalil",
        "kamal",
        "kamran"
        "kamil",
        "karim",
        "khaleel",
        "khan",
        "khaleeq",
        "khalid",
        "khalil",
        "khateeb",
        "khattak",
        "khatak",
        "khawar",
        "khawaja",
        "khuram",
        "khurram",
        "khurshid",
        "khushbakht",
        "kinza",
        "kiran",
        "kainat",
        "kalsoom",
        "kanwal",
        "kanza",
        "kareema",
        "karima",
        "kausar",
        "khadeeja",
        "khadija",
        "khadijah",
        "komal",
        ],
        'l':[
        "latif",
        "luqman",
        "laiba",
        "lamisa",
        "laraib",
        "lateefa",
        "latifa",
        "layla",
        "lubna",
        ],
        'm':[
        "maaz",
        "majeed",
        "majid",
        "makhdoom",
        "malik",
        "masood",
        "masroor",
        "mazhar",
        "mehroz",
        "mehboob",
        "mahmood",
        "mehmood",
        "mehtab",
        "minhaj",
        "mir",
        "miraj",
        "mirza",
        "misbah",
        "mishal",
        "moazzam",
        "moazam",
        "mobeen",
        "moeez",
        "moeena",
        "moetesum",
        "mohammed",
        "mohid",
        "mohsin",
        "muhsan",
        "moosa",
        "mudasir",
        "multani",
        "mubashir",
        "mohammad",
        "muhammad",
        "mujeeb",
        "mujahid",
        "mukhtar",
        "moiz",
        "maryam",
        "mumtaz",
        "munawwar",
        "muneeb",
        "munib",
        "munir",
        "murtaza",
        "musa",
        "mussarrat",
        "mustafa",
        "muzaffar",
        "muzammal",
        "muzzammil",
        "madiha",
        "maha",
        "maheen",
        "mahek",
        "mahira",
        "mahnoor",
        "mahrukh",
        "mahru",
        "maida",
        "maimoona",
        "malieka",
        "malaika",
        "malaikah",
        "maliha",
        "malika",
        "malikah",
        "manaal",
        "manzoor",
        "maria",
        "mariam",
        "mariyam",
        "marwa",
        "marwah",
        "mashal",
        "masooma",
        "meena",
        "mehak",
        "mehek",
        "mehnoor",
        "mehr",
        "mehreen",
        "mehrunisa",
        "mehvish",
        "mahvish",
        "mehwish",
        "memoona",
        "mevish",
        "minal",
        "misba",
        "miral",
        "momina",
        "mona",
        "mumina",
        "munawar",
        "munawwar",
        "muneeba",
        "muneza",
        "muniba",
        "munira",
        "munisa",
        "muqadas",
        ],
        'n':[
        "nadia",
        "nabeel",
        "nadeem",
        "nadim",
        "nadir",
        "naeem",
        "nafees",
        "najam ul islam",
        "najam",
        "najeeb",
        "namir",
        "naqi",
        "naqash",
        "naseem",
        "naseer",
        "nasir",
        "naveed",
        "nawaz",
        "nayab",
        "nazeer",
        "nazim",
        "nazir",
        "nisar",
        "nisa",
        "numair",
        "nabeeha",
        "nabeela",
        "nabila",
        "nagheen",
        "naghin",
        "nagina",
        "naheed",
        "naheeda",
        "nahid",
        "nahida",
        "nahidah",
        "naila",
        "najaf",
        "namra",
        "nargis",
        "nasim",
        "nasreen",
        "nasrin",
        "nasrullah",
        "natasha",
        "naureen",
        "nausheen",
        "naushin",
        "naveda",
        "nayyab",
        "nazia",
        "nazish",
        "nazma",
        "nazmin",
        "neelam",
        "neha",
        "nelam",
        "nelofar",
        "nibras",
        "nida",
        "nigar",
        "nighat",
        "nihal",
        "nija",
        "nilofar",
        "nilofer",
        "nimra",
        "nimrah",
        "nisha",
        "nishat",
        "nisreen",
        "nisrin",
        "nissa",
        "noor",
        "nora",
        "nauman",
        "noman",
        "norah",
        "noreen",
        "noshi",
        "nizami",
        "noshaba",
        "nosheen",
        "noureen",
        "numa",
        "nunah",
        "nur",
        "nusrat",
        "nuwairah",
        "nyla",
        ],
        'o':[
        "obaid",
        "omair",
        "omar",
        "osama",
        "owais",
        ],
        'p':[
        "parvez",
        "pervaiz",
        "parveen",
        ],
        'q':[
        "qadir",
        "qais",
        "qasif",
        "qaisrani",
        "qaseem",
        "qasim",
        "qudoos",
        "qazi",
        "qureshi",
        "qurban",
        "qamar",
        "qaysar",
        "qirat",
        "qurratulain",
        "qurut ul ain",
        ],
        'r':[
        "rahil",
        "rafay",
        "rafi ullah",
        "rafi",
        "rafia",
        "rafiq",
        "rahat",
        "raheel",
        "rahil",
        "rahim",
        "rehman",
        "rahman",
        "rahmat",
        "rehan",
        "raja",
        "ramis",
        "ramzan",
        "rameez",
        "ramiz",
        "raqeeb",
        "rasheed",
        "rashid",
        "rasool",
        "rasul",
        "rauf",
        "rayyan",
        "romana",
        "raza",
        "razin",
        "riaz",
        "rida",
        "rizwan ul haq",
        "rizwan",
        "rohail",
        "rameen",
        "rabab",
        "rabia",
        "rahila",
        "rahimah",
        "raihana",
        "raina",
        "raja",
        "rana",
        "rania",
        "raniya",
        "rayan",
        "reham",
        "rifat",
        "riffat",
        "rihana",
        "rimsha",
        "rizwana",
        "rubina",
        "rukhsana",
        "rukhsar",
        "ruksana",
        "rumana",
        "ruqaya",
        "ruqayya",
        ],
        's':[
        "saad",
        "sabahuddin",
        "sibtain",
        "saeed ur rehman",
        "saeed",
        "safdar",
        "sahar",
        "sahir",
        "said",
        "saif",
        "saim",
        "sajjad",
        "saleem",
        "saleh",
        "sameed",
        "sameer",
        "sami",
        "sanaullah",
        "saqlain",
        "saqib",
        "sarfraz",
        "sarmad",
        "sarwar",
        "sati",
        "saud",
        "seema",
        "shabaan",
        "shabab",
        "shabir",
        "shabbir",
        "shadab",
        "shaftab",
        "shafeeq",
        "shafique",
        "shafiq",
        "shafiullah",
        "shafqat",
        "shah",
        "shahid",
        "shahab",
        "shehryar",
        "shaharyar",
        "shahbaz",
        "shaheen",
        "shahmir",
        "shaheer",
        "shahnawaz",
        "shahrukh",
        "shahzad",
        "shahzaib",
        "shakoor",
        "shakeel",
        "shakib",
        "shakir",
        "shams ul deen",
        "shams",
        "shamshad",
        "shareef",
        "sharif",
        "shariq",
        "sharjeel",
        "shaukat",
        "shayan",
        "shazeb",
        "shazia",
        "shehzad",
        "shehroz",
        "shehryar",
        "sheikh",
        "shehzaad",
        "shifa",
        "shoaib",
        "shujaat",
        "shuja",
        "shumayl",
        "sidique",
        "siddiqi",
        "sohaib",
        "sohail",
        "sohima",
        "subhan",
        "sufyan",
        "suhaib",
        "suhail",
        "suhaim",
        "sulaiman",
        "sultan",
        "suroor",
        "suleman",
        "syed",
        "sadia",
        "sara",
        "saba",
        "sabiha",
        "sabina",
        "sabrin",
        "sadaf",
        "sadia",
        "safia",
        "sahar",
        "saima",
        "saira",
        "sakina",
        "salma",
        "samabia",
        "samia",
        "samina",
        "samiya",
        "samra",
        "sana",
        "sanabil"
        "sanaubar",
        "saniya",
        "sara",
        "sarish",
        "sehrish",
        "shabnam",
        "shafaq",
        "shagufta",
        "shaheena",
        "shahnaz",
        "shaista",
        "shams",
        "shareefa",
        "shazia",
        "shenaz",
        "shezan",
        "shimreen",
        "shireen",
        "sidra",
        "simra",
        "sobia",
        "sofia",
        "sohana",
        "somaya",
        "sonia",
        "subhaan",
        "suheera",
        "sumaira",
        "sumera",
        "syeda",
        "sundas",
        ],
        't':[
        "tabish",
        "taha",
        "tahir",
        "tahseen",
        "taimur",
        "taj",
        "talal",
        "talat",
        "talha",
        "talib",
        "tamim",
        "tanvir",
        "tanveer",
        "tareef",
        "tarif",
        "tariq",
        "taseen",
        "tasneen",
        "taufiq",
        "tauqeer",
        "tayyab",
        "tazeem",
        "tazneem",
        "tehsin",
        "tehseenullah",
        "tehseen",
        "touseef",
        "tauseef",
        "tipu",
        "tauseef",
        "taalah",
        "taalia",
        "tabassum",
        "tabinda",
        "tabina",
        "tahira",
        "tamanna",
        "taqiyah",
        "taqwa",
        "taqwaa",
        "tasneem",
        "tasnim",
        "tayyaba",
        "tehmina",
        "tehreem",
        "tooba",
        "toufeeq",
        ],
        'u':[
        "ubaid",
        "umar",
        "umer",
        "ullah",
        "uhban",
        "ul",
        "ulfat",
        "umair",
        "umar",
        "umarah",
        "umayyah",
        "umaid",
        "urooj",
        "urwah",
        "usama",
        "usman",
        "uzair",
        "uhud",
        "ulfah",
        "umaiza",
        "unsa",
        "uroosa",
        "ul",
        "ur"
        "ushna",
        "uswa",
        "uzma",
        ],
        'v':[
        "varisha",
        ],
        'w':[
        "wafa",
        "wahab",
        "waheed",
        "wahaj",
        "wahid",
        "wajeeh",
        "wajid",
        "wajih",
        "wakeel",
        "wakil",
        "waleed",
        "waqar",
        "waqas",
        "waseem",
        "wasif",
        "wasil",
        "wasim",
        "wazir",
        "wafa",
        "wajahat",
        "wajiha",
        "wania",
        "waniya",
        "warda",
        "wareesha",
        ],
        'y':[
        "yahya",
        "yameen",
        "yaqoob",
        "yaseen",
        "yasir",
        "yunus",
        "yousaf",
        "yusuf",
        "yasmeen",
        "yasmeena",
        "yasmin",
        "yasmina",
        "yumna",
        ],
        'z':[
        "zafar",
        "zaheer",
        "zahid",
        "zaidi",
        "zaid",
        "zain ul abideen",
        "zain",
        "zakria",
        "zakir",
        "zaman",
        "zameer",
        "zarar",
        "zaroon",
        "zartasha",
        "zeeshan",
        "zia",
        "zeb",
        "zohaib",
        "zubair",
        "zuhaib",
        "zuhair",
        "zuhoor",
        "zulfiqar",
        "zara",
        "zafreen",
        "zaheera",
        "zahida",
        "zahira",
        "zahra",
        "zaida",
        "zain",
        "zainab",
        "zara",
        "zareena",
        "zeba",
        "zeena",
        "zeenat",
        "zehna",
        "zehra",
        "zoha",
        "zohra",
        "zoya",
        "zubaria",
        "zubaydah",
        "zubi",
        "zunaira",
        ],
        }


        to_train_ents = []
        rand_sent = []
        training_sent_list = []

        counter1 = 0
        i = 0
        with open("training_sentences.txt", "r") as tn:
            for key, names in Recipient_names_dic.items():
                for name in names:
                    lines = tn.readlines()
                    random.shuffle(lines)
                    tn.seek(0)
                    for line in lines:
                        # line = tn.readline()
                        # if not line:
                        #     break
                        word = line.split()
                        random.shuffle(word)

                        # if line == lines[0]:
                        #     rand_sent = list(word)
                        #     rand_sent.insert(0, name)
                        #     rand_sent = ' '.join(rand_sent)
                        #     # new_sentence = ' '.join(word)
                        #     training_sent_list.append(rand_sent + "\n")
                        for char in range(len(word)):
                            counter1 = counter1 + 1
                        print(counter1)
                        rand_in_word = random.randint(0, counter1)
                        print(rand_in_word)
                        rand_sent = list(word)
                        rand_sent.insert(rand_in_word, name)
                        rand_sent = ' '.join(rand_sent)
                        # new_sentence = ' '.join(word)
                        training_sent_list.append(rand_sent + "\n")
                        counter1 = 0
                        print(rand_sent)
                    # random.shuffle(line)
        tn.close()
        with open("training_data_recipient.txt", "w") as wr:
            wr.writelines(training_sent_list)
        wr.close()

        TRAIN_DATA = [(
            'Department of Computer Engineering is committed to excellence in teaching, research and inculcating a sense of pride and confidence in our students. ',
            {'entities': [(14, 34, 'Department_name')]}), (
            'he aim of the department is to pursue excellence in Computer Engineering through teaching and research and we are achieving our objectives with the help of our highly qualified and distinguished faculty of national and international repute.',
            {'entities': [(52, 72, 'Department_name')]}),
            (
                'Department of Computer Engineering endeavors to provide best learning and professional opportunities to our students and work hard for their bright future',
                {'entities': [(14, 34, 'Department_name')]}), (
                'The Department of Computer Sciences at Bahria University is home of quality education and multidisciplinary research',
                {'entities': [(18, 35, 'Department_name')]}), (
                'The BS Computer Science program provides understanding of the fundamental and advanced concepts.',
                {'entities': [(7, 24, 'Department_name')]}),
            (
                'The aim of the department is to pursue excellence in Computer Engineering through teaching and research and we are achieving our objectives with the help of our highly qualified and distinguished faculty of national and international repute.',
                {'entities': [(53, 73, 'Department_name')]}),
            (
                'Department of Computer Engineering is committed to excellence in teaching, research and inculcating a sense of pride and confidence in our students. We target to enhance not only their academic knowledge but to nurture their practical skills and provide professional grooming so that our students are ready to serve as they join industry and provide valuable contribution',
                {'entities': [(14, 35, 'Department_name')]}),
            (
                'Department of Computer Engineering endeavors to provide best learning and professional opportunities to our students and work hard for their bright future.',
                {'entities': [(14, 34, 'Department_name')]}),
            (
                'Department of Software Engineering aims to be recognized as a leader in Software Engineering education and research through excellence in modern education and targeted research in emerging areas of Software Engineering',
                {'entities': [(14, 34, 'Department_name')]}), (
                'The mission of Bachelor of Software Engineering program is to prepare technically strong Software Engineers who can contribute effectively towards the nation, society and the world at large through effective problem solving skills, application of engineering knowledge, leadership and healthy lifelong learning attitude.',
                {'entities': [(26, 47, 'Department_name')]}),
            (
                'Software Engineering department aims to deliver a strong and coherent Software Engineering program for the development of skilled Software Engineers. The curriculum is inline with PEC and HEC regulations to equip students with latest skills for industry and research activities. Software Engineering graduates should achieve the following educational objectives.',
                {'entities': [(0, 20, 'Department_name')]}),
            (
                'Graduates should demonstrate competence in applying Software Engineering knowledge & practices in various phases of software/system development life cycle in their respective professional career.',
                {'entities': [(52, 73, 'Department_name')]}),
            ('An ability to apply knowledge of computer science.',
             {'entities': [(33, 50, 'Department_name')]}),
            ('Software engineering fundamentals and an engineering specialization to the solution',
             {'entities': [(0, 20, 'Department_name')]}),
            ('Of complex software engineering problems', {'entities': [(11, 31, 'Department_name')]}),
            (
                'An ability to identify, formulate, research literature and analyze complex software engineering problems reaching substantiated conclusions using software engineering principles, natural sciences and engineering sciences',
                {'entities': [(75, 95, 'Department_name')]}), (
                'An ability to design solutions for complex software engineering problems and design systems, components or processes that meet specified needs with appropriate consideration for public health and safety, cultural, societal, and environmental considerations.',
                {'entities': [(43, 63, 'Department_name')]}),
            (
                'Programming language theory considers approaches to the description of computational processes, while software engineering involves the use of programming languages and complex systems',
                {'entities': [(102, 122, 'Department_name')]}),
            (
                'Computer science is the study of processes that interact with data and that can be represented as data in the form of programs. It enables the use of algorithms to manipulate, store, and communicate digital information. A computer scientist studies the theory of computation and the design of software systems',
                {'entities': [(0, 16, 'Department_name')]}), (
                'This branch of computer science aims to manage networks between computers worldwide',
                {'entities': [(15, 31, 'Department_name')]}),
            (
                'Open the door to sought-after technology careers with a world-class online Bachelor of Science (BSc) in Computer Science degree from the University of London.',
                {'entities': [(104, 120, 'Department_name')]}), (
                'The course material ranges from entry-level subjects to specialised topics. Hold a degree outside of computer science',
                {'entities': [(101, 117, 'Department_name')]}), (
                'Whether you have high school qualifications or experience working in a computer science field, earning a valuable degree helps move your career forward.',
                {'entities': [(70, 88, 'Department_name')]}),
            (
                'The course material ranges from entry-level subjects to specialised topics. If you already have a degree outside of computer science, the curriculum will bring you up-to-date on the latest industry applications and practices',
                {'entities': [(116, 132, 'Department_name')]}),
            (
                'With the BSc Computer Science, you can apply for a range of computational and mathematical jobs in the creative industries, business, finance, education, medicine, engineering and science',
                {'entities': [(13, 29, 'Department_name')]}),
            (
                'The University of London offers a number of online taster courses and Massive Open Online Courses (MOOCs), designed to introduce you to themes included in degree programmes. Choose from three open courses that explore topics covered in the BSc Computer Science degrees',
                {'entities': [(244, 260, 'Department_name')]}),
            (
                'No background in Computer science is required. If you satisfy the admissions requirements you will be admitted on to the course. Please see the admissions requirements for further information about the entry routes available.',
                {'entities': [(17, 33, 'Department_name')]}),
            ('Computer science students have excellent graduate prospects',
             {'entities': [(0, 16, 'Department_name')]}),
            ('Check out our Computer Science subject table, look down the Graduate Prospects column',
             {'entities': [(14, 30, 'Department_name')]}),
            (
                "Computer Science students stand a pretty good chance of being professionally employed, or in further study, within six months of leaving uni. And that chance is strengthened if you go to one of the UK's best unis for the subject",
                {'entities': [(0, 16, 'Department_name')]}),
            (
                'Computer science departments at typically benefit from having one of the more culturally diverse cohorts at their respective unis.',
                {'entities': [(0, 16, 'Department_name')]}),
            ('According to HESA data almost 20,000 computer science students come from overseas',
             {'entities': [(37, 54, 'Department_name')]}),
            (
                'Computers have gone global, and it would be silly for Computer Science education providers to not reflect this fact',
                {'entities': [(54, 70, 'Department_name')]}),
            (
                'A number of universities offer four-year undergraduate or integrated masters degrees (MSci) in computer science. Many also offer an opportunity to work in industry for a year or study abroad as part of the degree',
                {'entities': [(95, 111, 'Department_name')]}),
            (
                'Computer graphics is the study of digital visual contents and involves the synthesis and manipulation of image data. The study is connected to many other fields in computer science, including computer vision, image processing, and computational geometry, and is heavily applied in the fields of special effects and video games',
                {'entities': [(164, 180, 'Department_name')]}),
            (
                'Conferences are important events for computer science research. During these conferences, researchers from the public and private sectors present their recent work and meet',
                {'entities': [(36, 53, 'Department_name')]}),
            (
                'A number of universities offer four-year undergraduate or integrated masters degrees (MSci) in computer science. Many also offer an opportunity to work in industry for a year or study abroad as part of the degree',
                {'entities': [(95, 111, 'Department_name')]}),
            (
                'To get on to a computer science related degree you will usually require at least two A levels or equivalent.  Entry requirements range from CDD to AAA, with the universities and colleges most commonly asking for BBC',
                {'entities': [(15, 31, 'Department_name')]}),
            (
                'In addition to the different A level requirements above, you will also need at least five GCSEs (A-C) including science, English, and maths. Some universities require a maths GCSE for computer science degrees',
                {'entities': [(184, 200, 'Department_name')]}),
            (
                'Computer science is the study of processes that interact with data and that can be represented as data in the form of programs. It enables the use of algorithms to manipulate, store, and communicate digital information.',
                {'entities': [(0, 16, 'Department_name')]}),
            (
                'Software engineering is the systematic application of engineering approaches to the development of software.',
                {'entities': [(0, 20, 'Department_name')]}),
            (
                'Modern, generally accepted best-practices for software engineering have been collected by the ISO/IEC JTC 1/SC 7 subcommittee and published as the Software Engineering Body of Knowledge (SWEBOK)',
                {'entities': [(46, 66, 'Department_name')]}),
            ('The origins of the term "software engineering" have been attributed to various sources.',
             {'entities': [(25, 45, 'Department_name')]}),
            (
                'The term "software engineering" appeared in a list of services offered by companies in the June 1965 issue of COMPUTERS and AUTOMATION and was used more formally in the August 1966 issue of Communications of the ACM (Volume 9, number 8)',
                {'entities': [(10, 30, 'Department_name')]}),
            (
                'ACM membership by the ACM President Anthony A. Oettinger;,[8] it is also associated with the title of a NATO conference in 1968 by Professor Friedrich L. Bauer, the first conference on software engineering',
                {'entities': [(186, 206, 'Department_name')]}),
            (
                'Independently, Margaret Hamilton named the discipline "software engineering" during the Apollo missions to give what they were doing legitimacy',
                {'entities': [(55, 75, 'Department_name')]}),
            (
                'At the time there was perceived to be a "software crisis".[11][12][13] The 40th International Conference on Software Engineering (ICSE 2018) celebrates 50 years',
                {'entities': [(108, 128, 'Department_name')]}),
            (
                'Modern, generally accepted best-practices for software engineering have been collected by the ISO/IEC JTC 1/SC 7 subcommittee and published as the Software Engineering Body of Knowledge (SWEBOK)',
                {'entities': [(46, 66, 'Department_name')]}),
            (
                'Electrical engineering is an engineering discipline concerned with the study, design and application of equipment, devices and systems which use electricity, electronics, and electromagnetism',
                {'entities': [(0, 22, 'Department_name')]}),
            (
                'However, the design of complex software systems is often the domain of software engineering, which is usually considered a separate discipline',
                {'entities': [(71, 91, 'Department_name')]}),
            ('Jalote, Pankaj (31 January 2006). An Integrated Approach to Software Engineering',
             {'entities': [(60, 80, 'Department_name')]}),
            (
                'Software engineering is an engineering branch associated with development of software product using well-defined scientific principles, methods and procedures',
                {'entities': [(0, 20, 'Department_name')]}),
            ('Let us first understand what software engineering stands for',
             {'entities': [(29, 49, 'Department_name')]}),
            (
                'Software engineering is an engineering branch associated with development of software product using well-defined scientific principles, methods and procedures.',
                {'entities': [(0, 20, 'Department_name')]}),
            ('The outcome of software engineering is an efficient and reliable software product',
             {'entities': [(15, 35, 'Department_name')]}),
            (
                'Software engineering is the establishment and use of sound engineering principles in order to obtain economically software that is reliable and work efficiently on real machines.',
                {'entities': [(0, 20, 'Department_name')]}),
            (
                'The process of developing a software product using software engineering principles and methods is referred to as software evolution',
                {'entities': [(51, 71, 'Department_name')]}),
            (
                'There are many methods proposed and are in work today, but we need to see where in the software engineering these paradigms stand',
                {'entities': [(87, 107, 'Department_name')]}),
            (
                'This Paradigm is known as software engineering paradigms where all the engineering concepts pertaining to the development of software are applied. It includes various researches and requirement gathering which helps the software product to build',
                {'entities': [(26, 46, 'Department_name')]}),
            (
                'The need of software engineering arises because of higher rate of change in user requirements and environment on which the software is working',
                {'entities': [(12, 32, 'Department_name')]}),
            (
                'The always growing and adapting nature of software hugely depends upon the environment in which user works. If the nature of software is always changing, new enhancements need to be done in the existing one. This is where software engineering plays a good role',
                {'entities': [(222, 242, 'Department_name')]}),
            (
                'In short, Software engineering is a branch of computer science, which uses well-defined engineering concepts required to produce efficient, durable, scalable, in-budget and on-time software products',
                {'entities': [(10, 30, 'Department_name')]}),
            (
                'Software Development Life Cycle, SDLC for short, is a well-defined, structured sequence of stages in software engineering to develop the intended software product',
                {'entities': [(101, 121, 'Department_name')]}),
            (
                'Software engineering is defined as a process of analyzing user requirements and then designing, building, and testing software application which will satisfy those requirements',
                {'entities': [(0, 20, 'Department_name')]}),
            (
                'IEEE, in its standard 610.12-1990, defines software engineering as the application of a systematic, disciplined, which is a computable approach for the development, operation, and maintenance of software.',
                {'entities': [(43, 63, 'Department_name')]}),
            (
                "Boehm defines software engineering, which involves, 'the practical application of scientific knowledge to the creative design and building of computer programs. It also includes associated documentation needed for developing, operating, and maintaining them",
                {'entities': [(14, 34, 'Department_name')]}),
            (
                'Solution was to the problem was transforming unorganized coding effort into a software engineering discipline',
                {'entities': [(78, 98, 'Department_name')]}),
            ('The late 1970s saw the widespread uses of software engineering principles',
             {'entities': [(42, 62, 'Department_name')]}),
            (
                'Whenever the software process was based on scientific and engineering, it is easy to re-create new software with the help of software engineering',
                {'entities': [(125, 145, 'Department_name')]}),
            (
                'In this sector, software engineering helps you in resource estimation and cost control. Computing system must be developed, and data should be maintained regularly within a given budget',
                {'entities': [(16, 36, 'Department_name')]}),
            (
                'Software engineering is labor-intensive work which demands both technical and managerial control. Therefore, it is widely used in management science',
                {'entities': [(0, 20, 'Department_name')]}),
            (
                'Most software is a component of a much larger system. For example, the software in an Industry monitoring system or the flight software on an airplane. Software engineering methods should be applied to the study of this type of systems',
                {'entities': [(152, 172, 'Department_name')]}),
            (
                'Software engineering is a process of analyzing user requirements and then designing, building, and testing software application which will satisfy that requirements',
                {'entities': [(0, 20, 'Department_name')]}),
            (
                'Important reasons for using software engineering are: 1) Large software, 2) Scalability 3) Adaptability 4) Cost and 5) Dynamic Nature',
                {'entities': [(28, 48, 'Department_name')]}),
            ('The late 1970s saw the widespread uses of software engineering principles',
             {'entities': [(42, 62, 'Department_name')]}),
            (
                'Increased market demands for fast turnaround time is the biggest challenges of software engineering field',
                {'entities': [(79, 106, 'Department_name')]}),
            (
                'A backlash against the overemphasis of processes in software development resulted in a group of software engineering consultants publishing the Manifesto for Agile Software Development',
                {'entities': [(96, 116, 'Department_name')]}),
            (
                'In this millennium, researchers in software engineering have performed numerous studies linking software metrics to post-release failures',
                {'entities': [(34, 55, 'Department_name')]}),
            (
                'V&V tasks should be performed by a team of senior software personnel lead by a member of the software engineering team',
                {'entities': [(93, 113, 'Department_name')]}),
            (
                'The software engineering literature has stressed the importance of software development processes and their influence on product quality for decades [2,4]',
                {'entities': [(4, 25, 'Department_name')]}),
            ('A. Bener, ... E. Kocaguneli, in Perspectives on Data Science for Software Engineering, 2016',
             {'entities': [(65, 85, 'Department_name')]}),
            (
                'Software engineering is more than just programming. It includes computer science, project management, engineering and other spheres. This lesson will discuss the different processes involved in it and the common methods used in developing software',
                {'entities': [(0, 20, 'Department_name')]}),
            ('You just applied the principles of software engineering to your business',
             {'entities': [(35, 55, 'Department_name')]}),
            (
                "Software engineering essentially follows the same steps. The only difference is that you are running a 'software' business instead of a card business",
                {'entities': [(0, 20, 'Department_name')]}),
            ('The end result of software engineering is a streamlined and reliable software product',
             {'entities': [(18, 38, 'Department_name')]}),
            ("Let's take a look at each of the steps involved in a typical software engineering process",
             {'entities': [(61, 81, 'Department_name')]}),
            (
                'Graduates of University of Marylands Computer Science Department are lifetime learners; they are able to adapt quickly with this challenging field',
                {'entities': [(38, 54, 'Department_name')]}),
            (
                'In a nutshell, computer science degrees deal with the theoretical foundations of information and computation, taking a scientific and practical approach to computation and its applications',
                {'entities': [(15, 32, 'Department_name')]}),
            (
                'Computer science is considered by many of its practitioners to be a foundational science - one which makes other knowledge and achievements possible',
                {'entities': [(0, 16, 'Department_name')]}),
            (
                'The study of computer science involves systematically studying methodical processes (such as algorithms) in order to aid the acquisition, representation, processing, storage, communication of, and access to information',
                {'entities': [(13, 29, 'Department_name')]}),
            (
                'This is done by analyzing the feasibility, structure, expression and mechanization of these processes and how they relate to this information. In computer science, the term information refers usually to information which is encoded in bits and bytes in computer memory',
                {'entities': [(146, 162, 'Department_name')]}),
            ('You may also find the term computer science', {'entities': [(27, 43, 'Department_name')]}),
            (
                'used to refer to information technology (IT) degrees, although many institutions now distinguish between the two (exactly how and where they draw this line varies)',
                {'entities': [(17, 39, 'Department_name')]}),
            (
                'The QS World University Rankings by Subject includes a ranking of the worlds top universities for computer science',
                {'entities': [(99, 115, 'Department_name')]}),
            (
                'Entry requirements for computer science degrees usually emphasize further mathematics, with some institutions asking for a background in physics',
                {'entities': [(23, 39, 'Department_name')]}),
            (
                'Some institutions offer joint courses, in which computer science is studied alongside subjects such as mathematics, engineering and computing',
                {'entities': [(48, 64, 'Department_name')]}),
            (
                'If you like solving problems and have a talent for mathematics and logical thinking, a degree in computer science could be the start of a rewarding career',
                {'entities': [(97, 113, 'Department_name')]}),
            (
                'Computer science degrees are structured in an incremental way, starting by giving students an overview of the basic principles',
                {'entities': [(0, 16, 'Department_name')]}),
            (
                'There is also likely to be some teaching about where modern computer science fits into society, either the history of the discipline, or a module on business or enterprise in the context of computer science',
                {'entities': [(60, 76, 'Department_name')]}),
            (
                'If you want to study computer science at university you must be creative, diligent and strong in maths',
                {'entities': [(21, 37, 'Department_name')]}),
            (
                'Most universities look for top marks in subjects like IT, computing, physics or further maths from applicants',
                {'entities': [(53, 56, 'Department_name')]}),
            (
                'Therfore are many reasons that computer science is so popular, including exceptional job security, uncommonly high starting salaries, and diverse job opportunities across industries',
                {'entities': [(31, 47, 'Department_name')]}),
            (
                'Due to the distinction between computers and computing, some of the research groups refer to computing or datalogy. The French refer to computer science as the term informatique',
                {'entities': [(136, 152, 'Department_name')]}),
            (
                'Informatics is also distinct from computer science, which encompasses the study of logic and low-level computing issues',
                {'entities': [(34, 50, 'Department_name')]}),
            (
                'Universities may confer degrees of ICS and CIS, not to be confused with a more specific Bachelor of Computer Science or respective graduate',
                {'entities': [(100, 116, 'Department_name')]}),
            (
                'The QS World University Rankings is one of the most widely recognised and distinguished university comparisons. They ranked the top 10 universities for computer science and information systems in 2015',
                {'entities': [(152, 168, 'Department_name')]}),
            (
                'Due the nature of this field, many topics are also shared with computer science and information systems',
                {'entities': [(62, 79, 'Department_name')]}),
            ('The discipline of Information and Computer Science spans a vast range of areas from basic',
             {'entities': [(34, 50, 'Department_name')]}),
            (
                'computer science theory (algorithms and computational logic) to in depth analysis of data manipulation and use within technology',
                {'entities': [(0, 16, 'Department_name')]}),
            (
                'and its predicted in the US that in the next decade there will be more than one million jobs in the technology sector than computer science graduates to fill them',
                {'entities': [(124, 140, 'Department_name')]}),
            (
                'f you see yourself designing and creating software systems, then computer science might be the right course of study for you. If you are thinking of becoming a manager or administrator to a technical enterprise',
                {'entities': [(65, 81, 'Department_name')]}),
            (
                'Computer science is a dynamic and rapidly growing area that has become an integral part of the world that we live in today. Having a degree in this field will provide you with a deep understanding of theories and emerging technologies',
                {'entities': [(0, 16, 'Department_name')]}),
            (
                'you may not become a billionaire in computer science there are only so many Steves Jobs and Bill Gates in the world but, since its specialized knowledge and challenging skills, salaries tend to be solidly high.',
                {'entities': [(36, 52, 'Department_name')]}),
            (
                'Before entering an information technology program, prospective students will wonder if a computer science degree is worth it',
                {'entities': [(19, 41, 'Department_name')]}),
            ('Over the last twenty years, the field of computer science has grown exponentially',
             {'entities': [(41, 57, 'Department_name')]}),
            (
                'The median wage for those in the computer science industry is $86,320 annually, according to the Bureau of Labor Statistics. Jobs in the industry are expected to experience a growth of at least 14% over the next decade with as many as 557,000 new jobs being created',
                {'entities': [(33, 49, 'Department_name')]}),
            ('A computer science degree is worth it since technology is consistently evolving',
             {'entities': [(2, 18, 'Department_name')]}),
            (
                'New specializations are always opening in the field of computer science as new technological advancements are made',
                {'entities': [(55, 71, 'Department_name')]}),
            ('Potential job opportunities for computer science degree holders include',
             {'entities': [(31, 49, 'Department_name')]}),
            (
                'Several jobs in the computer science field will have a masters degree requirement. For these jobs, median salaries will be upwards of $115,000 per year',
                {'entities': [(19, 36, 'Department_name')]}),
            ('It is possible to launch a career in the field of computer science with an associates degree',
             {'entities': [(50, 66, 'Department_name')]}),
            (
                'Associate degree programs will teach students both hard and soft skills needed for the IT workforce',
                {'entities': [(87, 89, 'Department_name')]}),
            (
                'n some incidences, an employer may not even ask for a college degree, but instead, look exclusively at past job experience and any certifications earned related to computer science',
                {'entities': [(164, 180, 'Department_name')]}),
            (
                'Computer science degree programs are being offered more and more online. Online degrees are widely accepted as long as they are earned from an accredited college or university',
                {'entities': [(0, 16, 'Department_name')]}),
            (
                'Any school chosen by the prospective computer science student should have the proper accreditation in order to successfully secure a position post-graduation',
                {'entities': [(37, 53, 'Department_name')]}),
            (
                ' An accredited computer science degree online will have the same value as a traditional program. Non-accredited programs may disqualify the applicant from a position',
                {'entities': [(15, 31, 'Department_name')]}),
            ('The following are frequently asked questions regarding computer science accreditation',
             {'entities': [(55, 71, 'Department_name')]}),
            (
                'Online programs have a separate accreditation process than traditional computer science and engineering types',
                {'entities': [(71, 87, 'Department_name')]}),
            (
                'Many employers are now requiring new hires in the field of computer science to have graduated from ABET-accredited program',
                {'entities': [(59, 75, 'Department_name')]}),
            (
                'The STEM field is looking for a global standard to determine if college graduates have the technical prowess to succeed in the industry. ABET programs confirm job readiness for computer science students',
                {'entities': [(177, 193, 'Department_name')]}),
            (
                ' Along with computer science programs, ABET accredits engineering and applied/natural science programs',
                {'entities': [(12, 29, 'Department_name')]}),
            (
                'Computer science degree requirements will also include general education classes in math, history, philosophy, writing, and more',
                {'entities': [(0, 16, 'Department_name')]}),
            (
                'Students should look at specialization options as well as accreditation to narrow down the best undergraduate computer science schools',
                {'entities': [(110, 126, 'Department_name')]}),
            (
                'Instead of a general overview, the master degree program will delve into advanced computer science topics',
                {'entities': [(82, 98, 'Department_name')]}),
            (
                'A technology firm could choose to send employees for a computer science degree online allowing the worker to take courses in the evenings and weekends',
                {'entities': [(55, 71, 'Department_name')]}),
            (
                'Types of computer science degrees at the graduate level include database systems, homeland security',
                {'entities': [(9, 25, 'Department_name')]}),
            (
                'Accelerated computer science degree programs may be finished in one year or less, but have a larger per semester course load',
                {'entities': [(12, 28, 'Department_name')]}),
            (
                'Computer science degree types include traditional, hybrid, and online. Traditional degree tracks require that students attend courses exclusively on campus',
                {'entities': [(0, 16, 'Department_name')]}),

            (
                ' Online computer science degrees are 100 percent online. In some cases, the student may only have a weekend campus visit requirement once or twice a year',
                {'entities': [(8, 24, 'Department_name')]}),
            (
                'Most aspects of computer science can be learned anywhere, which means that theres nothing inherently better about a traditional residential program over an online program',
                {'entities': [(16, 32, 'Department_name')]}),
            (
                'A computer science certificate online program may have pre-requisites before a person can complete it',
                {'entities': [(2, 18, 'Department_name')]}),
            (
                " Considering these factors, it's no wonder that you consider studying Computer Science or Information Technology degree",
                {'entities': [(70, 86, 'Department_name')]}),
            (
                'Choosing your studies can be a tough choice, with this guide we hope to help you decide if you want to study Computer Science',
                {'entities': [(109, 125, 'Department_name')]}),
            (
                'Although there is some overlap. When you study Computer Science you will learn to design and develop computer programs, applications and software',
                {'entities': [(47, 63, 'Department_name')]}),
            (
                'Being able to find a job after graduating is something a lot of people are struggling with. Good news, this is not the case for people with a degree in Computer Science',
                {'entities': [(152, 168, 'Department_name')]}),
            (
                'Computer engineering (CE) is a branch of engineering that integrates several fields of required to develop computer hardware and software',
                {'entities': [(0, 20, 'Department_name')]}),
            (
                'In many institutions of higher learning, computer engineering students are allowed to choose areas of in-depth study in their junior and senior year because the full breadth of knowledge used in the design and application of computers is beyond the scope of an undergraduate degree',
                {'entities': [(41, 62, 'Department_name')]}),
            (
                'The first computer engineering degree program in the United States was established in 1971 at Case Western Reserve University in Cleveland, Ohio',
                {'entities': [(10, 30, 'Department_name')]}),
            (
                "some tertiary institutions around the world offer a bachelor's degree generally called computer engineering",
                {'entities': [(87, 108, 'Department_name')]}),
            (
                'Both computer engineering and electronic engineering programs include analog and digital circuit design in their curriculum',
                {'entities': [(5, 25, 'Department_name')]}),
            ("Most entry-level computer engineering jobs require at least a bachelor's degree in computer",
             {'entities': [(17, 37, 'Department_name')]}),
            ('computer engineering (ECE) and has been divided into many subcategories',
             {'entities': [(0, 20, 'Department_name')]}),
            (
                'Computer Engineering is generally practiced within larger product development firms, and such practice may not be subject to licensing',
                {'entities': [(0, 21, 'Department_name')]}),
            (
                ' offered a Principles and Practice of Engineering Examination for Computer Engineering[33] in 2003',
                {'entities': [(65, 86, 'Department_name')]}),
            ('There are many specialty areas in the field of computer engineering',
             {'entities': [(47, 67, 'Department_name')]}),
            (
                'This specialty of computer engineering requires adequate knowledge of electronics and electrical systems',
                {'entities': [(18, 38, 'Department_name')]}),
            (
                'computer embedded computer engineering specializations include system-on-chip design, architecture of edge computing and the Internet of things',
                {'entities': [(18, 38, 'Department_name')]}),
            ('Media related to Computer engineering at Wikimedia Commons',
             {'entities': [(17, 37, 'Department_name')]}),
            ('IT is the use of computers to store, retrieve, transmit, and manipulate data[1] or information',
             {'entities': [(0, 2, 'Department_name')]}),
            (
                'IT is typically used within the context of business operations as opposed to personal or entertainment technologies',
                {'entities': [(0, 2, 'Department_name')]}),
            ('IT is considered to be a subset of information and communications technology (ICT)',
             {'entities': [(0, 2, 'Department_name')]}),
            ('We shall call it IT', {'entities': [(17, 19, 'Department_name')]}), (
                'is possible to distinguish four distinct phases of IT development',
                {'entities': [(51, 54, 'Department_name')]}),
            ('As the IT industry evolved from the mid-20th', {'entities': [(7, 9, 'Department_name')]}),
            ('can be included in the IT domain', {'entities': [(23, 25, 'Department_name')]}),
            ('IT architectures have evolved to include virtualization and cloud computing',
             {'entities': [(0, 2, 'Department_name')]}),
            ('Clouds may be distributed across locations and shared with other IT users',
             {'entities': [(65, 67, 'Department_name')]}),
            ('IT teams depend on a wide range of specialized information.',
             {'entities': [(0, 2, 'Department_name')]}),
            ('vendor support personnel augment the IT team', {'entities': [(37, 39, 'Department_name')]}),
            ('Information Technology includes several layers of physical equipment',
             {'entities': [(0, 22, 'Department_name')]}),
            ('Information Technology teams depend on a wide range of specialized',
             {'entities': [(0, 22, 'Department_name')]}),
            ('Information technology is the use of any computers, storage',
             {'entities': [(0, 22, 'Department_name')]}),
            ('The term information technology was coined by the Harvard Business Review',
             {'entities': [(9, 31, 'Department_name')]}),
            (
                'For many people, information technology is basically synonymous with the guys and gals you call when you need help with a computer issue',
                {'entities': [(17, 39, 'Department_name')]}),
            (
                'While that view of information technology isnt totally wrong, it drastically understates the scope of this critical career field',
                {'entities': [(19, 42, 'Department_name')]}),
            ('If youre looking to get a better handle on what information technology is',
             {'entities': [(49, 71, 'Department_name')]}),
            ("The most basic information technology definition is that it's the application",
             {'entities': [(15, 37, 'Department_name')]}),
            ('There are three primary pillars of responsibility for an IT department',
             {'entities': [(57, 59, 'Department_name')]}),
            ('No matter the role, a member of an IT department works',
             {'entities': [(35, 38, 'Department_name')]}),
            ('computer and information technology occupations is projected to grow',
             {'entities': [(13, 35, 'Department_name')]}),
            ('those in information technology need to have a level of empathy',
             {'entities': [(9, 31, 'Department_name')]}),
            (
                'Now that youve got a better handle on the basics of what information technology is and the important nature of the field',
                {'entities': [(58, 80, 'Department_name')]}),
            ('The information technology profession is extremely diverse',
             {'entities': [(4, 26, 'Department_name')]}),
            ('This person examines and changes IT functions to best support the business.',
             {'entities': [(33, 35, 'Department_name')]}),
            ('What is changing today about information technology roles?',
             {'entities': [(29, 51, 'Department_name')]}),
            ("Today's IT professionals need to be quicker to respond to new technologies",
             {'entities': [(8, 10, 'Department_name')]}),
            ('Hii sir!, am finding for the IT technician to help me some things can you help me',
             {'entities': [(29, 31, 'Department_name')]}),
            (
                "I'm doing my research for how information technology has developed and contributed to shaping our society today and this article helped a lot",
                {'entities': [(30, 53, 'Department_name')]}),
            ('Sir, please tell me the definition of Information Technology',
             {'entities': [(38, 60, 'Department_name')]}),
            ('Now a days, what is Information Technology', {'entities': [(20, 42, 'Department_name')]}),
            ('Programming and Information Technology should understand the objectives of the business',
             {'entities': [(16, 38, 'Department_name')]}),
            ('Information Technology is devising more user-friendly and supporting system',
             {'entities': [(0, 22, 'Department_name')]}),
            ('one day become a chief officer of Information Technology',
             {'entities': [(34, 56, 'Department_name')]}),
            ('am in Tanzania i need to know much about IT', {'entities': [(40, 43, 'Department_name')]}),
            (
                'i am in Kenya wanted to learner about Information Technology hoping that you will assist me thank you',
                {'entities': [(38, 60, 'Department_name')]}),
            ('I want to know what is infromation technology', {'entities': [(23, 46, 'Department_name')]}),
            ('our new technics, that is information technology', {'entities': [(26, 48, 'Department_name')]}),
            ('Thank you Margaret, because IT is my career', {'entities': [(28, 30, 'Department_name')]}),
            ('CS is the study of processes that interact with data',
             {'entities': [(0, 3, 'Department_name')]}),
            ('A CS studies the theory of computation and the design',
             {'entities': [(2, 4, 'Department_name')]}),
            ('the term CS appears in a 1959 article in Communications of the ACM',
             {'entities': [(8, 11, 'Department_name')]}),
            ('Graduate School in CS analogous to the creation of Harvard Business School in 1921',
             {'entities': [(19, 22, 'Department_name')]}),
            ('funding aspects of CS tend to depend on whether a department.',
             {'entities': [(19, 21, 'Department_name')]}),
            ('which treats CS as a branch of mathematics.', {'entities': [(12, 15, 'Department_name')]}),
            ('CS focuses on methods involved in design', {'entities': [(0, 2, 'Department_name')]}),
            ('As a discipline, CS spans a range of topics from theoretical studies of algorithms',
             {'entities': [(17, 19, 'Department_name')]}),
            ('Theoretical CS is mathematical and abstract in spirit',
             {'entities': [(12, 15, 'Department_name')]}),
            ('the fundamental question underlying CS', {'entities': [(36, 38, 'Department_name')]}),
            ('It falls within the discipline of CS both depending on and affecting',
             {'entities': [(34, 36, 'Department_name')]}),
            ('the application of a fairly broad variety of theoretical CS fundamentals',
             {'entities': [(57, 59, 'Department_name')]}),
            (
                'The study is connected to many other fields in cs', {'entities': [(47, 49, 'Department_name')]}),
            ('The philosopher of computing Bill Rapaport noted three Great Insights of cs',
             {'entities': [(73, 75, 'Department_name')]}),
            ('Further information List of cs conferences', {'entities': [(28, 31, 'Department_name')]}),
            ('Unlike in most other academic fields, in cs', {'entities': [(41, 43, 'Department_name')]}),
            ('cs to A level students', {'entities': [(0, 2, 'Department_name')]}),
            ('and South Korea have included cs in their national secondary education curricula',
             {'entities': [(30, 32, 'Department_name')]}),
            ('states have adopted significant education standards for high school cs',
             {'entities': [(68, 70, 'Department_name')]}),
            ('In many countries, there is a significant gender gap in cs education',
             {'entities': [(56, 58, 'Department_name')]}),
            ('See the entry cs on Wikiquote for the history of this quotation',
             {'entities': [(14, 16, 'Department_name')]}),
            ('The problems that cs encounter range from the abstract',
             {'entities': [(18, 20, 'Department_name')]}),
            ('Graduates of University of Marylands cs Department',
             {'entities': [(38, 41, 'Department_name')]}),
            (
                'Accounting & Finance is a highly specialised degree, preparing the graduate as having expertise',
                {'entities': [(0, 21, 'Department_name')]}),
            ('opportunities in accounting and finance than many other areas of study',
             {'entities': [(17, 39, 'Department_name')]}),
            ('Accounting & Finance program is aimed at giving students a solid foundation',
             {'entities': [(0, 20, 'Department_name')]}),
            (
                'in accounting and finance, rounded out with the all-important interpersonal, computer, and business communication skills',
                {'entities': [(2, 25, 'Department_name')]}), (
                'Accounting & Finance is a four-year degree program and consists of 130-136 credit hours of study',
                {'entities': [(0, 20, 'Department_name')]}),
            ('Accounting and Finance  was are the an ACCA accredited program',
             {'entities': [(0, 22, 'Department_name')]}),
            ('Accounting And Finance is an accredited program googing on in this session',
             {'entities': [(0, 23, 'Department_name')]}),
            ('The course is a blend of theory and practice of accounting and finance',
             {'entities': [(48, 70, 'Department_name')]}),
            ('Accounting and Finance program consist of four or five-course units per semester',
             {'entities': [(0, 22, 'Department_name')]}),
            (
                'Accounting & Finance are the most significant and critical areas in the system of free enterprise',
                {'entities': [(0, 21, 'Department_name')]}),
            (
                'The BS Accounting & Finance program is designed to prepare students to meet the challenges posed by this complex',
                {'entities': [(7, 27, 'Department_name')]}),
            (
                'BS Accounting & Finance is tailored to first impart a broad-based education in the fundamentals of business',
                {'entities': [(3, 24, 'Department_name')]}),
            ('Accounting & Finance degree, a student must have', {'entities': [(0, 20, 'Department_name')]}),
            (
                'A major in Accounting and Finance (ACF) in B.Sc. (Hons) provides students with a basis from which to continue',
                {'entities': [(11, 33, 'Department_name')]}),
            (
                'At this time, students can follow a set of pre-identified courses to simultaneously complete professional certifications with their B.Sc. (Hons) Degree in Accounting and Finance',
                {'entities': [(155, 177, 'Department_name')]}),
            ('At the heart of accounting and financial  is the system known as double entry',
             {'entities': [(16, 40, 'Department_name')]}),
            (
                'The bachelor degree program in Accounting and Finance prepares students for entry-level positions',
                {'entities': [(31, 53, 'Department_name')]}),
            ('The degree provides a strong foundation for a successful career in accounting and finance',
             {'entities': [(67, 89, 'Department_name')]}),
            (
                'To make students able to understand and develop the skills to grasp broad range of accounting and finance techniques and concepts',
                {'entities': [(83, 105, 'Department_name')]}),
            (
                'To provide the knowledge and skills to students for using computer technology in accounting and finance for the purpose of improving decision making in an organization setting',
                {'entities': [(81, 103, 'Department_name')]}),
            (
                'To provide an opportunity for students to evaluate problems and innovations in accounting and finance with effects on managerial decision making',
                {'entities': [(79, 101, 'Department_name')]}), (
                'To make them able to apply integrated techniques of accounting and finance in evaluating the costs and benefits of strategic investments',
                {'entities': [(52, 74, 'Department_name')]}), (
                'To develop the understanding about ethical issues in Accounting And Finance',
                {'entities': [(53, 76, 'Department_name')]}), (
                'To mentor students to exploit newly created opportunities in Accounting And Finance profession',
                {'entities': [(61, 83, 'Department_name')]}), (
                'Students are required to complete a Project/ Internship Report in the final semester of their BS in Accounting and Finance program',
                {'entities': [(100, 122, 'Department_name')]}),
            (
                'Accounting and Finance intends to prepare students in professional accounting and financial management',
                {'entities': [(0, 22, 'Department_name')]}),
            ('This programme covers the major tools and theories of ACCOUNTING & FINANCE',
             {'entities': [(54, 75, 'Department_name')]}),
            ('The BSc ACCOUNTING & FINANCE programme is primarily designed for students who are interested',
             {'entities': [(8, 28, 'Department_name')]}),
            ('then ACCOUNTING & FINANCE is the perfect career path for you',
             {'entities': [(5, 25, 'Department_name')]}),
            (
                'Tri-city is the residence of many companies offering international ACCOUNTING & FINANCE services',
                {'entities': [(67, 87, 'Department_name')]}),
            (
                'Develop specialist ACCOUNTING & FINANCE skills, and learn to apply them in an organisational context',
                {'entities': [(19, 39, 'Department_name')]}),
            ('Finance & Accounting Level are Undergraduate program',
             {'entities': [(0, 20, 'Department_name')]}),
            ('Our specialised ACCOUNTING & FINANCE degree aims to improve employability',
             {'entities': [(16, 36, 'Department_name')]}),
            (
                'Lincolns ACCOUNTING & FINANCE degree aims to equip students with vocationally relevant and academically rigorous education in a programmer',
                {'entities': [(10, 31, 'Department_name')]}),
            (
                'Students are required to complete 46 courses and a 6 credit hours of ?nal year project ACCOUNTING AND FINANCE',
                {'entities': [(87, 110, 'Department_name')]}),
            (
                'This programme covers the major tools and differnt universites doing that theories of ACCOUNTING AND FINANCE is impotrant in universities',
                {'entities': [(86, 108, 'Department_name')]}),
            ('Our main purpose is specialised ACCOUNTING AND FINANCE degree aims do that about it',
             {'entities': [(32, 54, 'Department_name')]}),
            (
                'To mentor students is get and many of the energy to exploit newly created opportunities in ACCOUNTING AND FINANCE  profession',
                {'entities': [(91, 113, 'Department_name')]}),
            (
                'ACCOUNTING AND FINANCE make them able to apply integrated techniques of  in different universities',
                {'entities': [(0, 22, 'Department_name')]}),
            (
                'A major in ACCOUNTING AND FINANCE (ACF) in B.Sc. (Hons) provides students with a basis from which the sytem that not really the gone',
                {'entities': [(11, 33, 'Department_name')]}),
            ('COMPUTER SCIENCES design and analyze algorithms to solve the problems',
             {'entities': [(0, 17, 'Department_name')]}),
            (
                'The course material ranges from entry-level subjects to specialised topics. Hold a degree outside of COMPUTER SCIENCES',
                {'entities': [(101, 118, 'Department_name')]}),
            ('Students who earn a BA in COMPUTER SCIENCES must complete at least five courses',
             {'entities': [(25, 43, 'Department_name')]}),
            (
                'Students majoring in COMPUTER SCIENCES may not earn a second major or a minor in business analytics and information systems',
                {'entities': [(21, 38, 'Department_name')]}),
            (
                'Welcome to the Electrical Engineering Department (EED) at Information Technology University (ITU), Lahore',
                {'entities': [(15, 37, 'Department_name')]}),
            (
                'The Department of Electrical Engineering has a carefully designed curriculum which offers a wide range of knowledge',
                {'entities': [(18, 40, 'Department_name')]}),
            (
                'highlight that both Higher Education Commission (HEC) and Pakistan Engineering Council (PEC) recognize BS in electrical engineering program at ITU',
                {'entities': [(109, 131, 'Department_name')]}),
            (
                'The Program Educational Objectives (PEO) of the BS in Electrical Engineering program are as under',
                {'entities': [(54, 76, 'Department_name')]}),
            (
                'To produce creative graduates with core electrical engineering concepts to embark on real-world challenges',
                {'entities': [(40, 62, 'Department_name')]}),
            (
                'The mission of School of Electrical Engineering is to provide graduates with a strong and stable foundation',
                {'entities': [(25, 48, 'Department_name')]}),
            (
                'To inculcate graduates with technical competence through advanced and comprehensive knowledge of the practical aspect of electrical engineering, including analytical and design skills and of the technical tools to meet the engineering requirements',
                {'entities': [(120, 143, 'Department_name')]}),
            (
                'To provide an undergraduate education that will further enable qualified students to pursue Graduate/Higher studies in electrical engineering and related fields',
                {'entities': [(119, 141, 'Department_name')]}),
            ('This versatile degree opens careers in different areas of electrical engineering',
             {'entities': [(58, 80, 'Department_name')]}),
            ('For the award of BS Electrical Engineering degree, a student must have',
             {'entities': [(20, 43, 'Department_name')]}),
            (
                'engineering specialization Electrical Engineering to the solution of complex engineering problems',
                {'entities': [(27, 49, 'Department_name')]}),
            (
                'An ability to design solutions in the domain of Electrical Engineering for complex engineering problems',
                {'entities': [(48, 70, 'Department_name')]}),
            (
                'Electrical engineering is an engineering discipline concerned with the study, design and application of equipment',
                {'entities': [(0, 22, 'Department_name')]}),
            ('Electrical engineering is now divided into a wide range of fields including',
             {'entities': [(0, 22, 'Department_name')]}),
            (
                'The IEC prepares international standards for electrical engineering, developed through consensus',
                {'entities': [(45, 67, 'Department_name')]}),
            (
                'Electrical engineerings work in a very wide range of industries and the skills required are likewise variable',
                {'entities': [(0, 23, 'Department_name')]}),
            ('soon to be renamed the Institution of Electrical Engineering',
             {'entities': [(38, 60, 'Department_name')]}),
            (
                "the world's first department of electrical engineering in 1882 and introduced the first degree course",
                {'entities': [(32, 54, 'Department_name')]}),
            (
                'The first electrical engineering degree program in the United States was started at Massachusetts Institute of Technology (MIT) in the physics department',
                {'entities': [(10, 32, 'Department_name')]}),
            (
                'Weinbach at University of Missouri soon followed suit by establishing the electrical engineering department in 1886',
                {'entities': [(74, 96, 'Department_name')]}),
            ('started to offer electrical engineering programs to their students all over the world',
             {'entities': [(17, 39, 'Department_name')]}),
            ('During these decades use of ELECTRICAL ENGINEERING increased dramatically',
             {'entities': [(28, 50, 'Department_name')]}),
            ('ELECTRICAL ENGINEERING has many subdisciplines, the most common of which are listed below',
             {'entities': [(0, 23, 'Department_name')]}),
            (
                'the main aim of ELECTRICAL ENGINEERING may use electronic circuits, digital signal processors, microcontrollers, and programmable logic controllers (PLCs)',
                {'entities': [(16, 38, 'Department_name')]}),
            (
                'ELECTRICAL ENGINEERING involves the design and testing of electronic circuits that use the properties of components such as resistors',
                {'entities': [(0, 22, 'Department_name')]}),
            (
                'In the mid-to-late 1950s, the term radio engineering gradually gave way to the name ELECTRICAL ENGINEERING',
                {'entities': [(84, 107, 'Department_name')]}),
            (
                'The field of ELECTRICAL ENGINEERING involves a significant amount of chemistry and material science and requires the electronic engineer',
                {'entities': [(13, 35, 'Department_name')]}),
            (
                'he most common microelectronic components are semiconductor transistors, although all main ELECTRICAL ENGINEERING',
                {'entities': [(91, 114, 'Department_name')]}),
            ('The term mechatronics is typically used to refer to ELECTRICAL ENGINEERING macroscopic system',
             {'entities': [(52, 74, 'Department_name')]}),
            ('SOFTWARE ENGINEERING is the process of analyzing user needs and designing, constructing',
             {'entities': [(0, 20, 'Department_name')]}),
            (
                'Furthermore may SOFTWARE ENGINEERING involve the process of analyzing existing software and modifying it to meet current application needs',
                {'entities': [(16, 36, 'Department_name')]}),
            (
                'There must be discipline and control during SOFTWARE ENGINEERING, much like any complex engineering endeavor',
                {'entities': [(44, 64, 'Department_name')]}),
            (
                'SOFTWARE ENGINEERING is a direct sub-field of engineering and has an overlap with computer science and management science',
                {'entities': [(0, 21, 'Department_name')]}),
            (
                'The term SOFTWARE ENGINEERING  appeared in a list of services offered by companies in the June 1965 issue of COMPUTERS.',
                {'entities': [(9, 29, 'Department_name')]}),
            (
                "SOFTWARE ENGINEERING with the Plenary Sessions' keynotes of Frederick Brooks[14] and Margaret Hamilton",
                {'entities': [(0, 20, 'Department_name')]}),
            (
                'Modern, generally accepted best-practices for SOFTWARE ENGINEERING have been collected by the ISO/IEC JTC 1/SC 7 subcommittee and published',
                {'entities': [(46, 66, 'Department_name')]}),
            (
                'INFORMATION TECHNOLOGY system (IT system) is generally an information system, a communications system or, more specifically speaking, a computer system including all hardware, software and peripheral equipment operated by a limited group of users.',
                {'entities': [(0, 22, 'Department_name')]}),
            (
                'the new technology does not yet have a single established name. We shall call it INFORMATION TECHNOLOGY (IT).',
                {'entities': [(80, 103, 'Department_name')]}),
            (
                'but INFORMATION TECHNOLOGY also encompasses other information distribution technologies such as television and telephones',
                {'entities': [(4, 26, 'Department_name')]}),
            (
                'in a business context, the INFORMATION TECHNOLOGY Association of America has defined information technology as the study, design',
                {'entities': [(27, 49, 'Department_name')]}),
            (
                'Some of the ethical issues associated with the use of INFORMATION TECHNOLOGY include many terms',
                {'entities': [(54, 76, 'Department_name')]}),
            (
                'On the later more broad application of the term IT, Keary comments in its original application INFORMATION TECHNOLOGY',
                {'entities': [(48, 50, 'Department_name')]}),
            (
                'INFORMATION TECHNOLOGY (IT) is basically synonymous with the guys and gals you call when you need help with a computer issue and many term kept in mind',
                {'entities': [(0, 23, 'Department_name')]}),
            (
                "The most basic INFORMATION TECHNOLOGY definition is that it's the application of technology to solve business or organizational problems on a broad scale and key is to success",
                {'entities': [(15, 38, 'Department_name')]}),
            (
                'COMPUTER ENGINEERING students are allowed to choose areas of in-depth study in their junior and senior years and the intermession',
                {'entities': [(0, 20, 'Department_name')]}),
            ('Media related to COMPUTER ENGINEERING at Wikimedia Commons and this is the most important',
             {'entities': [(16, 37, 'Department_name')]}),
            (
                'the most important computer embedded COMPUTER ENGINEERING specializations include system-on-chip design, architecture of edge computing and the Internet of things',
                {'entities': [(37, 58, 'Department_name')]}),
            (
                'This specialty of a many times then different COMPUTER ENGINEERING requires adequate knowledge of electronics and electrical systems',
                {'entities': [(46, 66, 'Department_name')]}),
            (
                'There are many specialty areas in the field of COMPUTER ENGINEERING we have many choices and this is many times',
                {'entities': [(47, 67, 'Department_name')]}),
            (
                'this is offered a Principles and Practice of Engineering Examination for COMPUTER ENGINEERING [33] in 2003 and many times we can do that it',
                {'entities': [(73, 93, 'Department_name')]}),
            (
                'bascially,we can COMPUTER ENGINEERING (ECE) and has been divided into many subcategories as we show many times',
                {'entities': [(17, 37, 'Department_name')]}),
            (
                'COMPUTER ENGINEERING  is referred to as computer science and engineering at some universities as well as soon',
                {'entities': [(0, 21, 'Department_name')]}),
            (
                'LLB programs give students a solid understanding of law, as well as the critical, analytical and strategic thinking skills necessary for the field of law',
                {'entities': [(0, 3, 'Department_name')]}),
            (
                'An LLB, or Bachelor of Laws, is the professional law degree awarded after completing undergraduate education',
                {'entities': [(3, 6, 'Department_name')]}),
            (
                'In most countries, holding an LLB with additional accreditation, allows for the practice of law',
                {'entities': [(30, 33, 'Department_name')]}),
            (
                'Some examples of LLB programs are in law sectors such as business law, European law, international law, and criminal law',
                {'entities': [(17, 20, 'Department_name')]}),
            (
                'Some universities also allow students to develop their own specialized LLB programs specific to their professional interests',
                {'entities': [(71, 74, 'Department_name')]}),
            ('LLB programs can usually be completed in 3 or 4 years',
             {'entities': [(0, 3, 'Department_name')]}),
            ("The variety of different LLB programs can be overwhelming - don't let it stop you",
             {'entities': [(25, 28, 'Department_name')]}),
            ('Start your search by looking at the most popular LLB and Bachelor of Law programs listed below',
             {'entities': [(49, 52, 'Department_name')]}),
            ('LLB programs are available at universities around the world',
             {'entities': [(0, 3, 'Department_name')]}),
            ('LLB programs are offered in a number of various fields',
             {'entities': [(0, 3, 'Department_name')]}),
            (
                'There are many popular LLB programs offered by some of the highest ranking universities in the cities listed below',
                {'entities': [(23, 26, 'Department_name')]}),
            ('The University of London offers two schemes for the LLB degree',
             {'entities': [(52, 55, 'Department_name')]}),
            ('LLB is the abbreviation for the Bachelor of Laws', {'entities': [(0, 3, 'Department_name')]}),
            (
                "The degree abbreviates to LLB instead of due to the traditional name of the qualification in Latin, 'Legum Baccalaureus'",
                {'entities': [(26, 29, 'Department_name')]}),
            (
                'Bachelor of Law is a three year undergraduate degree in law. If you want to join legal line then you must go for LLB after bachelors in any stream of study',
                {'entities': [(0, 15, 'Department_name')]}),
            ('the at Wikimedia Commons and this is the most important in Bachelor of Law',
             {'entities': [(59, 75, 'Department_name')]}),
            (
                'Its a five year program and soon we shall write a separate detailed article on scope of Bachelor of Law',
                {'entities': [(88, 104, 'Department_name')]}),
            (
                'is a better choice than any nonprofessional MA or MSc degree after graduation Bachelor of Law it will alleviate your social status in the society',
                {'entities': [(78, 93, 'Department_name')]}),
            (
                'Science after but Bachelor of Law i think that should be their first choice as it will not only help them in their legal practice but also in judiciary papers',
                {'entities': [(18, 33, 'Department_name')]}),
            (
                'this an student is referred to as Bachelor of Law and engineering at some universities as well as soon',
                {'entities': [(34, 49, 'Department_name')]}),
            (
                'The main Bachelor of Law abbreviation stand for Literally Legum Baccalaureus which is a Latin pharse related to law education',
                {'entities': [(9, 24, 'Department_name')]}),
            (
                'In india Bachelor of Law stand for Bachelor of legislative law and many different types of varity',
                {'entities': [(9, 24, 'Department_name')]}),
            ('An example of BACHELOR OF LAW is the title after the name of a solicitor from England',
             {'entities': [(14, 29, 'Department_name')]}),
            (
                'The BACHELOR OF LAW initiates from the Latin abbreviation of Legum Baccalaureus and many different types of session',
                {'entities': [(4, 19, 'Department_name')]}),
            (
                'this is many your search by looking at the most popular BACHELOR OF LAW and Bachelor of Law programs listed below',
                {'entities': [(76, 91, 'Department_name')]}),
            (
                'It is usually outside of the United States. An example of BACHELOR OF LAW is the title after the name of a solicitor from England',
                {'entities': [(58, 74, 'Department_name')]}),
            ("It's in latin language and it's meaning is BACHELOR OF LAW in the end",
             {'entities': [(43, 58, 'Department_name')]}),
            (
                'It is an undergraduate course presented by different universities in India. There are two options to pursue BACHELOR OF LAW course',
                {'entities': [(108, 123, 'Department_name')]}),
            (
                'One BACHELOR OF LAW course runs for 3 years and other is an integrated dual specialization course of 5 years',
                {'entities': [(4, 19, 'Department_name')]}),
            ('The degree is pursued by the individual to become a legal professor and BACHELOR OF LAW',
             {'entities': [(72, 87, 'Department_name')]}),
            (
                'BACHELOR OF LAW Full Form is Bachelor of Laws. It is also implied by the Latin term Legum Baccalaureus',
                {'entities': [(0, 15, 'Department_name')]}),
            (
                'Most of these deal with writing and publishing. A few longer abbreviations use this as well BACHELOR OF LAW',
                {'entities': [(92, 108, 'Department_name')]}),
            (
                'The Department of Earth and Environmental Sciences offers BS (4 years) and MS (2 years) degree programs',
                {'entities': [(27, 50, 'Department_name')]}),
            (
                'employed by national and multinational companies have proven, that it strives for highest of the academic standards at ENVIRONMENTAL SCIENCES',
                {'entities': [(119, 141, 'Department_name')]}),
            (
                'Environmental Sciences and Environmental is maximum Management Representative in industrial sector',
                {'entities': [(0, 22, 'Department_name')]}),
            (
                'this is many ways to define Environmental Sciences courses teach knowledge pertaining to Environmental Impact Assessment',
                {'entities': [(28, 50, 'Department_name')]}),
            (
                'Introduction to Environmental Science is necessary to maitntained different types and going to throughwalk',
                {'entities': [(16, 37, 'Department_name')]}),
            (
                'The course load should be minimum in the final year for the purpose of giving in Environmental Sciences that it',
                {'entities': [(81, 103, 'Department_name')]}),
            (
                'Environmental Sciences is different relief for final years project work and career-oriented activities',
                {'entities': [(0, 22, 'Department_name')]}),
            (
                'To maintain the equivalence of duration of study at international level, the main purpose is ENVIRONMENTAL SCIENCES',
                {'entities': [(93, 115, 'Department_name')]}),
            (
                'To illustrate these points, this course has been developed, which examines the history ENVIRONMENTAL SCIENCES and philosophical',
                {'entities': [(87, 109, 'Department_name')]}),
            (
                'ENVIRONMENTAL SCIENCES Exploration of such topics will help them become better prepared for the inevitable public debates',
                {'entities': [(0, 22, 'Department_name')]}),
            (
                'Historical and logical analysis of various types of scientific hypotheses and the data that support or undermine ENVIRONMENTAL SCIENCES them',
                {'entities': [(113, 135, 'Department_name')]}),
            (
                'Introduction To Climatology and A Brief History, The Earth Four Spheres and ENVIRONMENTAL SCIENCES to provides different condition and man term has been used',
                {'entities': [(76, 98, 'Department_name')]}),
            (
                'many differnt catagories of ENVIRONMENTAL SCIENCES understanding of adaptation and mitigation options in relation to climate change',
                {'entities': [(28, 50, 'Department_name')]}),
            (
                'Hydrocarbons & their byproducts; Future Climates and the Consequences and ENVIRONMENTAL SCIENCES is necessary to used differnt catagories',
                {'entities': [(74, 97, 'Department_name')]}),
            (
                'geophysics is an applied branch of geophysics and economic geology, which uses physical methods',
                {'entities': [(0, 10, 'Department_name')]}),
            (
                'geophysics can be used to directly detect the target style of mineralization, via measuring its physical properties directly',
                {'entities': [(0, 10, 'Department_name')]}),
            (
                'it is also used to map the subsurface structure of a region, to elucidate the underlying structures and geophysics are as follows',
                {'entities': [(104, 114, 'Department_name')]}),
            ('this techniques are the most widely used geophysics technique in hydrocarbon exploration',
             {'entities': [(41, 51, 'Department_name')]}),
            ('Ground magnetometric surveys can be used for detecting buried ferrous metals and geophysics',
             {'entities': [(81, 91, 'Department_name')]}),
            (
                'They are used to map the subsurface distribution of stratigraphy and its structure geophysics into the categories',
                {'entities': [(82, 93, 'Department_name')]}),
            (
                'geophysics Gravity and magnetics are also used, with considerable frequency, in oil and gas exploration',
                {'entities': [(0, 10, 'Department_name')]}),
            (
                'These can be used to determine the geometry and geophysics depth of covered geological structures including uplifts',
                {'entities': [(48, 58, 'Department_name')]}),
            (
                'round the geophysics penetrating radar is a non-invasive technique, and is used within civil construction and engineering for a variety of uses',
                {'entities': [(10, 20, 'Department_name')]}),
            (
                'GEOPHYSICS The Spectral-Analysis-of-Surface-Waves (SASW) method is another non-invasive techniques',
                {'entities': [(0, 10, 'Department_name')]}),
            (
                'The most direct method of detection of ore via magnetism involves detecting iron ore mineralisation via mapping magnetic anomalies at GEOPHYSICS',
                {'entities': [(134, 144, 'Department_name')]}),
            (
                'This is an GEOPHYSICS indirect method for assessing the likelihood of ore deposits or hydrocarbon accumulations',
                {'entities': [(11, 21, 'Department_name')]}),
            (
                'The most direct method of detection of ore via magnetism involves GEOPHYSICS detecting iron ore mineralisation via mapping magnetic.',
                {'entities': [(66, 76, 'Department_name')]}),
            (
                'This can be used to directly detect Mississippi Valley Type ore deposits, iron oxide copper in GEOPHYSICS',
                {'entities': [(95, 105, 'Department_name')]}),
            (
                'This helps in rig monitoring and prescriptive analysis and in many different ways GEOPHYSICS in at different home automatically',
                {'entities': [(82, 92, 'Department_name')]}),
            (
                'GEOPHYSICS Electric-resistance methods such as induced polarization methods can be useful for directly detecting sulfide bodies',
                {'entities': [(0, 10, 'Department_name')]}),
            (
                'Social science is the branch of science devoted to the study of human societies and the relationships among individuals within those societies',
                {'entities': [(0, 15, 'Department_name')]}),
            (
                'Positivist social sciences use methods resembling those of the natural sciences as tools for understanding society',
                {'entities': [(11, 26, 'Department_name')]}),
            ('The history of the social sciences begins in the Age of Enlightenment after 1650',
             {'entities': [(19, 34, 'Department_name')]}),
            (
                'describe the field, taken from the ideas of Charles Fourier; Comte also referred to the field as social sciences',
                {'entities': [(97, 113, 'Department_name')]}),
            (
                'social and environmental factors affecting it, made many of the natural sciences interested in some aspects of social sciences methodology',
                {'entities': [(111, 126, 'Department_name')]}),
            (
                'In the contemporary period, Karl Popper and Talcott Parsons influenced the furtherance of the social sciences',
                {'entities': [(94, 110, 'Department_name')]}),
            (
                'The term "social sciences" may refer either to the specific sciences of society established by thinkers such as Comte',
                {'entities': [(10, 25, 'Department_name')]}),
            (
                'Around the start of the 21st century, the expanding domain of economics in the social sciences has been described as economic imperialism',
                {'entities': [(79, 95, 'Department_name')]}),
            (
                'The social sciences disciplines are branches of knowledge taught and researched at the college or university level',
                {'entities': [(4, 19, 'Department_name')]}),
            (
                'Social science fields of study usually have several sub-disciplines or branches, and the distinguishing lines between these are often both arbitrary and ambiguous',
                {'entities': [(0, 14, 'Department_name')]}),
            (
                'Economics is a social sciences that seeks to analyze and describe the production, distribution, and consumption of wealth',
                {'entities': [(15, 31, 'Department_name')]}),
            (
                'The expanding domain of economics in the social sciences has been developed and used in different department',
                {'entities': [(41, 56, 'Department_name')]}),
            (
                'geography bridges some gaps between the natural sciences and social sciences and its used variety of types',
                {'entities': [(61, 76, 'Department_name')]}),
            ('History has a base in both the social sciences and the humanities',
             {'entities': [(31, 46, 'Department_name')]}),
            (
                'The Social Science History Association, formed in 1976, brings together scholars from numerous disciplines interested in social history',
                {'entities': [(4, 18, 'Department_name')]}),
            (
                'The social science of law, jurisprudence, in common parlance, means a rule that (unlike a rule of ethics) is capable of enforcement through institutions',
                {'entities': [(4, 18, 'Department_name')]}),
            (
                'Legal policy incorporates the practical manifestation of thinking from almost every SOCIAL SCIENCES and the humanities',
                {'entities': [(84, 99, 'Department_name')]}),
            ('can be clearly distinguished as having little to do with the SOCIAL SCIENCES',
             {'entities': [(61, 76, 'Department_name')]}),
            ('whereas a B.A. underlines a majority of SOCIAL SCIENCES credits',
             {'entities': [(40, 55, 'Department_name')]}),
            (
                'whether they choose a balance, a heavy science basis, or heavy SOCIAL SCIENCES basis to their degree',
                {'entities': [(63, 78, 'Department_name')]}),
            ('Additional applied or interdisciplinary fields related to the SOCIAL SCIENCES include',
             {'entities': [(61, 77, 'Department_name')]}),
            ('branch of SOCIAL SCIENCES that addresses issues of concern to developing countries',
             {'entities': [(10, 25, 'Department_name')]}),
            (
                'Computational SOCIAL SCIENCES is an umbrella field encompassing computational approaches within the input',
                {'entities': [(14, 29, 'Department_name')]}),
            (
                'Environmental SOCIAL SCIENCES is the broad, transdisciplinary study of interrelations between humans and the natural environment',
                {'entities': [(14, 29, 'Department_name')]}),
            (
                'Legal management is a SOCIAL SCIENCES discipline that is designed for students interested in the study of state and legal elements',
                {'entities': [(21, 37, 'Department_name')]}),
            (
                'Business administration (also known as business management) is the administration of a business',
                {'entities': [(0, 23, 'Department_name')]}),
            (
                "Bachelor of Commerce (Bcom. or BComm) is a bachelor's degree in commerce and business administration",
                {'entities': [(77, 100, 'Department_name')]}),
            (
                "it is the is a master's degree in business administration with a significant focus on management",
                {'entities': [(34, 57, 'Department_name')]}),
            (
                'he Doctor of Business Administration (abbreviated DBA, D.B.A., DrBA, or Dr.B.A.) is a research doctorate awarded on the basis of advanced study',
                {'entities': [(13, 36, 'Department_name')]}),
            ('Bachelor of Science in Economics program is designed for those students who',
             {'entities': [(23, 32, 'Department_name')]}),
            ('career oriented and market determined educational program in the field of Economics',
             {'entities': [(74, 83, 'Department_name')]}),
            (
                'The program is the blend of different courses like theoretical, quantitative and applied areas in economics',
                {'entities': [(98, 107, 'Department_name')]}),
            (
                'The main objective is to achieve the highest possible standards of education, teaching and research in economics more are different',
                {'entities': [(103, 112, 'Department_name')]}),
            ('Impart sound theoretical and applied knowledge of economics',
             {'entities': [(50, 59, 'Department_name')]}),
            (
                'Provide a thorough understanding of the economics theory pertaining to global in the different society and many types',
                {'entities': [(40, 49, 'Department_name')]}),
            ('global economics issues and its impact on Pakistans economy',
             {'entities': [(7, 16, 'Department_name')]}),
            (
                'Develop professionals with a sound knowledge in the field of economics who can understand and analyze problems faced by developing country like Pakistan',
                {'entities': [(61, 70, 'Department_name')]}),
            ('Prepare students for advanced studies in economics in different types in the sytle',
             {'entities': [(41, 50, 'Department_name')]}),
            (
                'Some programs allow students to select a specialty within the economics field so they can tailor their curricula to their career goals',
                {'entities': [(62, 71, 'Department_name')]}),
            (
                "Many students continue their studies in graduate programs by earning a master's or doctoral degree in economics",
                {'entities': [(102, 111, 'Department_name')]}),
            ('A Bachelor of Science in Economics gives students the necessary knowledge in math',
             {'entities': [(25, 34, 'Department_name')]}),
            (
                'English is a West Germanic language that was first spoken in early medieval England and eventually',
                {'entities': [(0, 7, 'Department_name')]}),
            (
                'The earliest forms of English, a group of West Germanic (Ingvaeonic) dialects brought to Great Britain by Anglo-Saxon settlers in the 5th century',
                {'entities': [(22, 29, 'Department_name')]}),
            (
                'Modern English began in the late 15th century with the introduction of the printing press to London, the printing of the King James Bible and the start of the Great Vowel Shift',
                {'entities': [(7, 14, 'Department_name')]}),
            (
                'English is the largest language by number of speakers,[10] and the third most-spoken native language in the world, after Standard Chinese and Spanish',
                {'entities': [(0, 7, 'Department_name')]}),
            (
                'English is the majority native language in the United States, the United Kingdom, Canada, Australia, New Zealand and the Republic of Ireland',
                {'entities': [(0, 7, 'Department_name')]}),
            (
                'Modern English grammar is the result of a gradual change from a typical Indo-European dependent marking pattern',
                {'entities': [(7, 14, 'Department_name')]}),
            (
                'but in extreme cases can lead to confusion or even mutual unintelligibility between English speakers',
                {'entities': [(84, 91, 'Department_name')]}),
            (
                'Unlike Icelandic and Faroese, which were isolated, the development of English was influenced by a long series of invasions of the British',
                {'entities': [(70, 77, 'Department_name')]}),
            ('Some scholars have argued that English can be considered a mixed language or a creole',
             {'entities': [(31, 38, 'Department_name')]}),
            ('most specialists in language contact do not consider English to be a true mixed language',
             {'entities': [(53, 61, 'Department_name')]}),
            (
                'English is classified as a Germanic language because it shares innovations with other Germanic languages such as Dutch, German, and Swedish.[25]',
                {'entities': [(0, 7, 'Department_name')]}),
            ('Even after the vowel shift the language still sounded different from Modern English',
             {'entities': [(76, 83, 'Department_name')]}),
            (
                'The countries where English is spoken can be grouped into different categories according to how',
                {'entities': [(20, 27, 'Department_name')]}),
            (
                'English does not belong to just one country, and it does not belong solely to descendants and differet types of close',
                {'entities': [(0, 7, 'Department_name')]}),
            (
                "The Bachelor of Business Administration (BBA or B.B.A.) is a bachelor's degree in business administration",
                {'entities': [(4, 39, 'Department_name')]}),
            (
                'Bachelor of Business Administration is a quantitative variant on the BBA. General educational requirements are relatively mathematics intensive',
                {'entities': [(0, 35, 'Department_name')]}),
            (
                'Bachelor of Bussiness Administration The Academy of Business Administration was established in the year of 1993 by Mr. Sudhasindhu Panda',
                {'entities': [(0, 36, 'Department_name')]}),
            (
                'Germanic language that was first spoken in early medieval England and eventually in Bachelor of Bussiness Administration at different types',
                {'entities': [(83, 120, 'Department_name')]}),
            (
                "The bachelor's degree program offers a progressive curriculum Bachelor of Bussiness Administration designed to teach business fundamentals and higher level leadership skills",
                {'entities': [(62, 98, 'Department_name')]}),
            (
                'This specialization in Bachelor of business administration helps you develop the management, interpersonal, and professional skills you need to advance your career',
                {'entities': [(23, 58, 'Department_name')]}),
            (
                'The Bachelor of Science in Bachelor of Business Administration (BSBA) is four-year (8 semesters) program and designed for candidates having 12-years education with commerce & business backgrounds.',
                {'entities': [(27, 62, 'Department_name')]}),
            (
                'This program offers a progressive Bachelor of Business Administration curriculum designed to teach business fundamentals and higher level leadership skills, and equip students to function more effectively in a business-driven economy',
                {'entities': [(34, 69, 'Department_name')]}),
            (
                'This program will Bachelor of Business Administration help students to examine how technology and innovation can help organizations develop a sustainable competitive advantage',
                {'entities': [(18, 53, 'Department_name')]}),
            (
                'It is four-year full time study program spread over eight semesters. Each semester has at least 18 weeks duration for teaching and examinations etc Bachelor of Business Administration',
                {'entities': [(160, 183, 'Department_name')]}),
            (
                'BBA The students study progress evaluation mechanism is based on continuous assessment throughout the semester',
                {'entities': [(0, 4, 'Department_name')]}),
            (
                'The mid and final term exams are conducted at VUs designated exam centers and usually count for 80 to 85% of the total marks for a course BBA.',
                {'entities': [(139, 142, 'Department_name')]}),
            (
                'Students are required to complete a Project/ Internship Report in the final semester of their BBA.',
                {'entities': [(94, 97, 'Department_name')]}),
            (
                'The choice of the final project is at BBA the students discretion. However, consultation with the student advisor is compulsory.',
                {'entities': [(38, 41, 'Department_name')]}),
            (
                'The students who are already in service shall be BBA exempted from Internship but required to submit the Project',
                {'entities': [(49, 53, 'Department_name')]}),
            (
                'BBA Students have to submit a detailed write-up of the Project and may be required to give a presentation',
                {'entities': [(0, 3, 'Department_name')]}),
            (
                'The students of BBA who are already in service shall be exempted from Internship but required to submit the Project',
                {'entities': [(16, 19, 'Department_name')]}),
            (
                'To be eligible for the BBA award BS degree, the students are required to complete prescribed course work of 132 credit hours with a minimum Cumulative Grade Point Average (CGPA) of 2.0 out of 4',
                {'entities': [(23, 26, 'Department_name')]}),
            (
                'The courses BBA may be revised time to time as a result of continuous review to bring them at par with courses',
                {'entities': [(12, 16, 'Department_name')]}),
            ('The University reserves the right to change fee structure from time to time BBA.',
             {'entities': [(76, 79, 'Department_name')]}),
            (
                'A Bachelor of Business Administration (BBA) program can prepare students to manage companies by teaching subjects such as marketing and human resources.',
                {'entities': [(14, 37, 'Department_name')]}),
            (
                'The 4-year degree program provides a fundamental education in business and management principles in BBA.',
                {'entities': [(100, 103, 'Department_name')]}),
            (
                'Programs typically allow students to BBA specialize in one of multiple concentration areas, including international business, finance, real estate',
                {'entities': [(37, 40, 'Department_name')]}),
            (
                'BBA programs can offer practical management training that can prepare students to successfully work within a large or small organization.',
                {'entities': [(0, 3, 'Department_name')]}),
            (
                'Programs may emphasize the development of communications, quantitative reasoning, and business analysis skills. Through BBA courses.',
                {'entities': [(120, 123, 'Department_name')]}),
            (
                'Through the BBA programs, students can pursue business education and learn skills that will help them pursue various management and administrative roles within a company.',
                {'entities': [(12, 15, 'Department_name')]}),
            (
                'BBA is a 4-year degree program which prepares students for a variety of different management and administrative roles within a company.',
                {'entities': [(0, 3, 'Department_name')]}),

            (
            'management science is also concerned with so-called soft-operational analysis, which concerns methods for strategic planning, strategic decision support, and problem structuring methods (PSM).',
            {'entities': [(0, 18, 'Department_name')]}),
            (
                'management science is a peer-reviewed academic journal that covers research on all aspects of management related to strategy, entrepreneurship, innovation, information technology, and organizations as well as all functional areas of business, such as accounting, finance, marketing, and operations.',
                {'entities': [(0, 18, 'Department_name')]}), (
                "It is published by the Institute for Operations Research and the management sciences and was established in 1954 by the Institute's precursor, The Institute of management sciences. C. West Churchman was the founding editor-in-chief.",
                {'entities': [(65, 84, 'Department_name')]}), (
                'The Institute of management sciences (IMS Lahore), formerly known as Pak-American Institute of management sciences (Pak-AIMS), is a project of AKEF established in Lahore, Pakistan in 1987 which offers undergraduate and graduate programs in management and computer sciences.',

                {'entities': [(17, 36, 'Department_name')]}),
            (
            'computer sciences If your database starts performing at slow speeds, its possible that there is a data bottleneck problem',
            {'entities': [(0, 17, 'Department_name')]}),
            (
            'This is most computer sciences commonly caused by high CPU usage and can be a sign that you need to upgrade your server',
            {'entities': [(13, 30, 'Department_name')]}),
            (
            'High CPU usage could also mean computer sciences that the operating system is consuming more than its CPU share and you need to address the software in your database',
            {'entities': [(31, 48, 'Department_name')]}),
            (
            'Alternatively, poor CPU performance could be caused by the CPU having to wait on the input/output subsystem computer sciences',
            {'entities': [(108, 125, 'Department_name')]}),
            (
            'computer sciences CPU usage might be the most common cause of slow performance, but close behind is low memory. When you start to run out of physical memory (RAM) on the server',
            {'entities': [(0, 17, 'Department_name')]}),
            (
            'the database computer sciences will typically start to use the hard drive to store mission-critical processes that are usually held in RAM',
            {'entities': [(13, 30, 'Department_name')]}),
            (
            'Usually, to fix this problem, you would need a RAM upgrade but ther is a chance that this could be the result of a memory leak computer sciences',
            {'entities': [(127, 144, 'Department_name')]}),
            (
            'which will need identifying and patching. A memory leak is the result of a computer sciences bug that means a program does return memory that was allocated to it on a temporary basis',
            {'entities': [(75, 92, 'Department_name')]}),
            (
            'You would need an experienced and meticulous computer sciences DBA to identify a leak, or you can prepare for it by using an operating system that provides memory leak detection',
            {'entities': [(45, 62, 'Department_name')]}),
            (
            'Lastly, you could be experiencing bottleneck issues due to high disk usage. If you asking too much of your disk, you could upgrade for more efficient performance computer sciences',
            {'entities': [(165, 182, 'Department_name')]}),
            ('but a better and longer-term solution is to scale up your computer sciences database',
             {'entities': [(58, 75, 'Department_name')]}),
            (
            'computer sciences Despite us spending this entire blog explaining why scalability is essential, its advisable that you look for alternatives before you decide on a scaling solution',
            {'entities': [(0, 17, 'Department_name')]}),
            (
            'At DSP, our DBAs know how to fine-tune computer sciences  your server to keep it working at maximum efficiency, so it always worth trying to take non-scalable',
            {'entities': [(39, 56, 'Department_name')]}),
            (
            'performance-optimisation steps before settling on scaling up or down. That said, it still very important computer sciences to have a plan in place, understand your options,',
            {'entities': [(107, 124, 'Department_name')]}),
            (
            'And realise what those options might involve.computer sciences You don want to decide you need to scale up when it too late, leaving your database operating insufficiently.',
            {'entities': [(45, 62, 'Department_name')]}),
            (
            'Get in touch via our contact page and let us know if you have any questions â€“ weâ€™ll computer sciences  be glad to help',
            {'entities': [(84, 101, 'Department_name')]}),
            (
            'The evaluation task gives the gold standard annotation data and computer sciences the unlabeleddata, given the entity location and category inthe text',
            {'entities': [(64, 81, 'Department_name')]}),
            (
            'We computer sciences use the char as aunit for sequence to modeling the text, deal with the entity recognition as a sequence labeling problem. Make this problem be a seq2seq model',
            {'entities': [(3, 20, 'Department_name')]}),
            (
            'Following Cloud Firestores NoSQL computer sciences data model, you store data in documents that contain fields mapping to values',
            {'entities': [(34, 51, 'Department_name')]}),
            (
            'These documents are stored in collections, which are containers for your documents that computer sciences you can use to organize your data and build queries',
            {'entities': [(88, 105, 'Department_name')]}),
            (
            'Documents support many different data types, from simple strings and numbers computer sciences to complex, nested objects',
            {'entities': [(77, 94, 'Department_name')]}),
            (
            'You can also create subcollections within documents and build computer sciences hierarchical data structures that scale as your database grows',
            {'entities': [(62, 79, 'Department_name')]}),
            (
            'The Cloud Firestore data model supports whatever data structure works best for your app computer sciences .',
            {'entities': [(88, 105, 'Department_name')]}),
            (
                "Pak-AIMS was issued 'No Objections Certificate (NOC)' by the University Grants Commission, now known as the Higher Education Commission (Pakistan) for the award of charter in 1995. Consequently, the institute was chartered as Institute of management sciences (IMS) by the Government of Punjab (Pakistan) under the Punjab Ordinance XXIII of 2002 and given degree-awarding status.",
                {'entities': [(239, 258, 'Department_name')]}), (
                "The Pak-American Institute of management sciences (Pak-AIMS) to reflect the Institute's Articulation Agreement with the College of Staten Island of City University of New York (CSI/CUNY), USA.",
                {'entities': [(30, 49, 'Department_name')]}), (
                'The Institute for Operations Research and the management sciences (INFORMS) is an international society for practitioners in the fields of operations research (O.R.).',
                {'entities': [(46, 65, 'Department_name')]}), (
                'The Institute of management sciences (TIMS). The 2019 president of the institute is Dean Ramayya Krishnan of Carnegie Mellon University.',
                {'entities': [(17, 36, 'Department_name')]}), (
                "According to INFORMS' constitution, the Institute's purpose is to improve operational processes, decision-making, and management by individuals and organizations through operations research, the management sciences, analytics and related scientific methods.",
                {'entities': [(195, 214, 'Department_name')]}), (
                'The constitution provides that the mission of INFORMS is to lead in the development, dissemination and implementation of knowledge, basic and applied research and technologies in operations research, the management sciences, analytics and related methods of improving operational processes, decision-making, and management.',
                {'entities': [(204, 223, 'Department_name')]}), (
                'INFORMS members are operations researchers and analytics professionals who work for universities, corporations, consulting groups, military, the government, and health care. Many are academics who teach operations research, management science, analytics, and the quantitative sciences in engineering and business schools.',
                {'entities': [(224, 242, 'Department_name')]}), (
                'The Army Public College of management and sciences, commonly known as APCOMS, is a private college located in Rawalpindi, Punjab, Pakistan.',
                {'entities': [(27, 50, 'Department_name')]}), (
                'It is often considered to be a sub-field of applied mathematics.[2] The terms management science and decision science are sometimes used as synonyms.',
                {'entities': [(78, 96, 'Department_name')]}), (
                'In 1967 Stafford Beer characterized the field of management science as the business use of operations research ',
                {'entities': [(49, 67, 'Department_name')]}), (
                ' Like operational research itself, management science (MS) is an interdisciplinary branch of applied mathematics devoted to optimal decision planning, with strong links with economics, business, engineering, and other sciences.',
                {'entities': [(35, 53, 'Department_name')]}), (
                "The management scientist's mandate is to use rational, systematic, science-based techniques to inform and improve decisions of all kinds. Of course, the techniques of management science are not restricted to business applications but may be applied to military, medical, public administration, charitable groups, political groups or community groups.",
                {'entities': [(167, 185, 'Department_name')]}), (
                'management science is concerned with developing and applying models and concepts that may prove useful in helping to illuminate management issues and solve managerial problems, as well as designing and developing new and better models of organizational excellence.',
                {'entities': [(0, 18, 'Department_name')]}), (
                'The application of these models within the corporate sector became known as management science.',
                {'entities': [(76, 94, 'Department_name')]}), (
                'The Institute for Operations Research and the management sciences (INFORMS) publishes thirteen scholarly journals about operations research, including the top two journals in their class, according to 2005 Journal Citation Reports.',
                {'entities': [(46, 65, 'Department_name')]}), (
                'management science, or MS, is the discipline of using mathematics, and other analytical methods, to help make better business decisions.',
                {'entities': [(0, 18, 'Department_name')]}), (
                'Some of the fields that are englobed within management science include: decision analysis, optimization, simulation, forecasting, game theory, network/transportation models, mathematical modeling, data mining, probability and statistics, Morphological analysis, resources allocation, project management as well as many others.',
                {'entities': [(44, 62, 'Department_name')]}), (
                "The management scientist's mandate is to use rational, systematic, science-based techniques to inform and improve decisions of all kinds. Of course, the techniques of management science are not restricted to business applications but may be applied to military, medical, public administration, charitable groups, political groups or community groups.",
                {'entities': [(167, 185, 'Department_name')]}), (
                'Institute of management sciences (management education with public spirit and market dynamism)',
                {'entities': [(13, 32, 'Department_name')]}), (
                'This is normally a two years program comprising of 4 semesters. There will be a Fall and a Spring semester in each year. The maximum duration to complete MS in management sciences is 4 years.',
                {'entities': [(160, 179, 'Department_name')]}), (
                'In the pursuit of delivering quality education at your door step, the Department of management sciences has established a diversified academic portfolio both at graduate and undergraduate levels.',
                {'entities': [(84, 103, 'Department_name')]}), (
                'The Department of management sciences aims to offer educationally sound and directly relevant programs to those areas of industry, commerce, the professions and public service.',
                {'entities': [(18, 37, 'Department_name')]}), (
                'The overall objective of the management sciences department is to develop managers and business leaders with the vision, knowledge, creativity, skills, ethics and entrepreneurial ability necessary to integrated, critical aware, dynamic and strategic view of organizations and to play an effective role within them.',
                {'entities': [(29, 48, 'Department_name')]}), (
                'We aim to deliver quality education at your door step by offering wide array of educational programs in the field of management sciences among a diverse community of learners and develop future business leaders of the world.',
                {'entities': [(117, 136, 'Department_name')]}), (
                'The Department of management sciences offers a large number of diversified educational programs thereby producing a maximum number of graduating students at the moment.',
                {'entities': [(18, 37, 'Department_name')]}), (
                'The Department of management sciences (DMS) was established in 1994 to fulfill the demands for quality business professionals by organizations. Since then, the Department has won accolades of success in the business world by producing scintillating results year after year.',
                {'entities': [(18, 37, 'Department_name')]}),
            (
            'The MS in management program is designed to develop the intellectual ability of researchers through understanding the academic body of knowledge in the field of management sciences with specializations in Human Resource Management.',
            {'entities': [(161, 180, 'Department_name')]}),
            (
            'The electives can be taken from graduate level courses in the Faculty of management sciences with the recommendation of the supervisor.',
            {'entities': [(73, 92, 'Department_name')]}),
            (
            'The department of media and Communication Studies (DMCS) has been envisioned as a centre of excellence for promoting media and communication studies in the country.',
            {'entities': [(18, 23, 'Department_name')]}),
            ('The other things of media and  has been complete.', {'entities': [(20, 25, 'Department_name')]}),
            (' We aim to accomplish this in a manner that can be useful for the media professionals',
             {'entities': [(66, 71, 'Department_name')]}),
            (
            'The students are provided opportunities to publish their own monthly newsletter, join field visits to media organizations, and have access to a series of lectures of national',
            {'entities': [(102, 107, 'Department_name')]}),
            ('analysis of media content, performance and audiences, add to basic and applied knowledge in the field',
             {'entities': [(12, 17, 'Department_name')]}),
            (
            'There are also courses aimed at  professionals and graduates seeking to build management carrier within the growing media and content industriesr',
            {'entities': [(116, 121, 'Department_name')]}),
            (
            'Upon completion of their studies the students will receive a BS or M. Sc. in media and Communication Sciences with one of the following specialization',
            {'entities': [(77, 82, 'Department_name')]}),
            ('Mass  saturate our lives, making media literacy an indispensable civicskill for the 21st century',
             {'entities': [(33, 38, 'Department_name')]}),
            ('industries and infrastructures, media activism, and political communication',
             {'entities': [(32, 37, 'Department_name')]}),
            ('media is most important in our life.', {'entities': [(0, 5, 'Department_name')]}),
            ('admin department is backbone of an organization', {'entities': [(0, 5, 'Department_name')]}),
            (
            'He or she is the link between an organizations various departments and ensures the smooth flow of information admin from one part to the other',
            {'entities': [(111, 116, 'Department_name')]}),
            (
            'Many admin positions require the candidate to have an advanced skill set in the software applications Microsoft Word, Excel and Access',
            {'entities': [(5, 10, 'Department_name')]}),
            (
            'An office admin has the responsibility of ensuring that the administrative activities within an organization run efficiently, by providing structure to other employees throughout the organization',
            {'entities': [(10, 15, 'Department_name')]}),
            (
            'The importance of an office administrator to an organization is substantial due to the duties that they are entrusted with, therefore specialized training is required in admin',
            {'entities': [(28, 33, 'Department_name')]}),
            (
            'There are some an extensive range of roles that admin can be associated with an office administrator, these being; organizations advertise',
            {'entities': [(48, 53, 'Department_name')]}),
            (
            'admin The task of inputting, filing and managing the data that is stored within the organizations office system',
            {'entities': [(0, 5, 'Department_name')]}),
            (
            'The role of an office manager admin is more demanding than other administrative positions, including such skills and qualifications as strong administrative',
            {'entities': [(30, 35, 'Department_name')]}),
            (
            'Personal assistants act as a first hand to the office manager so they must ensure that admin all contacts from third party individuals are processed through them',
            {'entities': [(87, 92, 'Department_name')]}),
            (
            'assistance. Becoming a personal assistant requires the employee to have experience in previous administrative jobs admin',
            {'entities': [(95, 100, 'Department_name')]}),
            (
            'The ability of adapting to changing environments and new technologies admin that could be implemented e.g. New software installation',
            {'entities': [(70, 75, 'Department_name')]}),
            (
            'A Business & management studies degree is concerned with the way a company or organisation operates and functions',
            {'entities': [(13, 31, 'Department_name')]}),
            (
            'bascially in the Business management studies is that branch of education which provides knowledge and training pertaining to planning and giving better',
            {'entities': [(26, 44, 'Department_name')]}),
            (
            'in our universities this field such as management studies in our field in simportant to improve this alot in life',
            {'entities': [(39, 57, 'Department_name')]}),
            (
            'Career-scope after completing a business management studies course is huge with a variety of managerial jobs on offer at junior as well as senior level',
            {'entities': [(41, 59, 'Department_name')]}),
            (
            'Candidates in final year of graduation are also eligible to apply for entrance tests conducted for management studies admission',
            {'entities': [(99, 117, 'Department_name')]}),
            (
            'A managers job is to lead and oversee a team performance to increase company revenue management studies business organization hires Managers for each department',
            {'entities': [(88, 106, 'Department_name')]}),
            (
            'management studies job of a financial analyst is to explore and assess investment opportunities on behalf of an individual or a business enterprise',
            {'entities': [(0, 18, 'Department_name')]}),
            (
            'The job of a business analyst includes analyzing the current status of a business, forecasting, outlining problems, finding out solutions, and budget planning for new management studies',
            {'entities': [(167, 185, 'Department_name')]}),
            (
            'You should look for a University which caters to your type of learning and offers good quality management studies educations at a nominal fee. My cousin sister did',
            {'entities': [(95, 113, 'Department_name')]}),
            (
            'Yes definitely it is a good choice management studies for you to make your future and career brighter in at differn and administration field',
            {'entities': [(35, 53, 'Department_name')]}),
            (
            'management studies Most of the top private universities tend to be really expensive as MBA is a programme with high rate of return',
            {'entities': [(0, 18, 'Department_name')]}),
            (
            'Not really, since the likes of FMS New Delhi and JBIMS Mumbai management studies are also great options for pursuing an MBA',
            {'entities': [(62, 80, 'Department_name')]}),
            (
            'I would say that you should go for the pinnacle MBA programme. It is a very holistic management programme consisting of liberal arts management studies necessary',
            {'entities': [(133, 151, 'Department_name')]}),
            (
            "I suggest that you management studies should go for an regular MBA from India's any of top privateUniversity or the Iims",
            {'entities': [(19, 37, 'Department_name')]}),
            (
            'transmitting advanced knowledge and forging indigenous human resource into local and national media markets as well as in other professional organizations.',
            {'entities': [(94, 99, 'Department_name')]}),
            (
            'electronic media and public relation specialization. Soon the department will start the masterâ€™s program in mobile journalism',
            {'entities': [(11, 17, 'Department_name')]}),
            ('The Department is currently offering BS and Master program with the facilities of print media',
             {'entities': [(90, 95, 'Department_name')]}),
            (
            'media The Department has very experienced and qualified faculty. There are two PhD and six MPhil permanent faculty members',
            {'entities': [(0, 6, 'Department_name')]}),
            (
            'linkages with mainstream media and associated organizations including development sector and research organizations',
            {'entities': [(25, 31, 'Department_name')]}),
            (
            'Practically, it is the only institution offering courses in media & Communication Studies to the people of rural and Urban Sindh. The Department has a well stocked seminar library',
            {'entities': [(60, 66, 'Department_name')]}),
            (
            'Under these programs students are treated as journalists who would one day be called upon to accept responsibilities in administrative or supervisory positions in media organization',
            {'entities': [(163, 168, 'Department_name')]}),
            (
            'The students media are required to write report news stories, columns, articles and features in weekly newspaper at different and monthly magazine at different reflecting scholarly and independent thought',
            {'entities': [(13, 19, 'Department_name')]}),
            (
            'and embrace technology to serve the public good media and where people from all backgrounds think critically about the media',
            {'entities': [(48, 54, 'Department_name')]}),
            (
            'Department of media Science realizes its mission statement by clearly defining its goals and objectives which arein accordance with its mission statement',
            {'entities': [(14, 20, 'Department_name')]}),
            ('Many admin positions require the candidate to have an advanced skill set in the software applications.',
             {'entities': [(5, 10, 'Department_name')]}),
            (
            'that the admin activities within an organization run efficiently, by providing structure to other employees throughout the organization',
            {'entities': [(9, 14, 'Department_name')]}),
            (
            'There are some an extensive range of roles that can be associated with an office admin these being; organizations',
            {'entities': [(81, 86, 'Department_name')]}),
            (
            'Like any other rolethat is related to an office admin the job title of personal assistant requires the employee to be organize',
            {'entities': [(49, 54, 'Department_name')]}),
            ('The role of an office manager is more demanding than other admin positions, including such skills',
             {'entities': [(59, 64, 'Department_name')]}),
            ('The admin Department provides and technical support in the areas of human resources (HR), budgetar',
             {'entities': [(4, 9, 'Department_name')]}),
            (
            'admin and human resources assistants support the work of office departments and, in some cases, specific managers or executives',
            {'entities': [(0, 5, 'Department_name')]}),
            ('undergraduate program for management studies offered by many universities throughout the world',
             {'entities': [(26, 44, 'Department_name')]}),
            (
            'obtain the knowledge and skills needed to assume management studies positions in a wide range of organizations.',
            {'entities': [(49, 67, 'Department_name')]}),
            ('management studies programmes provide students with a solid foundation in organizational behavior',
             {'entities': [(0, 18, 'Department_name')]}),
            (
            'Most of the universities offer a 11 months work placement option or studying abroad opportunity for a four-year degree on management studies.',
            {'entities': [(122, 140, 'Department_name')]}),
            (
            'The Bachelor of management studies Degree will be relevant in a vast number of professions; particularly within all business related',
            {'entities': [(16, 34, 'Department_name')]}),
            ('This course will provide the perfect gateway for a career in management studies',
             {'entities': [(61, 79, 'Department_name')]}),
            ('Teaching is typically a combination of lectures, seminars and classes management sciences',
             {'entities': [(70, 88, 'Department_name')]}),
            (
            'Youâ€™ll then be able to choose from a series of more specialized management studies topics, in order to focus on',
            {'entities': [(64, 82, 'Department_name')]}),
            ('therefore management sciences is vey mportant in our life if we',
             {'entities': [(10, 28, 'Department_name')]}),
            (
            'You start with core courses management studies in your first year covering topics such as introduction to accounting, introduction to computing, introduction to management,',
            {'entities': [(31, 49, 'Department_name')]})]

        for data in TRAIN_DATA:
            to_train_ents.append(data)

        # print(to_train_ents)

        random.shuffle(to_train_ents)

        print(to_train_ents)
        import srsly
        from spacy.gold import docs_to_json, biluo_tags_from_offsets, spans_from_biluo_tags
        docs = []
        text_list = []
        txt_list = []
        counter = 1274
        for text, annot in to_train_ents:
            word = text.split()
            doc = nlp(text)
            tags = biluo_tags_from_offsets(doc, annot['entities'])
            entities = spans_from_biluo_tags(doc, tags)
            doc.ents = entities
            iob_tags = [f"Sentence:{counter}|{t}|{t.pos_}|{t.ent_iob_}-{t.ent_type_} " if t.ent_iob_ else "O" for t in
                        doc]
            docs.append(iob_tags)
            counter = counter + 1
            print(docs)
        with open("iob_format.txt", "w") as wr:
            for i in docs:
                wr.writelines(i)
        wr.close()
        list_text = []
        with open("iob_format.txt", "r") as rd:
            ls = rd.readlines()
            for lns in ls:
                words = lns.split(" ")
                list_text.append(words)
                # wordss = list(words)
                # print(wordss + "\n")
        rd.close()

        with open("iob_format.txt", "w") as wr:
            for i in list_text:
                for j in i:
                    wr.writelines(j + "\n")
        wr.close()

    def offseter(label, doc, matchitem):
        start_char = len(str(doc[0:matchitem[1]])) + 1
        subdoc = doc[matchitem[1]:matchitem[2]]
        end_char = start_char + len(str(subdoc))
        return [(start_char, end_char, label)]













