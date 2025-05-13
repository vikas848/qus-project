# qus-project

qus_data  name ke databse me jitni tables ka use kiya gya h  -------------

MariaDB [qus_data]> show tables;
+--------------------+
| Tables_in_qus_data |
+--------------------+
| qus_data_table     |
| save_qus_type1     |
| save_qus_type2     |
| save_qus_type3     |
| save_qus_type4     |
| save_qus_type5     |
+--------------------+
6 rows in set (0.001 sec)

MariaDB [qus_data]> 



create tables -----------

MariaDB [qus_data]> create table save_qus_type2( sr int not null auto_increment, Question char(255), option1 char(255), option2 char(255), option3 char(255), option4 char(255), Correct_Option char(255), primary key(sr));
Query OK, 0 rows affected (0.015 sec)
MariaDB [qus_data]> 

<h1>registion page</h1>
<img src="static/img/register page.png">

<h1>login page</h1>
<img src="static/img/login page.png">

<h1>home page</h1>
<img src="static/img/home page.png">

<h1>exam question insert page</h1>
<img src="static/img/question page.png">

<h1>exam question update page</h1>
<img src="static/img/question update page.png">

<h1>exam page</h1>
<img src="static/img/exam page.png">

<h1>exam result page</h1>
<img src="static/img/result page.png">