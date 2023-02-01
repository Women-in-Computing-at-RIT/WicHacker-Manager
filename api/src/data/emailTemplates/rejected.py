def getRejectedEmail(firstName, lastName):
    try:
        appliedEmail = open('./src/data/emailTemplates/rejected.html', 'r')
        contents = appliedEmail.read()
        appliedEmail.close()
        contents = contents.replace("first_name", firstName).replace("last_name", lastName)
        return contents
    except:
        return f'<div>' \
               f'   <div>' \
               f'       <h3>Hello {firstName} {lastName}</h3>' \
               f'       <p>' \
               f'           We\'re sorry to inform you that your application has been rejected' \
               f'       </p>' \
               f'   </div>' \
               f'</div>'


def getRejectedSubjectLine() -> str:
    return "WiCHacks Application Rejected"
