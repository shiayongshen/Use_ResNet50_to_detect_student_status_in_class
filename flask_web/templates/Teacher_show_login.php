<?php
include('connectMySQL.php');
    session_start();
    
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $id = $_POST['id'];
        $name = $_POST['name'];
        $time = $_POST['time'];
        $login = $_POST['login'];
    }

	$query = "SELECT id, name, time, login FROM students";
	//mysqli_query << PHP 有很多種...指令(?) ，這是其中一個，我現在還都是學到甚麼用什麼，沒辦法自己看手冊，然後實驗+學習使用。 

	$query_run = mysqli_query($db_link,$query); //$con <<此變數來自引入的 db_cn.php
?>


<!DOCTYPE html>
<html lang="en">

<head>
	<title>學生登入狀態</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
      body{
        height:570px;
        background:linear-gradient(#EBEAEA,#E4E3E3,#BCBBBB);
        font-family:Microsoft JhengHei;
      }
      h2{
        font-family:Microsoft JhengHei;
      }
      input{
        display:inline-block;
  
        border:solid 1px black;
        border-radius: 5px;
  
        padding:10px;
        padding-left:20px;
        padding-right:20px;
  
        font-family:Microsoft JhengHei;
  
        position:fixed;
        right:60px;
        top:480px;

        color:white;
        background-color:#4472C4;
       }
      .hp:hover{
         color:#4472C4;
         background-color:#fff;
         border:2px #4472C4 solid;
      }
      .enter{
        color:black;
        background-color:#D6DCE5;
      }
    </style>
</head>

<body onload="startTime()">
<div class="container">

    <h2>學生登入狀態</h2>
    <p align = "right"><span id = "nowDateTimeSpan"></span></p>
	<table class="table table-sm table-bordered"style="text-align:center;">
		<thead style="text-align:center;">
			<tr style="text-align:center;">
				<th>學號</th>
				<th>姓名</th>
                <th>登入時間</th>
				<th>登入狀態</th>
			</tr>
		</thead>

		<tbody>
			<!-- 大括號的上、下半部分 分別用 PHP 拆開 ，這樣中間就可以純用HTML語法-->
			<?php
				if(mysqli_num_rows($query_run) > 0)
				{
					foreach($query_run as $row)
					{
			?>
							<tr>
								<!-- $row['(輸入資料表的欄位名稱)'];  <<用雙引號也行 -->
								<td><?php echo $row['id']; ?></td> 
								<td><?php echo $row['name']; ?></td> 
								<td><?php echo $row['time']; ?></td>
                                <td><?php 
                                        if($row['login'] == '1'){
                                            echo "已登入";
                                        }                               
                                        else{
                                            echo"<font color=gray>未登入</font>";
                                        }
                                    ?></td>
							</tr>
			<?php
				  }
				}
			?>
		</tbody>
        <a href = "Teacher_show_data.php">
                <input type = "button" value = "確認並開始上課" class = "hp">
        </a>
    <script>
    function startTime()   
            {   
                var today=new Date();//定義日期物件   
                var yyyy = today.getFullYear();//通過日期物件的getFullYear()方法返回年    
                var MM = today.getMonth()+1;//通過日期物件的getMonth()方法返回年    
                var dd = today.getDate();//通過日期物件的getDate()方法返回年     
                var hh=today.getHours();//通過日期物件的getHours方法返回小時   
                var mm=today.getMinutes();//通過日期物件的getMinutes方法返回分鐘   
                var ss=today.getSeconds();//通過日期物件的getSeconds方法返回秒   
                var aa;
				// 如果分鐘或小時的值小於10，則在其值前加0，比如如果時間是下午3點20分9秒的話，則顯示15：20：09   
                  
                var day; //用於儲存星期（getDay()方法得到星期編號）
                if(today.getDay()==0)   day   =   "星期日 " 
                if(today.getDay()==1)   day   =   "星期一 " 
                if(today.getDay()==2)   day   =   "星期二 " 
                if(today.getDay()==3)   day   =   "星期三 " 
                if(today.getDay()==4)   day   =   "星期四 " 
                if(today.getDay()==5)   day   =   "星期五 " 
                if(today.getDay()==6)   day   =   "星期六 " 
				document.getElementById('nowDateTimeSpan').innerHTML=yyyy+"/"+MM +"/"+ dd + "   " + hh+":"+mm+":"+ss+"   " +"     " +day;   
                setTimeout('startTime()',1000);//每一秒中重新載入startTime()方法 
            }   

            function checkTime(i)   
            {   
                if (i<10){
                    i="0" + i;
                }   
                  return i;
            }
    </script>  

	</body>

</div>

<!--BOOTSTRAP的東西------------------------------------------------------------------------->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</html>