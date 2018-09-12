# create a new exam
curl -X POST -H 'Content-Type: application/json' -d '{
  "title": "TypeScript Advanced Exam",
  "description": "Tricky questions about TypeScript."
}' http://0.0.0.0:5000/exams

curl -X POST -H 'Content-Type: application/json' -d '{
  "title": "Tensorflow Advanced Exam",
  "description": "Basic questions about machine learning."
}' http://0.0.0.0:5000/exams

# retrieve exams
curl http://0.0.0.0:5000/exams

curl -X POST -H 'Content-Type: application/json' -d '{
  "email": "finn@ft.com",
  "password": "pass"
}' http://0.0.0.0:5000/auth/register


curl -X POST -H 'Content-Type: application/json' -d '{
  "email": "finn@ft.com",
  "password": "pass"
}' http://0.0.0.0:5000/auth/login

token=$(curl -s -X POST -H 'Content-Type: application/json' -d '{                                           "email": "finn@ft.com",
  "password": "pass"
}' http://0.0.0.0:5000/auth/login | jq .auth_token|sed 's/"//g')

curl -H 'Content-Type: application/json' -H "Authorization: Bearer $token"  http://0.0.0.0:5000/auth/statu


curl -H 'Content-Type: application/json' -H "Authorization: Bearer $token"  http://0.0.0.0:5000/auth/logout

