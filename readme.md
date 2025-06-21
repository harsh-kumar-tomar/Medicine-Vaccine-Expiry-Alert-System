# Workflow of MVEAS
1. Health Worker adds new stock via mobile frontend (calls API).

2. Backend saves it in PostgreSQL with name, batch, expiry_date, etc.

3. Daily Celery job runs and:

4. Finds all medicines expiring in, say, 7 days.

5. Sends push/email/WebSocket notification or stores alert.

6. User can mark items as used/expired.

7. All actions logged in audit table.

8. Gov  can download/view logs for compliance.