from backend.app.model_utils import predict_message

msg = "Votre compte bancaire sera suspendu. Cliquez ici immédiatement pour vérifier vos informations."
result = predict_message(msg)

print(result)