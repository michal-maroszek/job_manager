from password_validator import PasswordValidator

MIN_NAME_LENGTH = 2
PW_VALIDATION_SCHEMA = (
    PasswordValidator()
    .min(8)
    .max(64)
    .has()
    .uppercase()
    .has()
    .lowercase()
    .has()
    .digits()
    .has()
    .symbols()
)

EMAIL_FORMAT = True
# check whether the email address has a valid structure
EMAIL_BLACKLIST = True
# check the email against the blacklist of domains downloaded from https://github.com/disposable-email-domains/disposable-email-domains
EMAIL_DNS = True
# check the DNS mx-records
EMAIL_SMTP = True
# check whether the email actually exists by initiating an SMTP conversation
