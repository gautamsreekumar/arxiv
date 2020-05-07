def load_template():
	f = open('template.html')
	template = '\n'.join(f.readlines())
	return template

def add_title_cell(html_content, paper_title):
	html_content += '<td style="word-wrap: break-word; text-align: justify; border: 1px solid black">\n<b>'
	html_content +=  paper_title
	html_content += '</b>\n</td>\n'

	return html_content

def add_abstract_cell(html_content, paper_abstract):
	html_content += '<td style="word-wrap: break-word; text-align: justify; border: 1px solid black">\n'
	html_content +=  paper_abstract
	html_content += '\n</td>\n'

	return html_content

def add_author_cell(html_content, paper_authors):
	html_content += '<td style="word-wrap: break-word; text-align: justify; border: 1px solid black">\n'
	html_content +=  paper_authors
	html_content += '\n</td>\n'

	return html_content

def add_link_cell(html_content, paper_id):
	html_content += '<td style="text-align: center; border: 1px solid black">\n'
	html_content +=  '<a href="https://arxiv.org/abs/{0}">Abs</a><br><a href="https://arxiv.org/pdf/{0}.pdf">PDF</a>'.format(paper_id)
	html_content += '\n</td>\n'

	return html_content