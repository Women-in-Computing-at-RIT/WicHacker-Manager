def getAppliedEmail(firstName, lastName):
    try:
        appliedEmail = open('./src/data/emailTemplates/applied.html', 'r')
        contents = appliedEmail.read()
        appliedEmail.close()
        contents = contents.replace("first_name", firstName).replace("last_name", lastName)
        return contents
    except:    
        return f'<div>' \
            f'   <div>' \
            f'       WiCHacks Header' \
            f'   </div>' \
            f'   <div>' \
            f'       <h3>Thank you for applying {firstName} {lastName}!</h3>' \
            f'       <p>' \
            f'           Your application has been submitted and will be reviewed by a WiCHacks Organizer' \
            f'       </p>' \
            f'   </div>' \
            f'   <div>' \
            f'       WiCHacks Footer' \
            f'   </div>' \
            f'</div>'


def getAppliedSubjectLine() -> str:
    return "WiCHacks Application Received"
