from prefect_email import EmailServerCredentials

credentials = EmailServerCredentials(
    username="EMAIL-ADDRESS-PLACEHOLDER",
    password="PASSWORD-PLACEHOLDER",  # must be an app password
)
credentials.save("BLOCK-NAME-PLACEHOLDER", overwrite=True)