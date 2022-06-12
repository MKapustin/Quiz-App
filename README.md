# Application description

The app needs to have the functionalities of being able to build & host quizzes (simple
multiple-choice with questions and answers) that can be solved by using an API

## DB Structure

- user
  - id (PK)
  - email
	- created_date ?
  - is_admin 


 - quiz
   - id (PK)
   - author_id (user FK) 
   - state (enum Draft, Active, Archived)
   - title
   - created_at

**Note**: Draft quiz can be modified by adding questions, and changing title, but when quiz is Marked as Active it cannot be modified, and only after this invitation for the quiz can be sent)

- question
  - id (PK)
  - quiz_id (FK)
  - description
  - correct_answer_points


 - question_option
   - id (PK)
   - question_id (FK)
   - option_description
   - is_correct


 - question_answer
   - id (PK)
   - quiz_participation_id (FK)
   - question_id (FK)
   - question_option_id (FK)
   - created_at
 
**Notes:**
1. unique together: "participation", "question", "chosen_question_option"
2. quiz_participation_id is used in case the same quiz is passed by the same user several times


- quiz_invitation
  - id (PK)
  - uuid (unique constraint)
  - quiz_id (FK)
  - participant_id (FK to user)
  - state (enum SENT, REJECTED, ACCEPTED)
  - created_at
  - updated_at

**Notes**: 
1. Only the quiz author can send the invitation to the quiz
2. UUID is used to send the invitation links (in order not to expose inner DB
identifiers)
3. When the quiz is accepted - the quiz participation object should be created


- quiz_participation
    - id (PK)
    - quiz_id (FK)
    - participant_id (FK)
    - state (enum NOT_STARTED, ACTIVE, FINISHED, CANCELED)


### Expected business case for the quiz

1. The user registers or logs-in
2. The user creates a quiz (Draft quiz without questions attached)
3. The user adds questions to the quiz, User can modify the quiz title or even remove the quiz
4. User Activates the quiz (changes status from Draft to Active)
5. The user sends invitations to participants
6. Participants can either accept or cancel the quiz
7. In case of acceptance, a participant has access to the quiz 


## How to run app?

1. Run `docker-compose up`
2. Go to http://localhost:8000/doc/ to access swagger docs
3. To get access to the admin panel - http://localhost:8000/admin/

**[Optional]** To create django superuser:
1. docker exec -it <container ID> /bin/bash
2. ./manage.py createsuperuser