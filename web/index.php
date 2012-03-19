<?php
	$con = mysql_connect("localhost", "root", "Jabaman1");
        if (!$con)
        {
                die('Could not connect: '.mysql_error());
        }

        mysql_select_db("movTorrent", $con);
	if ($_GET['action'] == 'approveMovie')
	{
		mysql_query("UPDATE MovieFiles SET FileStates_id = 1 WHERE id = ".$_GET['mid']);
		mysql_query("DELETE FROM MovieTitles WHERE MovieFiles_id = ".$_GET['mid']." AND id != ".$_GET['tid']);
		header('Location:index.php');
	} elseif ($_GET['action'] == 'ignoreMovie')
	{
		mysql_query("UPDATE MovieFiles SET FileStates_id = 3 WHERE id = ".$_GET['mid']);
		mysql_query("DELETE FROM MovieTitles WHERE MovieFiles_id = ".$_GET['mid']);
		header('Location:index.php');
	} elseif ($_GET['action'] == 'approveTv')
	{
		mysql_query("UPDATE TvSeries SET FileStates_id = 2, alias = series WHERE id = ".$_GET['eid']);
		header('Location:index.php');
	} elseif ($_GET['action'] == 'ignoreTv')
	{
		mysql_query("UPDATE TvSeries SET FileStates_id = 3 WHERE id = ".$_GET['eid']);
		header('Location:index.php');
	} elseif ($_GET['action'] == 'customTv')
	{
		mysql_query("UPDATE TvSeries SET FileStates_id = 2, alias = '".$_GET['alias']."' WHERE id = ".$_GET['eid']);
		header('Location:index.php');
	}
?>
<!DOCTYPE html>
<html>
<head>
	<title>MovTorrent</title>
	<link rel="stylesheet" type="text/css" href="mov.css" />
	<script src="jquery-1.6.4.min.js"></script>
	<script src="mov.js"></script>
	<meta name="viewport" content="width=device-width,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no" />
</head>
<body>
	<div id="menu">
        <ul>
            <li onclick="movieTab()">Movies</li>
            <li onclick="tvTab()">TV Series</li>
            <li onclick="infoTab()">Server Info</li>
        </ul>
    </div>
	<div id="container">
		<div id="contentWrapper">
			<div id="moviesContent" class="content">
				<?php
				//Movies
					$result = mysql_query("SELECT * FROM MovieFiles WHERE FileStates_id = 0");
					while($row = mysql_fetch_array($result))
					{
							echo "<div class='header' onclick='expandMovieSlider(".$row['id'].")'><p>".$row['path']."</p></div>";
					echo "<div id='sliderMovie".$row['id']."' class='slider'>";
					echo "<ul class='sliderList'>";
					$subresult = mysql_query("SELECT * FROM MovieTitles WHERE MovieFiles_id = ".$row['id']);
					while($subrow = mysql_fetch_array($subresult))
					{
						echo "<li onclick='approveMovie(".$row['id'].",".$subrow['id'].")'>".$subrow['title']."</li>";
					}
					echo "<li onclick='ignoreMovie(".$row['id'].")'>Ignore</li>";
					echo "<li onclick='customMovie(".$row['id'].")'>Search Other Title</li>";
					echo "</ul></div>";
					echo "<div id='sliderMovieText".$row['id']."' class='slider'>";
					echo "<form method='GET' action='cgi-bin/customMovie.cgi'><input type='hidden' name='action' value='customMovie'><input type='text' name='raw' /><input type='hidden' name='mid' value='".$row['id']."' /></form>";
					echo "</div>";

					}
				?>
			</div>
			<div id="tvContent" class="content">
				<?php
				//Tv
					$result = mysql_query("SELECT * FROM TvSeries WHERE FileStates_id = 0");
					while($row = mysql_fetch_array($result))
					{
							echo "<div class='header' onclick='expandTvSlider(".$row['id'].")'><p>".$row['series']."</p></div>";
					echo "<div id='sliderTv".$row['id']."' class='slider'>";
					echo "<ul class='sliderList'>";
					echo "<li onclick='approveTv(".$row['id'].")'>Approve</li>";
					echo "<li onclick='ignoreTv(".$row['id'].")'>Ignore</li>";
					echo "<li onclick='customTv(".$row['id'].")'>Enter Alias</li>";
					echo "</ul></div>";
					echo "<div id='sliderTvText".$row['id']."' class='slider'>";
					echo "<form method='GET' action='index.php'><input type='hidden' name='action' value='customTv'><input type='text' name='alias' /><input type='hidden' name='eid' value='".$row['id']."' /></form>";
					echo "</div>";
					}
					mysql_close($con);
				?>
			</div>
			<div id="infoContent" class="content">
				<?php
					$lines = file('info.txt');
					foreach ($lines as $line) {
						echo "<div class='header'><p>".$line."</p></div>";
						//echo $line."<br />";
					}
				?>
			</div>
			<div id="dummyContent" class="content"></div>
		</div>
	</div>
</body>
</html>

