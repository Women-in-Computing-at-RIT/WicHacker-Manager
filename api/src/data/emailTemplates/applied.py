def getAppliedEmail(firstName, lastName):
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
