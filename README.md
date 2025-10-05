# Robot-s-Morning-Routine-BT
**项目简介**:  使用Python的行为树库py_trees，构建一个模拟机器人早晨起床流程的行为树。

**行为树**
<img width="1846" height="1033" alt="屏幕截图 2025-10-05 161458" src="https://github.com/user-attachments/assets/61996946-774e-49f2-8da6-e84e5f9dfb41" />

Sequence使用：闹钟响->起床/继续睡->->冲咖啡->工作
- 原因：此行为树是连续的，中断后就不能执行了，因此必须保证所有都成功才成功
  
Selector使用：闹钟响之后机器人的选择（起床、继续睡）、检查是否为工作日
- 原因：只需要一个节点成功就行

**思考题**
改进方法：加一个Is_workDay（）方法用于获取今天日期、判断是否为工作日
- 工作日：返回True   冲咖啡
- 非工作日：返回False  不冲咖啡

  
