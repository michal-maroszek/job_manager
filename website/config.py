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

EMAIL_SCHEMA = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
