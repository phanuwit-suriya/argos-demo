# Feedback Server

Coming soon...

## Sequence Diagram
<img src="https://gitlab.com/phanuwit.suriya/argos-demo/raw/develop-branch/static/img/sequence-diagram.png">

Above is a simple sequence diagram of permission granter API usage. This describes how operations between anomaly detector instance and permission granter server are interact.

Everytime email sender module wants to notify users, it has to send a request to permission granter server for permission by sending HTTP request. Server will decides whether request should be granted or not by checking all criteria, then respond a permission back to email sender module. Email sender module, if permission is granted, will notify users by sending an email with anomaly information and attach URI to email body. Clicking URI is to let server knows that users no longer want to be notified for that metric.

- Criteria
    - Recent anomaly's start timestamp must be higher than the previous' one.
    - Permission assigned from a user