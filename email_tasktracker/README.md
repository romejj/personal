**Purpose**
This program serves as a no-cost alternative to project management tools. The automatic tracking of all requests from business users will not only prevent its loss in the plethora of emails, but also provide management a quick top-level view of all requests and their priorities.

**Overview**

This source code runs on Outlook and Microsoft Excel in a Windows machine, performing the following:
1. Scans the inbox every set interval for eligible emails
    - if email has a subject that contains predefined words ("Campaign request" in this case) AND
    - if email has a body that contains predefined words (if sender sends a team name and due date in this case)

2. All eligible emails are moved to a separate folder in Outlook.

3. All attachments from eligible emails are first prefixed with unique identifiers (to account for possibility of same      attachment names) before being saved in a central cloud folder. 

4. A master tracker Excel workbook is opened, and a new row is appended with the following information:
    - Index number
    - Task name/Email subject
    - Attachment names
    - Unique identifiers for attachments (from step 3.), for tracking in cloud folder
    - Team name, as specified by business user in email body
    - Email address of the sender
    - Due date of request, as specified by business user in email body
    - Task creation date, which corresponds to the date at which email is sent

5. The master tracker sheet is also updated every time there is a response to any eligible email. An update date is inserted in corresponding row that contains that specific task, so that the manager will have a better sense of the latest requirement gathering date.

6. The project manager can also set assignees in the master tracker sheet, afterwhich the program will automatically forward the respective emails to the assignees.