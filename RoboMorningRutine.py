import random
import py_trees
from datetime import date

BB_RING_COUNT="ring_count"
BB_MAX_RINGS="max_rings"
BB_IS_UP="is_up"
BB_DECISION="decision"
BB_FINISHED="finished"


class Init(py_trees.behaviour.Behaviour):
    def __init__(self,name="init"):
        super().__init__(name)
        self.bb=py_trees.blackboard.Client(name=self.name)
        for k in [BB_RING_COUNT,BB_MAX_RINGS,BB_IS_UP,BB_DECISION,BB_FINISHED]:
            self.bb.register_key(key=k,access=py_trees.common.Access.WRITE)

    def initialise(self):
        self.bb.set(BB_RING_COUNT,0)
        self.bb.set(BB_MAX_RINGS,3)
        self.bb.set(BB_IS_UP,False)
        self.bb.set(BB_DECISION,None)
        self.bb.set(BB_FINISHED,False)
        #self.bb.set(BB_FROM_DATE,10.1)

    def update(self):
        print("新的一天，闹钟最多响3次")
        return py_trees.common.Status.SUCCESS

class IsAlarmRinging(py_trees.behaviour.Behaviour):
    def __init__(self,name="is_alarm_ringing"):
        super(IsAlarmRinging,self).__init__(name)
        self.bb=py_trees.blackboard.Client(name=self.name)
        self.bb.register_key(key=BB_RING_COUNT,access=py_trees.common.Access.WRITE)
        self.bb.register_key(key=BB_MAX_RINGS,access=py_trees.common.Access.READ)


    def initialise(self):
        self.random_value=random.choice(["成功","失败"])
        self.logger.info(f"检查闹钟：{self.random_value}")

    def update(self):
        ct=self.bb.get(BB_RING_COUNT)
        mx=self.bb.get(BB_MAX_RINGS)
        if ct<=mx:
            ct+=1
            py_trees.blackboard.Blackboard().set(BB_RING_COUNT,ct)
            self.logger.info(f"闹钟第{ct}次响")
            if self.random_value=="成功":
                self.logger.info(f"检查闹钟，结果为{self.random_value}")
                return py_trees.common.Status.SUCCESS
            else:
                self.logger.info("睡不醒......检查闹钟失败")
                return py_trees.common.Status.FAILURE

class Decide(py_trees.behaviour.Behaviour):
    def __init__(self,name="decide"):
        super().__init__(name)
        self.bb=py_trees.blackboard.Client(name=self.name)
        self.bb.register_key(key=BB_DECISION,access=py_trees.common.Access.WRITE)

    def update(self):
        decision=random.choice(["SNOZE","GETUP"])
        self.bb.set(BB_DECISION,decision)
        self.logger.info(f"闹钟响后做出的选择：{decision}")
        return py_trees.common.Status.SUCCESS


class HitSnoozeButton(py_trees.behaviour.Behaviour):

    def __init__(self,name="hitSnoozeButton"):
        super(HitSnoozeButton,self).__init__(name)
        self.bb=py_trees.blackboard.Client(name=self.name)
        self.bb.register_key(key=BB_RING_COUNT,access=py_trees.common.Access.WRITE)

    def update(self):
        CURRENT_TIME=self.bb.get(BB_RING_COUNT)
        if CURRENT_TIME<=3:
            self.logger.info(f"Snoozing...")
            return py_trees.common.Status.SUCCESS
        else:
            self.logger.info("闹钟次数用完，今天放假")
            return py_trees.common.Status.FAILURE
class GetOutOfBed(py_trees.behaviour.Behaviour):
    def __init__(self,name="getUp"):
        super(GetOutOfBed,self).__init__(name)
        self.bb=py_trees.blackboard.Client(name=self.name)
        self.bb.register_key(key=BB_IS_UP,access=py_trees.common.Access.WRITE)

    def update(self):
        self.logger.info("Getting up!")
        self.bb.set(BB_IS_UP,True)
        return py_trees.common.Status.SUCCESS
class BrewCoffee(py_trees.behaviour.Behaviour):
    def __init__(self,name="brewCoffee"):
        super(BrewCoffee,self).__init__(name)
    def update(self):
        self.logger.info("Brewing coffee...")
        return py_trees.common.Status.SUCCESS

class toWork(py_trees.behaviour.Behaviour):
    def __init__(self,name="toWork"):
        super(toWork,self).__init__(name)
    def update(self):
        self.logger.info("goToWorking! ")
        return py_trees.common.Status.SUCCESS

class giveUpMorning(py_trees.behaviour.Behaviour):
    def __init__(self,name="giveUpMorning"):
        super(giveUpMorning,self).__init__(name)
    def update(self):
        self.logger.info("关闭闹钟，给自己放假。")
        return py_trees.common.Status.SUCCESS


class CheckExhausted(py_trees.behaviour.Behaviour):
    def __init__(self,name="checkExhausted"):
        super().__init__(name)
        self.bb=py_trees.blackboard.Client(name=self.name)
        self.bb.register_key(key=BB_MAX_RINGS,access=py_trees.common.Access.READ)
        self.bb.register_key(key=BB_RING_COUNT,access=py_trees.common.Access.READ)

    def update(self):
        cnt=self.bb.get("ring_count")
        mx=self.bb.get("max_rings")
        if cnt >= mx:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE
class end(py_trees.behaviour.Behaviour):
    def __init__(self,name="end"):
        super(end,self).__init__(name)
        self.bb=py_trees.blackboard.Client(name=self.name)
        self.bb.register_key(key=BB_FINISHED,access=py_trees.common.Access.WRITE)

    def update(self):
        print("早上日程结束...")
        self.bb.set(BB_FINISHED,True)
        return py_trees.common.Status.SUCCESS

class Checkdecision(py_trees.behaviour.Behaviour):
    def __init__(self,expected_value,name="checkdecision"):
        super().__init__(name)
        self.bb=py_trees.blackboard.Client(name=self.name)
        self.expected=expected_value
        self.bb.register_key(key=BB_DECISION,access=py_trees.common.Access.READ)

    def update(self):
        current=self.bb.get("decision")
        if current==self.expected:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class CheckIsUp(py_trees.behaviour.Behaviour):
    def __init__(self,name="checkIsUp"):
        super().__init__(name)
        self.bb=py_trees.blackboard.Client(name=self.name)
        self.bb.register_key(key=BB_IS_UP,access=py_trees.common.Access.READ)

    def update(self):
        if self.bb.get(BB_IS_UP):
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

def Is_workDay(day=None):
    if day is None:
        day=date.today()
    return day.weekday()<5

class CheckDate(py_trees.behaviour.Behaviour):
    def __init__(self,name="checkDate"):
        super().__init__(name)

    def update(self):
        if Is_workDay():
            self.logger.info("检查日历->今天是工作日")
            return py_trees.common.Status.SUCCESS
        else:
            self.logger.info("检查日历->今天是周末")
            return py_trees.common.Status.FAILURE


def creat_tree():
    bb_read=py_trees.blackboard.Client(name="reader")
    for k in [BB_RING_COUNT,BB_IS_UP,BB_DECISION,BB_FINISHED]:
        bb_read.register_key(key=k,access=py_trees.common.Access.READ)

    noAlarmTimes=py_trees.composites.Sequence("NoAlarmTimes",memory=True)
    noAlarmTimes.add_child(giveUpMorning())
    cond_getup=py_trees.composites.Sequence("ConditionGetUp",memory=True)
    cond_getup.add_children([Checkdecision("GETUP"),GetOutOfBed(),CheckDate(),BrewCoffee()])

    cond_snooze=py_trees.composites.Sequence("ConditionSnooze",memory=True)
    cond_snooze.add_children([Checkdecision("SNOZE"),HitSnoozeButton(),IsAlarmRinging(),noAlarmTimes])

    alarm_selector=py_trees.composites.Selector("alarmSelector",memory=False)
    alarm_selector.add_children([cond_getup,cond_snooze])
    alarm_cycle=py_trees.composites.Sequence("AlarmCycle",memory=True)
    alarm_cycle.add_children([IsAlarmRinging(),Decide(),alarm_selector])

    root_sequence=py_trees.composites.Sequence("AlarmRing",memory=True)
    root_sequence.add_children([Init(),alarm_cycle,end()])
    return py_trees.trees.BehaviourTree(root=root_sequence)



if __name__=="__main__":
    tree=creat_tree()
    tree.setup(timeout=10)
    bb=py_trees.blackboard.Blackboard()
    for i in range(10):
        print(f"\n--- TICK #{i + 1} ---")
        print("闹钟响了.....")
        print("Routine：")
        tree.tick()
        if bb.get(BB_FINISHED) is True:
            continue


