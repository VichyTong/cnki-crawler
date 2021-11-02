import pdfplumber
import re
import json

class Analyze_pdf :
    def work(self, path):
        List = []
        with pdfplumber.open(path) as pdf:
            SubjectCnt = -1
            SubsubjectCnt = 0
            for it in pdf.pages:
                form = it.extract_tables()
                for i in form[0]:
                    if i[1] == None:
                        List.append([i[0]])
                        SubjectCnt += 1
                        SubsubjectCnt = 0
                    elif re.match("\d", i[0]) != None:
                        List[SubjectCnt][SubsubjectCnt].append(i[1].replace('\n', ''))
                    elif re.match("[A-Z]+", i[1]) != None:
                        List[SubjectCnt].append([i[0].replace('\n', '')])
                        SubsubjectCnt += 1
                break
        return List
