# 这是一个员工信息表管理程序

### 作者介绍：
* author：haohe
* nickname:Howard
* My Blog:[http://987774031.blog.51cto.com/](http://987774031.blog.51cto.com)

### 功能介绍：
* 可进行模糊查询，支持下面3种语法：  

		select name,age from staff_table where age > 22;
		select  * from staff_table where dept = "IT" ; 
		select  * from staff_table where enroll_date like "2013"  ;

  查到的信息，打印后，最后面显示查到的条数 
* 创建新员工纪录，以phone做唯一键，staff_id自增
* 可删除指定员工信息纪录，输入员工id，即可删除,语法如下：     
      
      1
* 可修改员工信息，语法如下:     
     
      UPDATE staff_table SET dept="Market" WHERE  dept = "IT";(Market、IT可替换)
* 语法说明：字段间空格数无限制，字段中字符串可用“” ‘’ 或不用引号
### 环境依赖：
* Python3.0+

###程序调试环境：
* mac
