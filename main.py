from fastapi import FastAPI, HTTPException
from mains import db
from models import User, UpdateUser
from fastapi.responses import JSONResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

app = FastAPI()

# Sample JSON data
json_data = '''{
  "employee": {
    "id": 12345,
    "name": "John Doe",
    "contact": {
      "email": "john.doe@example.com",
      "phone": "123-456-7890"
    },
    "projects": [
      {
        "project_id": 1,
        "name": "Project Alpha",
        "details": {
          "start_date": "2023-01-15",
          "end_date": "2023-07-30",
          "team_members": [
            {
              "id": 101,
              "name": "Alice Smith",
              "role": "Developer"
            },
            {
              "id": 102,
              "name": "Bob Johnson",
              "role": "Tester"
            }
          ]
        }
      },
      {
        "project_id": 2,
        "name": "Project Beta",
        "details": {
          "start_date": "2023-08-01",
          "end_date": "2023-12-31",
          "team_members": [
            {
              "id": 103,
              "name": "Charlie Lee",
              "role": "Designer"
            },
            {
              "id": 104,
              "name": "David Kim",
              "role": "Product Manager"
            }
          ]
        }
      }
    ]
  }
}'''

# Add User
@app.post("/add_users")
async def add_user(user: User):
    doc_ref = db.collection("users").document()
    doc_ref.set(user.dict())
    return {"id": doc_ref.id, **user.dict()}

# Get All Users
@app.get("/get_users")
async def get_users():
    users = [doc.to_dict() for doc in db.collection("users").stream()]
    return users

# Update User
@app.patch("/update_users/{user_id}")
async def update_user(user_id: str, user: UpdateUser):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    doc_ref.update({k: v for k, v in user.dict().items() if v is not None})
    return {"id": user_id, **doc_ref.get().to_dict()}

# Delete User
@app.delete("/delete_users/{user_id}")
async def delete_user(user_id: str):
    db.collection("users").document(user_id).delete()
    return {"detail": f"User {user_id} deleted"}

# Send Invitation Email via Gmail SMTP
@app.post("/send_invite")
async def send_invite():
    sender_email = "bhadaurimanish666@gmail.com"  # Replace with your Gmail address
    sender_password = ""  # Replace with your Gmail app password
    recipients = [
        "shraddha@aviato.consulting",
        "pooja@aviato.consulting",
        "prijesh@aviato.consulting",
        "hiring@aviato.consulting"
    ]

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "API Documentation Link and Firestore Screenshot"
    body = """
    <p>Hello,</p>
    <p>Please find the API documentation at the following links:</p>
    <ul>
        <li><a href='http://localhost:8000/docs'>Swagger API Docs</a></li>
        <li><a href='http://localhost:8000/redoc'>Redoc API Docs</a></li>
    </ul>
    <p>Screenshot of the Firestore Database is attached.</p>
    <p>Regards,<br>Backend Task</p>
    """
    msg.attach(MIMEText(body, 'html'))

    # Send the email using Gmail's SMTP server
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return JSONResponse(content={"detail": "Invitation sent successfully!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Projects as List of Dictionaries
@app.get("/projects")
async def get_projects():
    # Load JSON data
    data = json.loads(json_data)

    # Extract employee data
    projects = data['employee']['projects']

    # Create a list of dictionaries
    project_list = []
    for project in projects:
        project_info = {
            'project_id': project['project_id'],
            'project_name': project['name'],
            'start_date': project['details']['start_date'],
            'end_date': project['details']['end_date'],
            'team_members': []
        }

        # Extract team members
        for member in project['details']['team_members']:
            member_info = {
                'id': member['id'],
                'name': member['name'],
                'role': member['role']
            }
            project_info['team_members'].append(member_info)

        project_list.append(project_info)

    return project_list

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
