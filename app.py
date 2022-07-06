from flask import Flask, redirect, url_for, request ,render_template
from nltk.corpus import stopwords
import PyPDF2,os
from nltk.tokenize import word_tokenize, sent_tokenize

app = Flask(__name__)

@app.route('/',methods = ["GET","POST"])
@app.route('/home', methods = ["GET","POST"])
def load_page():
    textvalue=''
    summary=''
    if request.method == 'POST':
        textvalue = request.form['inputText']
        file = request.files['file']
        if "file" not in request.files and textvalue == "":
            return redirect(request.url)
        elif file.filename != "" and textvalue == "":
            filePath = 'static/' + file.filename
            file.save(filePath)
            textvalue = extract_text(filePath) 
            summary = text_summarizer(textvalue)
        else:
            summary = text_summarizer(textvalue)
        
    return render_template('index.html', summary = summary)
        
def extract_text(file):
	pdfFileObj = open(file, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	print(pdfReader.numPages)
	pageObj = pdfReader.getPage(0)
	text = pageObj.extractText()
	pdfFileObj.close()
	return text
	
 
def text_summarizer(input):
	stopWords = set(stopwords.words("english"))
	words = word_tokenize(input)
 
	freq = dict()
	for w in words:
		w = w.lower()
		if w in stopWords:
			continue
		if w in freq:
			freq[w] += 1
		else:
			freq[w] = 1
   
	sentences = sent_tokenize(input)
	freqSen = dict()
	for sen in sentences:
		for w, s in freq.items():
			if w in sen.lower():
				if sen in freqSen:
					freqSen[sen] += s
				else:
					freqSen[sen] = s
     
	count = 0
	for sen in freqSen:
		count += freqSen[sen]
	if len(freqSen) != 0:
		average = int(count / len(freqSen))
 
	output = ''
	for sen in sentences:
		if (sen in freqSen) and (freqSen[sen] > (1.2 * average)):
			output +=  " " + sen
   
	return output

if __name__ == '__main__':
    app.run(debug=True)