import boto3
import os
import dotenv
from botocore.exceptions import ClientError
from customSecrets import get_secret

def send_email_invite(recipient_address, invitor, url_link):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = get_secret('AWS_SES_ACCOUNT')

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = recipient_address

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = f"Checkers Game Invite - From {invitor}"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = f'You have an invite to player Checkers on the Cloud!\r\n Go to {url_link} to accept the invite!'
                
                
    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>New Invite!</h1>
    <p>{invitor} wants to play checkers!</p>
    <p>Log in to <a href='{url_link}'>your home page</a> to accept the invite!
    </body>
    </html>
                """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION,
                            aws_access_key_id=get_secret("access_key_id"),
                            aws_secret_access_key=get_secret("access_key_secret"),)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])