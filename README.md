# Medea

### STATE: In progress

Script is using UpCloud API.
UpCloud API documentation -> https://developers.upcloud.com/1.3/

Core functionalities:
 - Deal only with Scheduled Backups, on demand backups are out of scope.
 - Check backup state.
 - Chcek if backup was complited or not.
 - Send notification to Slack channel if backup failed.

To be done:
 - Integration with Slack
 - Checking if backup was successfull after specific timestamp for every server (with custom backup settings)
 - Code refactoring
