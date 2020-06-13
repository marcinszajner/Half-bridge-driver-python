
class CommunicationStates_class():
    def __init__(self):
        self.sendIsEnable = True
        self.repeatPreMsg = False
        self.prevSendMsg = 0
        self.upSweepDirection = True

    def setSendState(self, status: bool):
        self.sendIsEnable = status

    def getSendState(self) -> bool:
        return self.sendIsEnable


    def setRepeatPrevMsgState(self, status: bool):
        self.repeatPreMsg = status

    def getRepeatPrevMsgState(self) -> bool:
        return self.repeatPreMsg


    def setPrevSendMsg(self, msg):
        self.prevSendMsg = msg

    def getPrevSendMsg(self):
        return self.prevSendMsg

    def getUpSweepDirectionState(self):
        return self.upSweepDirection

    def setUpSweepDirection(self, state: bool):
        self.upSweepDirection = state
