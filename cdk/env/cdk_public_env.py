# Variables that do not need to be stored as secrets and modify the behavior of the AWS CDK


'''
-------------------------------------------------------
General variables
-------------------------------------------------------
'''

reusableStack = False
showPublicIp = False
ec2Type = "t4g.nano"

'''
-------------------------------------------------------
Schedule auto-on and auto-off. Set enableScheduler to True for that.
-------------------------------------------------------
'''

enableScheduler = True

startHour = "07"
startMinute = "0"

stopHour = "22"
stopMinute = "0"
