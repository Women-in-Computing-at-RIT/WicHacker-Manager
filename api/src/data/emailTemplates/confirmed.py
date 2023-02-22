def getConfirmedEmail(firstName, lastName):
    try:
        appliedEmail = open('./src/data/emailTemplates/confirmed.html', 'r')
        contents = appliedEmail.read()
        appliedEmail.close()
        contents = contents.replace("first_name", firstName).replace("last_name", lastName)
        return contents
    except:
        return f'<div>' \
               f'   <div>' \
               f'       <h3>Hello {firstName} {lastName}</h3>' \
               f'       <p>' \
               f'           Thank you, your attendance has been confirmed.' \
               f'       </p>' \
               f'   </div>' \
               f'</div>'


def getConfirmedSubjectLine() -> str:
    return "WiCHacks Confirmation"


def getRequestConfirmedEmail():
    try:
        appliedEmail = open('./src/data/emailTemplates/requestConfirmed.html', 'r')
        contents = appliedEmail.read()
        appliedEmail.close()
        return contents
    except:
        return f'<div>' \
               f'   <div>' \
               f'       <h3>Hello!</h3>' \
               f'       <p>' \
               f'           As WiCHacks approaches, we ask you to confirm your attendance of WiCHacks. ' \
               f'           This helps the organizers finalize our planning to provide the best event possible.' \
               f'' \
               f'           Please login to your application homepage at apply.wichacks.io confirm your attendance' \
               f'' \
               f'           Thank you,' \
               f'           WiCHacks Organizers' \
               f'       </p>' \
               f'   </div>' \
               f'</div>'


def getRequestConfirmedSubjectLine() -> str:
    return "WiCHacks RSVP"
