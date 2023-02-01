def getAcceptedEmail(firstName, lastName):
    try:
        appliedEmail = open('./src/data/emailTemplates/accepted.html', 'r')
        contents = appliedEmail.read()
        appliedEmail.close()
        contents = contents.replace("first_name", firstName).replace("last_name", lastName)
        return contents
    except:
        return f'<div>' \
               f'   <div>' \
               f'       <h3>Hello {firstName} {lastName}</h3>' \
               f'       <p>' \
               f'           Your application has been <b>Accepted!</b>' \
               f'       </p>' \
               f'   </div>' \
               f'</div>'


def getAcceptedSubjectLine() -> str:
    return "WiCHacks Application Accepted"
