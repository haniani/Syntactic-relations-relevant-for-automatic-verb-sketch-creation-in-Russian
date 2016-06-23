# -*- coding: utf-8 -*-
#!/usr/bin/python
import json, io, re, sys, math, csv, operator
from operator import itemgetter
from math import log
from math import sqrt
import collections

with open("freqdict.json", "r") as jsonn:
  json_string = jsonn.read()
parsed_string = json.loads(json_string)

def getSketch(word):
    wordlistSortRel = []
    for c in parsed_string["DICTIONARY"]:
      if "FIELD1" not in c:
        continue
      firstword = c["FIELD1"]
      PoS = c["FIELD2"]
      ipm1 = c["FIELD3"]
      R = c["FIELD4"]
      D = c["FIELD5"]
      doc1 = c["FIELD6"]
      if firstword == word:
        #print("Word:", firstword, "PoS:", PoS, "Ipm:", ipm1, "R:", R, "D:", D, "Doc:", doc1)
        continue
    while word:
        line = f.readline()
        lineSplit = line.split('\t')
        if lineSplit[0] != word:
            continue

        json_data = lineSplit[1] #второй эл-т строки, т.е. словарь из отн-й и тд
        sketch = json.loads(json_data)
        w.write(lineSplit[0]+'\n')
        reg = re.compile('\w+_[Acc|Gen|Ins|Loc|Dat]( of)?')
        wordlistSortRel = []
        for rel in sketch:
            m = re.search(reg, rel)
            if rel in goodRel or m!=None:
                for kluch,znachenie in combineRel.items():
                    if type(znachenie) != list:
                        if re.search(znachenie, rel):
                            w.write('\n'+'Связь: '+kluch+'\n'+'Подсвязь: '+rel+'\n')
                    if rel in znachenie:
                        w.write('\n'+'Связь: '+kluch+'\n'+'Подсвязь: '+rel+'\n')

                freqrelglag = sketch[rel][0]
                print("Отношение + глагол:", rel, freqrelglag)

                rels = re.compile(rel)
                relsCount = rels.findall(str(slovnikline))
                relsCount2 = len(relsCount)
                relsCount3 = 209198275 - freqrelglag
                logar0 = (math.log2(float(freqrelglag)**3*float(209198275)/float(relsCount2)*float(relsCount3)))
                relsglagpmi.write(str(rel) + "\t" + str(logar0) + "\n")
                print("Всего отношения по корпусу:", relsCount2)
                print("Глагол + другие отношения:",relsCount3)
                print("PMI:",logar0)
                print("###")

                dic = sketch[rel][1]
                #print(dic) #слова в отношении-второй эл-т м-ва значения словаря sketch, что есть словарь слов с этим отношением
                wordlist = []
                for word in dic: #для слова в таком отношении -для ключа в словаре-
                    info = word, dic[word][0]
                    #print(info) #слово в отнош. и логдайс
                    wordlist.append(info)
                wordlistSorted = sorted(wordlist, key=lambda tup: tup[1], reverse=True)
                for l in wordlistSorted:
                    s = '| ' + l[0] +', '+str(l[1])+' |\n'
                    w.write(s)
                for c in parsed_string["DICTIONARY"]:
                  if "FIELD1" not in c:
                    continue
                  SecondWord = c["FIELD1"]
                  PoS2 = c["FIELD2"]
                  ipm22 = c["FIELD3"]
                  R2 = c["FIELD4"]
                  D2 = c["FIELD5"]
                  Doc2 = c["FIELD6"]
                  targetvalue7 = ()
                  if SecondWord == l[0]:
                    continue
                  for j in wordlistSorted:
                    targetvalue7 = j[0]
                    relfreq = j[1]
                    znachdic = targetvalue7
                    if znachdic == c["FIELD1"]:
                      ipm2 = c["FIELD3"]
                      if znachdic in stopwords:
                        break

                      logar = (math.log2(float(relfreq)*float(209198275)/float(ipm1)*float(ipm2))) #PMI1
                      logar2 = (math.log2(float(relfreq)**3*float(209198275)/float(ipm1)*float(ipm2))) #PMI2
                      sqrt_relfreq = sqrt(float(relfreq))
                      tscore = ((float(relfreq) + (((float(ipm1))*(float(ipm2))) / (float(209198275))))) / (sqrt_relfreq)
                      resglag.write(str(logar) + "\t" + str(tscore) + "\t" + str(rel) + "\t" + str(znachdic) + "\n")
                      resglag2.write(str(logar2) + "\t" + str(tscore) + "\t" + str(rel) + "\t" + str(znachdic) + "\n")


        break


goodRel = ['суб_копред of', 'об_копред of', 'присвяз of', 'сочин','и','или',
           'но','либо','а','обст','сравн', 
           'чем','1-компл', '2-компл', '3-компл','как', 'словно', 'будто', 'точно','сочин of','и of',
           'или of','но of','либо of','а of','сравн of', 'чем of','1-компл of','2-компл of',
           '3-компл of','как of','словно of','будто of','точно of','обст of',
           'предик','предик of', 'дат_субъект', 'дат_субъект_of', 'разъяснит', 'разъяснит_of', 'длительн', 'длительн_of',
           'изъяснит', 'изъяснит_of', 'неакт_компл', 'неакт_компл_of', 'сент_предик', 'сент_предик_of', 'агент', 'агент_of',
           'соотнос', 'соотнос_of', 'аналит', 'аналит_of', 'пасс_анал', 'пасс_анал_of', 'кратно_длительн', 'кратно_длительн_of',
           'присвяз', 'соч_союзн', 'соч_союзн_of', 'релят', 'релят_of', 'подч-союзн', 'подч-союзн_of', 'об-копр', 'об-копр_of',
           'оп_опред', 'оп-опред_of', 'колич_копред', 'колич_копред_of', 'суб_обст', 'суб_обст_of', 'колич_вспом', 'колич_вспом_of',
           "\w+_[Nom|Acc|Dat|Gen|Ins|Loc]","\w+_[Nom|Acc|Dat|Gen|Ins|Loc of]"
        ]

combineRel = {
  'глагол_adj' : ['суб_копред of', 'об_копред of', 'присвяз of'],
  'сочин' : ['сочин','и','или','но','либо','а'],
  'modifier' : ['огран','обст'],
  'сравн' : ['сравн', 'чем'],
  'компл' : ['1-компл', '2-компл', '3-компл'],
  'сравн_союзн' : ['как', 'словно', 'будто', 'точно'],
  'предл-падежн' : "\w+_[Nom|Acc|Dat|Gen|Ins|Loc]",
  'сочин_of' : ['сочин of','и of','или of','но of','либо of','а of'],
  'сравн_of' : ['сравн of', 'чем of'],
  'компл_of' : ['1-компл of','2-компл of','3-компл of'],
  'сравн_союзн_of' : ['как of','словно of','будто of','точно of'],
  'предл-падежн_of' : "\w+_[Nom|Acc|Dat|Gen|Ins|Loc] of",
  'modifier_of' : ['огран of','обст of'] 
}

stopwords = ["я", "ты", "мы", "он", "она", "оно", "они", "это", "этот", "эта", "эти", "то", "та", "тот", "те", "что", "так", "вот", "быть", "как", "в", "к", "на", "вы", "который"]

f =  open("test.py", "r", encoding='utf-8') 
word = input("Введите слово: ")
w = open(word+"_sketch.txt", 'w', encoding='utf-8')
resglag = open(word+": pmi+tscore+rel.csv", "w", encoding='utf-8')
resglag2 = open(word+": pmi2+tscore+rel.csv", "w", encoding='utf-8')
relsglagpmi = open(word+": pmirels.csv", "w", encoding='utf-8')
slovnikBigra = open("trigrams_sample.py", "r", encoding='utf-8')
slovnikline = slovnikBigra.readlines()


##
getSketch(word)

f.close()
w.close()
resglag.close()
resglag2.close()
relsglagpmi.close()


reader = csv.reader(open(word+": pmi+tscore+rel.csv"), delimiter = "\t")
sortedlist = sorted(reader, key=lambda x: float(x[0]), reverse=True)
resglag1 = open(word+": pmi+tscore+rel.csv", "w", encoding='utf-8')
resglag2 = csv.writer(resglag1)
header = (["PMI"] + ["T-score"] + ["Отношение"] + ["Слово"])
relevantrel = []
S = set()
resglag2.writerow(header)
for item in sortedlist:
  resglag2.writerow([item[0]] + [item[1]] + [item[2]] + [item[3]])
  if item[2] in S:
    continue
  S.add(item[2])
  relevantrel.append(item[2])
relrel = str(relevantrel)
resglag2.writerow(["Релевантные отношения:"] + [relrel])

reader2 = csv.reader(open(word+": pmi2+tscore+rel.csv"), delimiter = "\t")
sortedlist2 = sorted(reader2, key=lambda x: float(x[0]), reverse=True)
resglag11 = open(word+": pmi2+tscore+rel.csv", "w", encoding='utf-8')
resglag22 = csv.writer(resglag11)
header2 = (["PMI2"] + ["T-score"] + ["Отношение"] + ["Слово"])
relevantrel2 = []
S2 = set()
resglag22.writerow(header2)
for item in sortedlist2:
  resglag22.writerow([item[0]] + [item[1]] + [item[2]] + [item[3]])
  if item[2] in S2:
    continue
  S2.add(item[2])
  relevantrel2.append(item[2])

relrel2 = str(relevantrel2)
resglag22.writerow(["Релевантные отношения:"] +[relrel2])

reader3 = csv.reader(open(word+": pmirels.csv"), delimiter = "\t")
sortedlist3 = sorted(reader3, key=lambda x: float(x[1]), reverse=True)
resglag111 = open(word+": pmirels.csv", "w", encoding='utf-8')
resglag222 = csv.writer(resglag111)
header3 = (["Отношение"] + ["PMI"])
relevantrel3 = []
S3 = set()
resglag222.writerow(header3)
for item in sortedlist3:
  resglag222.writerow([item[0]] + [item[1]])
  if item[0] in S3:
    continue
  S3.add(item[0])
  relevantrel3.append(item[0])

relrel3 = str(relevantrel3)
resglag222.writerow(["Релевантные отношения:"] +[relrel3])

sys.exit()
